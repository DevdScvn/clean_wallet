import uuid
from decimal import Decimal

from sqlalchemy import UUID, func, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Wallet(Base):
    __tablename__ = "wallets"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.uuidv7(),
    )
    balance: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    