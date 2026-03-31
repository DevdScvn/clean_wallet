import dishka_faststream
from dishka import make_async_container
from faststream import FastStream

from clean_backend.config.settings import settings
from clean_backend.infrastructure.broker import new_broker
from clean_backend.ioc import AppProvider

container = make_async_container(AppProvider())


broker = new_broker(settings.broker.rabbit)
faststream_app = FastStream(broker)
dishka_faststream.setup_dishka(
    container,
    faststream_app,
    auto_inject=True,
)