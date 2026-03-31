
from collections.abc import AsyncGenerator

from dishka import Provider, Scope, provide, AnyOf
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    AsyncEngine,
)
from uuid_extensions import uuid7

from clean_backend.application.interactors import (
    GetUserInteractor,
    GetUsersInteractor,
    CreateUserInteractor,
    GetWalletInteractor,
    GetWalletsInteractor,
    CreateWalletInteractor, WalletOperationInteractor
)

from clean_backend.application.interfaces import (
    UUIDGenerator,
    TransactionManagerAsync,
    UserReader,
    UserSaver,
    UsersReader,
    WalletReader,
    WalletsReader,
    WalletSaver
)

from clean_backend.config.settings import settings
from clean_backend.infrastructure.db import (
    new_engine,
    new_session_maker)

from clean_backend.infrastructure.gateways import UserGateway, WalletGateway


class AppProvider(Provider):

    @provide(scope=Scope.APP)
    def get_uuid_generator(self) -> UUIDGenerator:
        return uuid7

    @provide(scope=Scope.APP)
    async def get_engine(self) -> AsyncGenerator[AsyncEngine]:
        engine = new_engine(settings.db)
        yield engine
        await engine.dispose()

    @provide(scope=Scope.APP)
    def get_session_maker(
        self,
        engine: AsyncEngine,
    ) -> async_sessionmaker[AsyncSession]:
        return new_session_maker(engine)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self,
        session_maker: async_sessionmaker[AsyncSession],
    ) -> AsyncGenerator[
        AnyOf[
            AsyncSession,
            TransactionManagerAsync,
        ]
    ]:
        async with session_maker() as session:
            yield session

    user_gateway = provide(
        UserGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[
            UserReader,
            UserSaver,
            UsersReader,
        ],
    )

    get_user_interactor = provide(
        GetUserInteractor,
        scope=Scope.REQUEST,
    )
    get_users_interactor = provide(
        GetUsersInteractor,
        scope=Scope.REQUEST,
    )
    create_new_user_interactor = provide(
        CreateUserInteractor,
        scope=Scope.REQUEST,
    )

    wallet_gateway = provide(
        WalletGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[
            WalletReader,
            WalletSaver,
            WalletsReader,
        ],
    )

    get_wallet_interactor = provide(
        GetWalletInteractor,
        scope=Scope.REQUEST,
    )
    get_wallets_interactor = provide(
        GetWalletsInteractor,
        scope=Scope.REQUEST,
    )
    create_new_wallet_interactor = provide(
        CreateWalletInteractor,
        scope=Scope.REQUEST,
    )

    wallet_operation_interactor = provide(
        WalletOperationInteractor,
        scope=Scope.REQUEST,
    )