from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field

from clean_backend.domain.wallet_operation import WalletOperationType


class WalletBase(BaseModel):
    balance: Decimal = Field(
        default=Decimal("0.00"),

        exclude=True,
        # examples=[Decimal("1000.00")],  # или examples=["1000.00"]
        description="Баланс (денежная сумма)",
    )
    user_id: UUID


class WalletCreate(WalletBase):
    ...


class WalletRead(WalletBase):
    id: UUID


class WalletBalanceRead(BaseModel):
    balance: Decimal = Field(
        ...,
        examples=[Decimal("1000.00")],
        description="Баланс (денежная сумма)",
    )
    username: str = Field(examples=["nikita"])


class WalletOperationBody(BaseModel):
    operation_type: WalletOperationType
    amount: Decimal = Field(gt=0)






