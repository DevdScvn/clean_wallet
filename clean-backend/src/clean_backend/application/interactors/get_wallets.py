from clean_backend.application.interfaces import WalletsReader
from clean_backend.domain.wallet import Wallet


class GetWalletsInteractor:
    def __init__(
        self,
        reader: WalletsReader,
    ) -> None:
        self._reader = reader

    async def __call__(self) -> list[Wallet]:
        return await self._reader.read()