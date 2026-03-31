from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from clean_backend.application.interfaces import UserReader, UserSaver, UsersReader
from clean_backend.domain.user import User, UserID
from clean_backend.infrastructure import models


class UserGateway(
    UserReader,
    UserSaver,
    UsersReader,
):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def read_by_uuid(
        self,
        uuid: UserID,
    ) -> User | None:
        user = await self._session.get(models.User, uuid)
        if user is None:
            return None
        return User(
            id=user.id,
            username=user.username,
        )

    async def read(self) -> list[User]:
        # TODO: ordering param later
        stmt = select(models.User).order_by(models.User.username)
        users = await self._session.scalars(stmt)
        return [
            User(
                id=user.id,
                username=user.username,
            )
            for user in users.all()
        ]

    async def save(self, user: User) -> None:
        user_model = models.User(
            id=user.id,
            username=user.username,
        )
        self._session.add(user_model)