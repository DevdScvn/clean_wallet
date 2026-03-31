from fastapi import APIRouter

from .users import router as users_router
from .wallet import router as wallet_router

router = APIRouter(
    prefix="/v1",
    tags=["v1"],
)
router.include_router(users_router)
router.include_router(wallet_router)
