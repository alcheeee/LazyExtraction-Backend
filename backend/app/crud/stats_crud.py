from typing import Dict, Union
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import (
    User,
    Inventory,
    InventoryItem,
    Stats,
    Items,
    Weapon,
    Bullets,
    Attachments,
    MarketItems
)


class StatsCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def adjust_user_weight(self, user_id: int, weight_change: float):
        query = select(Inventory.current_weight).join(User).where(User.id == user_id)  # type: ignore
        result = await self.session.execute(query)
        current_weight = result.scalar_one_or_none()

        if current_weight is None:
            raise LookupError("No inventory found for user")

        new_weight = round(max(current_weight + weight_change, 0), 2)

        update_stmt = (
            update(Inventory)
            .where(Inventory.id == User.inventory_id)  # type: ignore
            .where(User.id == user_id)
            .values(current_weight=new_weight)
        )
        await self.session.execute(update_stmt)
        await self.session.flush()
        return new_weight


    async def adjust_user_stats(self, user_id: int, stat_adjustments: Dict[str, Union[int, float]]):
        query = select(Stats).join(User).where(User.id == user_id)  # type: ignore
        result = await self.session.execute(query)
        stats: Stats = result.scalar_one_or_none()

        if not stats:
            raise LookupError(f"Stats not found for user_id: {user_id}")

        for stat_name, adjustment in stat_adjustments.items():
            if hasattr(stats, stat_name):
                current_value = getattr(stats, stat_name)
                new_value = current_value + adjustment
                setattr(stats, stat_name, new_value)
            else:
                raise ValueError(f"Invalid stat name: {stat_name}")

        await stats.round_stats()
        await self.session.flush()
        return stats
