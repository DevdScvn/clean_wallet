from abc import abstractmethod
from typing import Protocol

from clean_backend.domain.wallet import Wallet, WalletID


class WalletSaver(Protocol):
    @abstractmethod
    async def save(self, wallet: Wallet) -> None: ...


class WalletReader(Protocol):
    @abstractmethod
    async def read_by_uuid(self, uuid: WalletID) -> Wallet | None: ...

    @abstractmethod
    async def read_by_uuid_for_update(self, uuid: WalletID) -> Wallet | None: ...


class WalletsReader(Protocol):
    @abstractmethod
    async def read(self) -> list[Wallet]: ...
