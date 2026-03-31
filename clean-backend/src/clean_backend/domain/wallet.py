from dataclasses import dataclass, replace
from decimal import Decimal
from uuid import UUID

from clean_backend.domain.user import UserID

type WalletID = UUID


class InsufficientFundsError(Exception):
    """Withdrawal would make the wallet balance negative."""


@dataclass(frozen=True, slots=True)
class Wallet:
    id: WalletID
    balance: Decimal
    user_id: UserID


    def deposit(self, amount: Decimal):
        if amount <= 0:
            msg = "Amount must be positive"
            raise ValueError(msg)
        return replace(self, balance=self.balance + amount)

    def withdraw(self, amount: Decimal):
        if amount <= 0:
            msg = "Amount must be positive"
            raise ValueError(msg)
        new_balance = self.balance - amount
        if new_balance < 0:
            raise InsufficientFundsError
        return replace(self, balance=new_balance)