from sqlmodel import select
from fastapi import APIRouter, HTTPException, Depends

from ..models.models import User, InventoryItem
from ..auth.auth_handler import current_user
from ..models.item_models import Items

from ..game_systems.markets.MarketHandler import MarketTransactionHandler
from ..schemas.market_schema import MarketTransactionRequest
from ..database.UserHandler import UserHandler

from . import dependency_session, ResponseBuilder, DataName, MyLogger, common_http_errors, AsyncSession
error_log = MyLogger.errors()
game_log = MyLogger.game()


market_router = APIRouter(
    prefix="/market",
    tags=["market"],
    responses={404: {"description": "Not Found"}}
)


@market_router.post("/market-transaction")
async def all_market_transactions(
        request: MarketTransactionRequest,
        user_id: int = Depends(current_user.ensure_user_exists),
        session: AsyncSession = Depends(dependency_session)
    ):
    try:
        if request.amount <= 0:
            raise ValueError("Invalid amount")

        market_handler = MarketTransactionHandler(request, user_id, session)
        msg = await market_handler.market_transaction()

        await session.commit()
        game_log.info(msg)
        return ResponseBuilder.success(msg)

    except ValueError as e:
        await session.rollback()
        return ResponseBuilder.error(str(e))

    except Exception as e:
        await session.rollback()
        error_log.error(str(e))
        raise common_http_errors.server_error()

