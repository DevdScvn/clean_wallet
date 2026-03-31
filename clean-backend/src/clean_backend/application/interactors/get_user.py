from clean_backend.application.interfaces import UserReader
from clean_backend.domain.user import User, UserID


class GetUserInteractor:
    def __init__(
        self,
        reader: UserReader,
    ) -> None:
        self._reader = reader

    async def __call__(self, uuid: UserID) -> User | None:
        return await self._reader.read_by_uuid(uuid)
