__all__ = (
    "broker",
    "faststream_app",
)

from dishka import make_async_container

from clean_backend.controllers.amqp.users import router as users_router
from clean_backend.fs_app import broker, faststream_app
from clean_backend.ioc import AppProvider

container = make_async_container(AppProvider())

broker.include_router(users_router)
