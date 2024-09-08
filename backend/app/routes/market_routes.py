from fastapi import APIRouter, Depends
from ..game_systems.markets.market_handler import MarketTransactionHandler
from ..schemas import MarketTransactionRequest
from ..auth import current_user
from ..crud import MarketCRUD, UserCRUD
from . import (
    AsyncSession,
    get_db,
    ResponseBuilder,
    MyLogger,
    common_http_errors,
    exception_decorator
)

error_log = MyLogger.errors()
game_log = MyLogger.game()

market_router = APIRouter(
    prefix="/market",
    tags=["market"],
    responses={404: {"description": "Not Found"}}
)


@market_router.get("/")
async def root():
    return ResponseBuilder.success("Market routes ready")


@market_router.post("/market-transaction")
@exception_decorator
async def all_market_transactions(
        request: MarketTransactionRequest,
        user_id: int = Depends(current_user.ensure_user_exists),
        session: AsyncSession = Depends(get_db)
):
    user_in_raid = UserCRUD(None, session).get_user_field_from_id(user_id, 'in_raid')
    if user_in_raid:
        raise ValueError("Can't do that while in a raid")

    if request.amount <= 0:
        raise ValueError("Invalid amount")

    market_handler = MarketTransactionHandler(request, user_id, session)
    msg = await market_handler.market_transaction()

    await session.commit()
    game_log.info(msg)
    return ResponseBuilder.success(msg)



@market_router.get("/market-items-by-name")
async def get_market_items(
        item_name: str,
        offset: int = 0,
        user_id: int = Depends(current_user.ensure_user_exists),
        session: AsyncSession = Depends(get_db)
):
    market_crud = MarketCRUD(None, session)
    items = await market_crud.get_all_market_items_by_name(item_name, offset=offset)
    if not items:
        raise common_http_errors.mechanics_error("No items found")
    return items
