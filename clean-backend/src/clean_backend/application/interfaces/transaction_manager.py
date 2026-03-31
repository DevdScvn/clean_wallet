from abc import abstractmethod
from typing import Protocol


# class TransactionManagerSync(Protocol):
#     @abstractmethod
#     def commit(self) -> None: ...


class TransactionManagerAsync(Protocol):
    @abstractmethod
    async def commit(self) -> None: ...
