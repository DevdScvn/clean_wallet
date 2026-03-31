from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from dishka import make_async_container
from fastapi import FastAPI

from dishka.integrations.fastapi import setup_dishka

from clean_backend.config.settings import settings
from clean_backend.controllers.api import router as api_router
from clean_backend.fs_app import broker
from clean_backend.ioc import AppProvider

container = make_async_container(AppProvider())


@asynccontextmanager
async def lifespan(
    _: FastAPI,
) -> AsyncGenerator[None]:
    await broker.start()
    yield
    await broker.stop()


def get_fastapi_app() -> FastAPI:
    fastapi_app = FastAPI(
        title=settings.app.title,
        lifespan=lifespan,
    )

    fastapi_app.include_router(api_router)

    setup_dishka(container, fastapi_app)

    return fastapi_app


def get_app() -> FastAPI:
    fastapi_app = get_fastapi_app()

    return fastapi_app


app = get_app()
