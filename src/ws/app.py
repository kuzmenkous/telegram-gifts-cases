from fastapi import FastAPI

from src.core.config import settings

app = FastAPI(debug=settings.debug, title="WS")

for router in ():  # type: ignore[var-annotated]
    app.include_router(router)
