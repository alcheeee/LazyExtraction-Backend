from typing import Optional
from sqlalchemy import select, update, values
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import (
    Inventory,
    User
)


class UserBankingCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_bank_from_userid(self, user_id) -> tuple[int, int] | None:
        query = select(Inventory.id, Inventory.bank).join(
            User, User.inventory_id == Inventory.id  # type: ignore
        ).where(
            User.id == user_id
        )
        result = await self.session.execute(query)
        inventory_details = result.one_or_none()
        if inventory_details is None:
            raise LookupError("Failed to get user Inventory or Bank")
        return inventory_details  # type: ignore


    async def update_bank_balance(self, inventory_id: int, new_balance: int):
        update_bank = update(Inventory).where(  # type: ignore # noqa
            Inventory.id == inventory_id  # type: ignore
        ).values(bank=new_balance)
        result = await self.session.execute(update_bank)
        return result


    async def update_bank_balance_by_username(self, username: str, balance_adjustment: int):
        subquery = select(Inventory.id, Inventory.bank).join(User).where(User.username == username).subquery()  # type: ignore
        query = select(subquery.c.id, subquery.c.bank)
        result = await self.session.execute(query)
        details = result.one_or_none()
        if not details:
            raise LookupError("Failed to get user Inventory or Bank")

        inventory_id, current_bank_balance = details

        # Calculate and update new balance
        new_bank_balance = current_bank_balance + balance_adjustment
        update_stmt = update(Inventory).where(
            Inventory.id == inventory_id
        ).values(bank=new_bank_balance)

        await self.session.execute(update_stmt)
        return new_bank_balance

