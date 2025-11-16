#!/bin/sh

# Define the application base directory
APP_DIR="/app/api"

# Wait for dependent services to be ready (PostgreSQL, Redis etc)
sleep 5

if [ -e ".env" ]; then
    # Load .env file safely, handling quotes and whitespace
    while IFS='=' read -r key value; do
        # Trim whitespace from the key and value
        key=$(echo "$key" | xargs)
        value=$(echo "$value" | xargs)

        # Skip comments and empty lines
        case "$key" in
            \#* | "") continue ;;
        esac

        # Remove surrounding quotes from the value if present
        value=$(echo "$value" | sed 's/^["'\''"]//;s/["'\''"]$//')

        # Export the variable
        export "$key=$value"
    done < ".env"
    echo "Loaded environment file: .env"
else
    echo "No environment file found at .env. Exiting."
    exit 1
fi
set +a

# Navigate to the application directory
cd "$APP_DIR" || { echo "Failed to change directory to $APP_DIR. Exiting."; exit 1; }

# Database migration
if grep -qi '^ALEMBIC_RUN_MIGRATIONS=True' .env; then
    alembic upgrade head || { echo "Alembic upgrade failed. Exiting."; exit 1; }
fi

# Set the default message format for app mode
APP_MODE_MESSAGE="Starting the application in %s mode..."

# Check the MODE environment variable
if [ "$MODE" = "PROD" ]; then
    # Production mode: start Supervisor
    echo "Starting the application in production mode..."
    /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf

elif [ "$MODE" = "DEV" ]; then
    # Development or debug mode
    if [ "$DEBUG" = "1" ]; then
        printf "$APP_MODE_MESSAGE" "debug"
        uvicorn src.main:app --reload --host 0.0.0.0 --port "$APP_PORT"
    else
        printf "$APP_MODE_MESSAGE" "production"
        gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind "0.0.0.0:$APP_PORT"
    fi
else
    echo "No valid MODE set. Exiting..."
    exit 1
fi
