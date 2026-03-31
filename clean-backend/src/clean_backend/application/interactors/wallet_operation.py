from decimal import Decimal

from clean_backend.application.interfaces import (
    TransactionManagerAsync,
    WalletReader,
    WalletSaver,
)
from clean_backend.domain.wallet import Wallet, WalletID
from clean_backend.domain.wallet_operation import WalletOperationType


class WalletOperationInteractor:
    def __init__(
        self,
        trx_manager: TransactionManagerAsync,
        reader: WalletReader,
        saver: WalletSaver,
    ) -> None:
        self._trx_manager = trx_manager
        self._reader = reader
        self._saver = saver

    async def __call__(
        self,
        wallet_id: WalletID,
        operation_type: WalletOperationType,
        amount: Decimal,
    ) -> Wallet:
        current = await self._reader.read_by_uuid_for_update(wallet_id)
        if current is None:
            msg = "Wallet not found"
            raise LookupError(msg)

        if operation_type is WalletOperationType.DEPOSIT:
            updated = current.deposit(amount)
        else:
            updated = current.withdraw(amount)

        await self._saver.save(updated)
        await self._trx_manager.commit()
        return updated