from __future__ import annotations

from collections.abc import AsyncIterator
from decimal import Decimal
from uuid import UUID

import pytest
import pytest_asyncio
from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from faker import Faker
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from clean_backend.controllers.api.v1 import wallet_router
from clean_backend.infrastructure import models


@pytest_asyncio.fixture
async def http_app(container: AsyncContainer) -> FastAPI:
    app = FastAPI()
    app.include_router(router=wallet_router)
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
async def test_create_wallet(
    session: AsyncSession,
    http_client: AsyncClient,
    faker: Faker,
) -> None:
    user_id = UUID(faker.uuid4())
    username = faker.pystr(min_chars=3, max_chars=32)
    await session.execute(insert(models.User).values(id=user_id, username=username))

    res = await http_client.post(
        "/wallets/",
        json={"user_id": str(user_id), "balance": "10.00"},
    )
    assert res.status_code == 201
    body = res.json()
    assert body["user_id"] == str(user_id)
    assert UUID(body["id"])  # valid uuid


@pytest.mark.asyncio
async def test_get_wallet_balance_by_wallet_id(
    session: AsyncSession,
    http_client: AsyncClient,
    faker: Faker,
) -> None:
    user_id = UUID(faker.uuid4())
    username = faker.pystr(min_chars=3, max_chars=32)
    wallet_id = UUID(faker.uuid4())

    await session.execute(insert(models.User).values(id=user_id, username=username))
    await session.execute(
        insert(models.Wallet).values(id=wallet_id, user_id=user_id, balance=Decimal("12.34"))
    )

    res = await http_client.get(f"/wallets/{wallet_id}")
    assert res.status_code == 200
    body = res.json()
    assert Decimal(str(body["balance"])) == Decimal("12.34")
    assert body["username"] == username


@pytest.mark.asyncio
async def test_wallet_operation_deposit(
    session: AsyncSession,
    http_client: AsyncClient,
    faker: Faker,
) -> None:
    user_id = UUID(faker.uuid4())
    username = faker.pystr(min_chars=3, max_chars=32)
    wallet_id = UUID(faker.uuid4())

    await session.execute(insert(models.User).values(id=user_id, username=username))
    await session.execute(
        insert(models.Wallet).values(id=wallet_id, user_id=user_id, balance=Decimal("10.00"))
    )

    res = await http_client.post(
        f"/wallets/{wallet_id}/operation",
        json={"operation_type": "DEPOSIT", "amount": "5.00"},
    )
    assert res.status_code == 200
    body = res.json()
    assert Decimal(str(body["balance"])) == Decimal("15.00")
    assert body["username"] == username


@pytest.mark.asyncio
async def test_wallet_operation_withdraw_insufficient_funds(
    session: AsyncSession,
    http_client: AsyncClient,
    faker: Faker,
) -> None:
    user_id = UUID(faker.uuid4())
    username = faker.pystr(min_chars=3, max_chars=32)
    wallet_id = UUID(faker.uuid4())

    await session.execute(insert(models.User).values(id=user_id, username=username))
    await session.execute(
        insert(models.Wallet).values(id=wallet_id, user_id=user_id, balance=Decimal("1.00"))
    )

    res = await http_client.post(
        f"/wallets/{wallet_id}/operation",
        json={"operation_type": "WITHDRAW", "amount": "2.00"},
    )
    assert res.status_code == 400
    assert res.json()["detail"] == "Insufficient funds for this withdrawal."


@pytest.mark.asyncio
async def test_get_wallets_list(
    session: AsyncSession,
    http_client: AsyncClient,
    faker: Faker,
) -> None:
    user_id = UUID(faker.uuid4())
    username = faker.pystr(min_chars=3, max_chars=32)
    await session.execute(insert(models.User).values(id=user_id, username=username))

    wallet_id_1 = UUID(faker.uuid4())
    wallet_id_2 = UUID(faker.uuid4())
    await session.execute(
        insert(models.Wallet),
        [
            {"id": wallet_id_1, "user_id": user_id, "balance": Decimal("0.00")},
            {"id": wallet_id_2, "user_id": user_id, "balance": Decimal("3.21")},
        ],
    )

    res = await http_client.get("/wallets/")
    assert res.status_code == 200
    body = res.json()
    assert isinstance(body, list)
    ids = {item["id"] for item in body}
    assert {str(wallet_id_1), str(wallet_id_2)}.issubset(ids)

