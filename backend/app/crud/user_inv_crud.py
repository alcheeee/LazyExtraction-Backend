from typing import Optional, List
from sqlalchemy import select, update, values, delete
from sqlalchemy.orm import joinedload, selectinload
from .base_crud import BaseCRUD
from ..models import (
    InventoryItem,
    Inventory,
    Stats,
    User,
    Items
)
from ..utils import RetryDecorators


class UserInventoryCRUD(BaseCRUD):

    @RetryDecorators.db_retry_decorator()
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

    @RetryDecorators.db_retry_decorator()
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

    @RetryDecorators.db_retry_decorator()
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

    @RetryDecorators.db_retry_decorator()
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

    @RetryDecorators.db_retry_decorator()
    async def switch_item_stash_status(self, user_id: int, item_id: int, to_stash: bool, quantity: int):
        """
        :param user_id: User.id
        :param item_id: InventoryItem.item_id
        :param to_stash: bool
        :param quantity: int
        :return: Updated InventoryItem instance
        """
        inventory_id = await self.get_user_inventory_id_by_userid(user_id)

        query = select(InventoryItem).where(
            InventoryItem.inventory_id == inventory_id,
            InventoryItem.item_id == item_id
        )

        inventory_item = (await self.session.execute(query)).scalars().first()

        if not inventory_item:
            raise ValueError("Item not found")

        if to_stash:
            to_stash_change = inventory_item.amount_in_stash + quantity
            from_inventory_change = inventory_item.amount_in_inventory - quantity

            if from_inventory_change <= 0 or to_stash_change <= 0:
                raise ValueError("Invalid amount")

            inventory_item.amount_in_stash = to_stash_change
            inventory_item.amount_in_inventory = from_inventory_change

            self.session.add(inventory_item)
        else:
            from_stash_change = inventory_item.amount_in_stash - quantity
            to_inventory_change = inventory_item.amount_in_inventory + quantity

            if to_inventory_change <= 0 or from_stash_change <= 0:
                raise ValueError("Invalid amount")

            inventory_item.amount_in_stash = from_stash_change
            inventory_item.amount_in_inventory = to_inventory_change

            self.session.add(inventory_item)

        return inventory_item

    @RetryDecorators.db_retry_decorator()
    async def update_user_inventory_item(self, inventory_id: int, item_id: int, quantity_change: int,
                                         inventory_item: InventoryItem = None, to_stash=True):
        """
        :param inventory_id: User.inventory_id
        :param item_id: Items.id
        :param quantity_change: int
        :param inventory_item: Optional[InventoryItem] instance
        :param to_stash: bool
        :return: New/Update/Delete InventoryItem instance
        :raise ValueError
        """
        if inventory_item is None:
            query = select(InventoryItem).join(Inventory).where(
                Inventory.id == inventory_id,
                InventoryItem.item_id == item_id
            )
            inventory_item = (await self.session.execute(query)).scalars().first()

        if inventory_item:
            amount_to_change = inventory_item.amount_in_stash if to_stash else inventory_item.amount_in_inventory
            if quantity_change < 0 and abs(quantity_change) > amount_to_change:
                raise ValueError("Insufficient quantity to remove")

            amount_to_change += quantity_change

        else:
            if quantity_change <= 0:
                raise ValueError("Cannot add zero or negative quantity")

            query_target = select(InventoryItem).join(Inventory).where(
                Inventory.id == inventory_id,
                InventoryItem.item_id == item_id
            )
            target_inventory_item = (await self.session.execute(query_target)).scalars().first()

            if target_inventory_item:
                amount_to_change = (
                    target_inventory_item.amount_in_stash
                    if to_stash else
                    target_inventory_item.amount_in_inventory
                )

                amount_to_change += quantity_change
                if to_stash:
                    inventory_item.amount_in_stash = amount_to_change
                else:
                    inventory_item.amount_in_inventory = amount_to_change

                self.session.add(target_inventory_item)
            else:
                new_inventory_item = InventoryItem(
                    inventory_id=inventory_id,
                    item_id=item_id
                )
                if to_stash:
                    new_inventory_item.amount_in_stash = quantity_change
                else:
                    new_inventory_item.amount_in_inventory = quantity_change

                self.session.add(new_inventory_item)

        return inventory_item

    @RetryDecorators.db_retry_decorator()
    async def get_inv_stats_invitem(self, user_id: int, item_id: int):
        try:
            result = await self.session.execute(
                select(
                    Inventory,
                    Stats,
                    InventoryItem
                ).select_from(User)
                .join(Inventory, User.inventory_id == Inventory.id)
                .join(InventoryItem, InventoryItem.inventory_id == Inventory.id)
                .join(Stats, User.stats_id == Stats.id)
                .where(User.id == user_id, InventoryItem.item_id == item_id)
                .options(
                    selectinload(InventoryItem.item).joinedload(Items.clothing_details),
                    selectinload(InventoryItem.item).joinedload(Items.weapon_details),
                    selectinload(InventoryItem.item).joinedload(Items.armor_details)
                )
            )
            inventory, stats, inventory_item = result.one()
            return inventory, stats, inventory_item

        except Exception as e:
            raise e

    @RetryDecorators.db_retry_decorator()
    async def get_all_items_by_inventory_id(self, inventory_id: int) -> List[InventoryItem]:
        """
        Fetch all inventory items by inventory ID, including item names.
        :param inventory_id: int
        :return: List of InventoryItem with item names
        """
        query = (
            select(InventoryItem)
            .options(joinedload(InventoryItem.item))  # Ensure item relationship is loaded
            .where(InventoryItem.inventory_id == inventory_id)
        )
        result = await self.session.execute(query)
        inventory_items = result.scalars().all()

        return inventory_items



