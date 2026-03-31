from collections.abc import AsyncIterator

import pytest
import pytest_asyncio
from dishka import AsyncContainer
from faker import Faker
from fastapi import FastAPI
from dishka.integrations.fastapi import setup_dishka
from httpx import AsyncClient, ASGITransport
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from clean_backend.controllers.api.v1 import users_router
from clean_backend.infrastructure import models


@pytest_asyncio.fixture
async def http_app(container: AsyncContainer) -> FastAPI:
    app = FastAPI()
    app.include_router(router=users_router)
    setup_dishka(container, app)
    return app


@pytest_asyncio.fixture
async def http_client(http_app: FastAPI) -> AsyncIterator[AsyncClient]:
    async with AsyncClient(
        transport=ASGITransport(app=http_app),
        base_url="http://",
    ) as client:
        yield client


@pytest.mark.asyncio
async def test_get_book(
    session: AsyncSession,
    http_client: AsyncClient,
    faker: Faker,
) -> None:
    user_id = UUID(faker.uuid4())
    # DB constraint requires length 3..32
    username = faker.pystr(min_chars=3, max_chars=32)

    await session.execute(
        insert(models.User).values(id=user_id, username=username)
    )

    result = await http_client.get(f"/users/{user_id}/")
    assert result.status_code == 200
    assert result.json()["username"] == username
