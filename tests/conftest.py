import os
from typing import Any, AsyncGenerator
from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio
import asyncpg
from dishka import AnyOf, AsyncContainer, Provider, Scope, make_async_container, provide

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from clean_backend.application import interfaces

# Default tests to an isolated DB so drop/create never touches dev DB.
# You can override these when running tests:
# - Variant 1 (same container, separate DB): keep PORT=5443, NAME=backend_test
# - Variant 2 (separate pg_test service): set PORT=5444 (and optionally HOST)
os.environ.setdefault("BACKEND__DB__PG__NAME", "backend_test")
os.environ.setdefault("BACKEND__DB__PG__HOST", "localhost")
os.environ.setdefault("BACKEND__DB__PG__PORT", "5443")
os.environ.setdefault("BACKEND__DB__PG__USER", "app")
os.environ.setdefault("BACKEND__DB__PG__PASSWORD", "password")

from clean_backend.config.settings import settings
from clean_backend.infrastructure.models import Base
from clean_backend.ioc import AppProvider


@pytest_asyncio.fixture(scope="function")
async def session_maker(
) -> async_sessionmaker[AsyncSession]:
    # Ensure test database exists even if docker init scripts didn't create it yet.
    pg = settings.db.pg
    admin_conn = await asyncpg.connect(
        user=pg.user,
        password=pg.password.get_secret_value(),
        host=pg.host,
        port=pg.port,
        database="postgres",
    )
    try:
        exists = await admin_conn.fetchval(
            "SELECT 1 FROM pg_database WHERE datname=$1",
            pg.name,
        )
        if not exists:
            # CREATE DATABASE must not run inside a transaction block.
            await admin_conn.execute(f'CREATE DATABASE "{pg.name}"')
    finally:
        await admin_conn.close()

    target_conn = await asyncpg.connect(
        user=pg.user,
        password=pg.password.get_secret_value(),
        host=pg.host,
        port=pg.port,
        database=pg.name,
    )
    try:
        await target_conn.execute("CREATE EXTENSION IF NOT EXISTS citext")
        await target_conn.execute(f'CREATE SCHEMA IF NOT EXISTS "{pg.schema_name}"')
    finally:
        await target_conn.close()

    # Use application settings so tests work with your existing config.
    # (Avoid relying on non-existent POSTGRES_* env vars.)
    engine = create_async_engine(settings.db.async_url)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    maker = async_sessionmaker(
        bind=engine, class_=AsyncSession, autoflush=False, expire_on_commit=False
    )
    yield maker
    await engine.dispose()


@pytest_asyncio.fixture
async def session(
        session_maker: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession, Any]:
    async with session_maker() as session:
        session.commit = AsyncMock()
        yield session
        await session.rollback()


@pytest.fixture
def mock_provider(session: AsyncSession) -> Provider:
    class MockProvider(Provider):
        @provide(scope=Scope.REQUEST)
        async def get_session(self) -> AnyOf[AsyncSession, interfaces.TransactionManagerAsync]:
            return session

    return MockProvider()


@pytest.fixture
def container(mock_provider: Provider) -> AsyncContainer:
    return make_async_container(
        AppProvider(),
        mock_provider,
        context={},
    )
