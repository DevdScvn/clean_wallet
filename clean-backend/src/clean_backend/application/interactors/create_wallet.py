from clean_backend.application.dto.wallet import NewWallet
from clean_backend.application.interfaces import TransactionManagerAsync, WalletSaver, UUIDGenerator
from clean_backend.domain.wallet import Wallet


class CreateWalletInteractor:
    def __init__(
        self,
        trx_manager: TransactionManagerAsync,
        wallet_saver: WalletSaver,
        uuid_generator: UUIDGenerator,
    ) -> None:
        self._trx_manager = trx_manager
        self._saver = wallet_saver
        self._generate_uuid = uuid_generator

    async def __call__(self, dto: NewWallet) -> Wallet:
        new_wallet = Wallet(
            id=self._generate_uuid(),
            balance=dto.balance,
            user_id=dto.user_id
        )
        await self._saver.save(new_wallet)
        await self._trx_manager.commit()
        return new_wallet
