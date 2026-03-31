from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from clean_backend.application.interfaces import WalletReader, WalletsReader, WalletSaver
from clean_backend.domain.wallet import Wallet, WalletID
from clean_backend.infrastructure import models


class WalletGateway(
    WalletReader,
    WalletSaver,
    WalletsReader,
):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def read_by_uuid(
        self,
        uuid: WalletID,
    ) -> Wallet | None:
        wallet = await self._session.get(models.Wallet, uuid)
        if wallet is None:
            return None
        return Wallet(
            id=wallet.id,
            balance=wallet.balance,
            user_id=wallet.user_id
        )

    async def read(self) -> list[Wallet]:
        stmt = select(models.Wallet).order_by(models.Wallet.id)
        wallets = await self._session.scalars(stmt)
        return [
            Wallet(
                id=wallet.id,
                balance=wallet.balance,
                user_id=wallet.user_id
            )
            for wallet in wallets.all()
        ]

    # async def save(self, wallet: Wallet) -> None:
    #     wallet_model = models.Wallet(
    #         id=wallet.id,
    #         balance=wallet.balance,
    #         user_id=wallet.user_id,
    #     )
    #     self._session.add(wallet_model)

    async def read_by_uuid_for_update(
            self,
            uuid: WalletID,
    ) -> Wallet | None:
        stmt = (
            select(models.Wallet)
            .where(models.Wallet.id == uuid)
            .with_for_update()
        )
        result = await self._session.execute(stmt)
        row = result.scalar_one_or_none()
        if row is None:
            return None
        return Wallet(
            id=row.id,
            balance=Decimal(row.balance),
            user_id=row.user_id,
        )

    async def save(self, wallet: Wallet) -> None:
        existing = await self._session.get(models.Wallet, wallet.id)
        if existing is None:
            self._session.add(
                models.Wallet(
                    id=wallet.id,
                    balance=wallet.balance,
                    user_id=wallet.user_id,
                )
            )
        else:
            existing.balance = wallet.balance
            existing.user_id = wallet.user_id