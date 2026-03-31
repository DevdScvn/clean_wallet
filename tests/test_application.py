from unittest.mock import create_autospec, MagicMock
from uuid import uuid4

import pytest

from faker import Faker

from clean_backend.application import interfaces
from clean_backend.application.dto import NewUser
from clean_backend.application.interactors import GetUserInteractor, CreateUserInteractor
from clean_backend.domain.user import User


@pytest.fixture
def get_user_interactor() -> GetUserInteractor:
    user_gateway = create_autospec(interfaces.UserReader)
    return GetUserInteractor(user_gateway)


@pytest.mark.asyncio
@pytest.mark.parametrize("uuid", [str(uuid4()), str(uuid4())])
async def test_get_user(get_user_interactor: GetUserInteractor, uuid: str) -> None:
    result = await get_user_interactor(uuid=uuid)
    # GetUserInteractor передает uuid позиционно, поэтому проверяем без именованных аргументов
    get_user_interactor._reader.read_by_uuid.assert_awaited_once_with(uuid)
    assert result == get_user_interactor._reader.read_by_uuid.return_value


@pytest.fixture
def new_user_interactor(faker: Faker) -> CreateUserInteractor:
    trx_manager = create_autospec(interfaces.TransactionManagerAsync)
    user_gateway = create_autospec(interfaces.UserSaver)
    uuid_generator = MagicMock(return_value=faker.uuid4())
    return CreateUserInteractor(trx_manager, user_gateway, uuid_generator)


@pytest.mark.asyncio
async def test_new_book_interactor(
    new_user_interactor: CreateUserInteractor, faker: Faker
) -> None:
    dto = NewUser(
        username=faker.pystr(),
    )
    result = await new_user_interactor(dto=dto)
    generated_uuid = new_user_interactor._generate_uuid.return_value
    new_user_interactor._saver.save.assert_awaited_with(
        User(
            id=generated_uuid,
            username=dto.username,
        )
    )
    new_user_interactor._trx_manager.commit.assert_awaited_once()
    assert result == User(id=generated_uuid, username=dto.username)
