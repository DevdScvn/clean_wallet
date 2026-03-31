from clean_backend.application.interfaces import WalletReader
from clean_backend.domain.wallet import Wallet, WalletID


class GetWalletInteractor:
    def __init__(
        self,
        reader: WalletReader,
    ) -> None:
        self._reader = reader

    async def __call__(self, uuid: WalletID) -> Wallet | None:
        return await self._reader.read_by_uuid(uuid)
