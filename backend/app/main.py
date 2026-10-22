from fastapi import FastAPI
from app.api.routes.tools import router
from app.core.config import settings

app = FastAPI(title=settings.app_name)
app.include_router(router, prefix="/api/tools", tags=["tools"])


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
