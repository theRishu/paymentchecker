from fastapi import FastAPI

from api.auth import router as auth_router
from api.dashboard import router as dashboard_router
from api.webhook import router as webhook_router


def create_app(bot) -> FastAPI:
    app = FastAPI(title="PaymentChecker Pro")
    app.state.bot = bot
    app.include_router(auth_router)
    app.include_router(dashboard_router)
    app.include_router(webhook_router)
    return app
