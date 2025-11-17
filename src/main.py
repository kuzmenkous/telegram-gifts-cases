from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from src.core.config import settings
from src.exception_handlers import get_exception_handlers
from src.routers import admins_router, auth_router
from src.schemas.errors import ServerErrorSchema
from src.schemas.validation import ValidationErrorListSchema

# App configuration
app = FastAPI(
    title=settings.app.name,
    debug=settings.debug,
    root_path=f"/v{settings.app.version}",
    version=str(settings.app.version),
    docs_url=settings.app.docs_url if settings.debug else None,
    redoc_url=settings.app.redoc_url if settings.debug else None,
    exception_handlers=get_exception_handlers(),
    default_response_class=ORJSONResponse,
    responses={
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": ValidationErrorListSchema,
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "example": {
                        "errors": [
                            {"field": "field1", "detail": "error1"},
                            {"field": "field2", "detail": "error2"},
                        ]
                    }
                }
            },
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": ServerErrorSchema,
            "description": "Bad Request",
            "content": {
                "application/json": {
                    "example": {"code": 400, "detail": "error"}
                }
            },
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ServerErrorSchema,
            "description": "Not Found",
            "content": {
                "application/json": {
                    "example": {"code": 404, "detail": "Object not found"}
                }
            },
        },
    },
    swagger_ui_parameters={
        "docExpansion": None,
        "tryItOutEnabled": settings.debug,
        "displayRequestDuration": True,
        "filter": True,
        "requestSnippetsEnabled": True,
    },
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
for router in (auth_router, admins_router):
    app.include_router(router)
