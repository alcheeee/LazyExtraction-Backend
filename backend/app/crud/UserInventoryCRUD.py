from typing import Optional
from sqlalchemy import select, update, values, delete
from sqlalchemy.orm import joinedload
from .BaseCRUD import BaseCRUD
from ..models import (
    InventoryItem,
    Inventory,
    User
)


class UserInventoryCRUD(BaseCRUD):

    async def get_inventory_item_by_userid(self, user_id: int, item_id: int) -> InventoryItem:
        """
        :param user_id: User.id
        :param item_id: Items.id
        :return: Optional[InventoryItem instance]
        :raise ValueError
        """
        query = select(InventoryItem).join(Inventory).join(User).where(
            User.id == user_id,
            InventoryItem.item_id == item_id
        )
        result = (await self.session.execute(query)).scalars().first()
        if result is None:
            raise ValueError("You do not have that item")
        return result


    async def get_user_inventory_id_by_userid(self, user_id: int) -> Optional[int]:
        """
        :param User.id
        :return: Optional[User.Inventory.id]
        """
        query = select(Inventory.id).join(User).where(User.id == user_id)
        return await self.execute_scalar_one_or_none(query)


    async def get_user_bank_from_userid(self, user_id) -> Optional[int]:
        """
        :param user_id: User.id
        :return: (Inventory.id, Inventory.bank)
        :raise Exception
        """
        query = select(Inventory.id, Inventory.bank).join(
            User, User.inventory_id == Inventory.id
        ).where(
            User.id == user_id
        )
        result = await self.session.execute(query)
        inventory_details = result.first()
        if inventory_details is None:
            raise Exception("Failed to get user Inventory or Bank")
        return inventory_details


    async def update_bank_balance(self, inventory_id: int, new_balance: int):
        """
        :param inventory_id: Inventory.id
        :param new_balance: int
        :return: Updated Balance
        """
        update_ = update(Inventory).where(
            Inventory.id == inventory_id
        ).values(bank=new_balance)
        result = await self.session.execute(update_)
        return result


    async def update_bank_balance_by_username(self, username: str, balance_adjustment: int):
        """
        :param username: User.username
        :param balance_adjustment: int
        :return: New bank balace
        :raise Exception
        """
        subquery = select(Inventory.id, Inventory.bank).join(User).where(User.username == username).subquery()
        query = select(subquery.c.id, subquery.c.bank)
        result = await self.session.execute(query)
        inventory_id, current_bank_balance = result.first()

        if inventory_id is None:
            raise Exception("Failed to get user Inventory or Bank")

        # Calculate and update new balance
        new_bank_balance = current_bank_balance + balance_adjustment
        update_stmt = update(Inventory).where(
            Inventory.id == inventory_id
        ).values(bank=new_bank_balance)

        await self.session.execute(update_stmt)
        return new_bank_balance


    async def update_user_inventory_item(self, inventory_id: int, item_id: int, quantity_change: int, inventory_item: InventoryItem=None):
        """
        :param inventory_id: User.inventory_id
        :param item_id: Items.id
        :param quantity_change: int
        :param inventory_item: InventoryItem instance
        :return: New/Update/Delete InventoryItem instance
        :raise ValueError
        """
        if inventory_item is None:
            inventory_item = await self.get_inventory_item_by_userid(inventory_id, item_id)

        if inventory_item:
            if quantity_change < 0 and abs(quantity_change) > inventory_item.quantity:
                raise ValueError("Insufficient quantity to remove")

            inventory_item.quantity += quantity_change
            if inventory_item.quantity <= 0:
                await self.session.delete(inventory_item)
        else:
            if quantity_change <= 0:
                raise ValueError("Cannot add zero or negative quantity")
            new_inventory_item = InventoryItem(inventory_id=inventory_id, item_id=item_id, quantity=quantity_change)
            self.session.add(new_inventory_item)
        return inventory_item




