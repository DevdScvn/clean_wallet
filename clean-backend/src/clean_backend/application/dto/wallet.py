from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass(slots=True)
class NewWallet:
    balance: Decimal
    user_id: UUID
