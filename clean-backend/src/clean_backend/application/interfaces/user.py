from abc import abstractmethod
from typing import Protocol

from clean_backend.domain.user import User, UserID


class UserSaver(Protocol):
    @abstractmethod
    async def save(self, user: User) -> None: ...


class UserReader(Protocol):
    @abstractmethod
    async def read_by_uuid(self, uuid: UserID) -> User | None: ...


class UsersReader(Protocol):
    @abstractmethod
    async def read(self) -> list[User]: ...
