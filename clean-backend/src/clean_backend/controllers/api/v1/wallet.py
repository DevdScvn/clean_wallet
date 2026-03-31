from typing import Annotated
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status

from clean_backend.application.dto import NewWallet
from clean_backend.application.interactors import (
    CreateWalletInteractor,
    GetWalletInteractor,
    GetWalletsInteractor,
    WalletOperationInteractor, GetUserInteractor,
)
from clean_backend.controllers.schemas import (
    WalletCreate,
    WalletRead,
    WalletBalanceRead,
    WalletOperationBody,
)
from clean_backend.domain.wallet import InsufficientFundsError, Wallet

router = APIRouter(
    prefix="/wallets",
    tags=["wallets"],
    route_class=DishkaRoute,
)


def new_wallet_dep(wallet_create: WalletCreate) -> NewWallet:
    return NewWallet(
        balance=wallet_create.balance,
        user_id=wallet_create.user_id,
    )


@router.post(
    "/",
    response_model=WalletRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_wallet_view(
    new_wallet: Annotated[NewWallet, Depends(new_wallet_dep)],
    create_wallet: FromDishka[CreateWalletInteractor],
) -> Wallet:
    return await create_wallet(new_wallet)


@router.post(
    "/{wallet_id}/operation",
    response_model=WalletBalanceRead,
)
async def wallet_operation_view(
    wallet_id: Annotated[UUID, Path(...)],
    body: WalletOperationBody,
    operate: FromDishka[WalletOperationInteractor],
    get_user: FromDishka[GetUserInteractor],
) -> WalletBalanceRead:
    try:
        updated = await operate(wallet_id, body.operation_type, body.amount)
        user = await get_user(updated.user_id)
        if user is None:
            raise HTTPException(status_code=404, detail=f"User {updated.user_id} not found.")
        return WalletBalanceRead(balance=updated.balance, username=user.username)
    except LookupError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Wallet {wallet_id} not found.",
        ) from None
    except InsufficientFundsError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient funds for this withdrawal.",
        ) from None
    except ValueError as e:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e),
            ) from None


@router.get(
    "/{wallet_id}",
    response_model=WalletBalanceRead,
)
async def get_wallet_balance(
    wallet_id: Annotated[UUID, Path(description="Wallet UUID")],
    get_wallet: FromDishka[GetWalletInteractor],
    get_user: FromDishka[GetUserInteractor],
) -> WalletBalanceRead:
    wallet = await get_wallet(wallet_id)
    if wallet is None:
        raise HTTPException(status_code=404, detail=f"Wallet {wallet_id} not found.")

    user = await get_user(wallet.user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User {wallet.user_id} not found.")

    return WalletBalanceRead(balance=wallet.balance, username=user.username)


@router.get(
    "/{user_id}",
    response_model=WalletBalanceRead,
)
async def get_wallet_balance(
    user_id: Annotated[
        UUID,
        Path(description="User ID", title="User ID"),
    ],
    get_wallet: FromDishka[GetWalletInteractor],
    get_user: FromDishka[GetUserInteractor],
) -> WalletBalanceRead:
    wallet = await get_wallet(user_id)
    if wallet is None:
        raise HTTPException(status_code=404, detail=f"Wallet not found.")

    user = await get_user(wallet.user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User {wallet.user_id} not found.")

    return WalletBalanceRead(balance=wallet.balance, username=user.username)


@router.get(
    "/",
    response_model=list[WalletRead],
)
async def get_wallets_view(
    get_wallets: FromDishka[GetWalletsInteractor],
) -> list[Wallet]:
    return await get_wallets()
