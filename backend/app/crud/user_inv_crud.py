from typing import Optional, List, Union, Any, Sequence
from sqlalchemy import select, update, values, delete, Row, RowMapping
from sqlalchemy.orm import joinedload, selectinload
from .base_crud import BaseCRUD
from .stats_crud import StatsCRUD
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
    async def get_inventory_item_by_userid(
            self, user_id: int, inventory_item_id: int
    ) -> Union[InventoryItem, None]:
        """
        :param user_id: User.id
        :param inventory_item_id: InventoryItem.id
        :return: Optional[InventoryItem instance]
        :raise ValueError
        """
        query = select(InventoryItem).join(Inventory).join(User).where(
            User.id == user_id,  # type: ignore
            InventoryItem.id == inventory_item_id  # type: ignore
        )
        result = (await self.session.execute(query)).scalars().first()
        return result


    @RetryDecorators.db_retry_decorator()
    async def get_inventory_item_by_item_id(
            self, inventory_id: int, item_id: int
    ) -> Optional[InventoryItem]:
        """
        :param inventory_id: Inventory.id
        :param item_id: Items.id
        :return: InventoryItem or None
        """
        # TODO : Change to InventoryItem
        query = select(InventoryItem).where(
            InventoryItem.inventory_id == inventory_id,  # type: ignore
            InventoryItem.item_id == item_id  # type: ignore
        )
        result = (await self.session.execute(query)).scalars().first()
        return result


    async def get_user_inventory_id_by_userid(self, user_id: int) -> Optional[int]:
        """
        :param user_id:int = User.id
        :return: Optional[User.Inventory.id]
        """
        query = select(Inventory.id).join(User).where(User.id == user_id)  # type: ignore
        return await self.execute_scalar_one_or_none(query)

    @RetryDecorators.db_retry_decorator()
    async def get_user_bank_from_userid(self, user_id) -> Optional[int]:
        """
        :param user_id: User.id
        :return: (Inventory.id, Inventory.bank)
        :raise LookupError
        """
        query = select(Inventory.id, Inventory.bank).join(
            User, User.inventory_id == Inventory.id  # type: ignore
        ).where(
            User.id == user_id
        )
        result = await self.session.execute(query)
        inventory_details = result.first()
        if inventory_details is None:
            raise LookupError("Failed to get user Inventory or Bank")
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
        :raise LookupError
        """
        subquery = select(Inventory.id, Inventory.bank).join(User).where(User.username == username).subquery()  # type: ignore
        query = select(subquery.c.id, subquery.c.bank)
        result = await self.session.execute(query)
        inventory_id, current_bank_balance = result.first()

        if inventory_id is None:
            raise LookupError("Failed to get user Inventory or Bank")

        # Calculate and update new balance
        new_bank_balance = current_bank_balance + balance_adjustment
        update_stmt = update(Inventory).where(
            Inventory.id == inventory_id
        ).values(bank=new_bank_balance)

        await self.session.execute(update_stmt)
        return new_bank_balance

    @RetryDecorators.db_retry_decorator()
    async def switch_item_stash_status(self, user_id: int, inventory_item_id: int, to_stash: bool, quantity: int):
        """
        :param user_id: User.id
        :param inventory_item_id: InventoryItem.id
        :param to_stash: bool
        :param quantity: int
        :return: Updated InventoryItem instance
        """
        from_inventory_change = None
        to_inventory_change = None
        to_stash_change = None
        from_stash_change = None

        inventory_id = await self.get_user_inventory_id_by_userid(user_id)
        inventory_item = await self.session.get(InventoryItem, inventory_item_id)

        if not inventory_item or inventory_item.inventory_id != inventory_id:
            raise LookupError("Item not found in inventory")

        stats_crud = StatsCRUD(self.session)
        weight_change = inventory_item.item.weight * quantity

        if to_stash:
            to_stash_change = inventory_item.amount_in_stash + quantity
            from_inventory_change = inventory_item.amount_in_inventory - quantity
            await stats_crud.adjust_user_weight(user_id, -weight_change)
        else:
            from_stash_change = inventory_item.amount_in_stash - quantity
            to_inventory_change = inventory_item.amount_in_inventory + quantity
            await stats_crud.adjust_user_weight(user_id, +weight_change)

        if to_stash and (from_inventory_change < 0 or to_stash_change < 0):
            raise ValueError("Invalid amount")

        elif not to_stash and (to_inventory_change < 0 or from_stash_change < 0):
            raise ValueError("Invalid amount")

        if to_stash:
            inventory_item.amount_in_stash = to_stash_change
            inventory_item.amount_in_inventory = from_inventory_change
        else:
            inventory_item.amount_in_stash = from_stash_change
            inventory_item.amount_in_inventory = to_inventory_change

        return inventory_item


    @RetryDecorators.db_retry_decorator()
    async def update_any_inventory_quantity(
            self,
            user_id: int,
            quantity_change: int,
            inventory_item: Union[InventoryItem, None] = None,
            to_modify: bool = False
    ) -> InventoryItem:
        """
        Not to be used while user is in_raid
        :param user_id:
        :param quantity_change: int
        :param inventory_item: Optional[InventoryItem] instance
        :param to_modify: bool
        :return: New/Update/Delete InventoryItem instance, stash or inventory
        :raise ValueError
        """
        if not inventory_item:
            raise LookupError("Not inventory item found")

        if not inventory_item.is_modified and to_modify:
            new_item = InventoryItem(
                item_name=inventory_item.item_name,
                quick_sell_value=inventory_item.quick_sell_value,
                inventory_id=inventory_item.inventory_id,
                item_id=inventory_item.item_id,
                is_modified=True,
                modifications={},
                amount_in_stash=1,
                amount_in_inventory=0
            )
            self.session.add(new_item)
            await self.session.flush()
            return new_item

        if inventory_item.is_modified and not to_modify:
            # Create new InventoryItem for modified items
            new_item = InventoryItem(
                item_name=inventory_item.item_name,
                quick_sell_value=inventory_item.quick_sell_value,
                inventory_id=inventory_item.inventory_id,
                item_id=inventory_item.item_id,
                is_modified=True,
                modifications=inventory_item.modifications.copy(),
                amount_in_stash=1,
                amount_in_inventory=0
            )
            self.session.add(new_item)
            await self.session.flush()
            return new_item

        total_quantity = inventory_item.amount_in_stash + inventory_item.amount_in_inventory
        new_total_quantity = total_quantity + quantity_change
        if new_total_quantity < 0:
            raise ValueError("Insufficient quantity available")

        if new_total_quantity == 0:
            await self.session.delete(inventory_item)
            return inventory_item

        if quantity_change > 0 and inventory_item.amount_in_stash > 0:
            inventory_item.amount_in_stash += quantity_change
        else:
            if inventory_item.amount_in_stash >= abs(quantity_change):
                inventory_item.amount_in_stash += quantity_change
            else:
                remaining_change = quantity_change + inventory_item.amount_in_stash
                inventory_item.amount_in_stash = 0
                inventory_item.amount_in_inventory += remaining_change

                stats_crud = StatsCRUD(self.session)
                weight_change = inventory_item.item.weight * remaining_change
                await stats_crud.adjust_user_weight(user_id, weight_change)

        await self.session.flush()
        return inventory_item


    @RetryDecorators.db_retry_decorator()
    async def update_user_inventory_item(
            self,
            inventory_id: int,
            item_id: int,
            quantity_change: int,
            to_stash=True
    ) -> Union[InventoryItem, None]:
        """
        :param inventory_id: User.inventory_id
        :param item_id: Items.id
        :param quantity_change: int
        :param inventory_item: Optional[InventoryItem] instance
        :param to_stash: bool
        :return: New/Updated InventoryItem instance, or None if deleted
        :raise ValueError
        """
        query = select(InventoryItem).options(joinedload(InventoryItem.item)).where(
            InventoryItem.inventory_id == inventory_id,  # type: ignore
            InventoryItem.item_id == item_id  # type: ignore
        )
        inventory_item = (await self.session.execute(query)).scalars().first()

        stats_crud = StatsCRUD(self.session)

        if inventory_item:
            if not inventory_item.item.can_be_modified or not inventory_item.is_modified:
                amount_to_change = inventory_item.amount_in_stash if to_stash else inventory_item.amount_in_inventory
                if quantity_change < 0 and abs(quantity_change) > amount_to_change:
                    raise ValueError("Insufficient quantity available")
                if to_stash:
                    inventory_item.amount_in_stash += quantity_change
                    weight_change = -inventory_item.item.weight * quantity_change
                else:
                    inventory_item.amount_in_inventory += quantity_change
                    weight_change = inventory_item.item.weight * quantity_change

                await stats_crud.adjust_user_weight(inventory_id, weight_change)
                if inventory_item.amount_in_stash <= 0 and inventory_item.amount_in_inventory <= 0:
                    await self.session.delete(inventory_item)

                return inventory_item
            else:
                if quantity_change < 0:
                    raise ValueError("Cannot reduce quantity of modified items")

                item = await self.session.get(Items, item_id)
                if item is None:
                    raise LookupError("Couldn't find that item")

                new_inventory_item = InventoryItem(
                    item_name=item.item_name,
                    quick_sell_value=inventory_item.quick_sell_value,
                    inventory_id=inventory_id,
                    item_id=item_id,
                    is_modified=True,
                    modifications=inventory_item.modifications.copy() if inventory_item.modifications else {}
                )
                if to_stash:
                    new_inventory_item.amount_in_stash = 1
                else:
                    new_inventory_item.amount_in_inventory = 1
                    await stats_crud.adjust_user_weight(inventory_id, item.weight)

                self.session.add(new_inventory_item)
                return new_inventory_item
        else:
            if quantity_change <= 0:
                raise ValueError("Cannot add zero or negative quantity")

            item = await self.session.get(Items, item_id)
            if item is None:
                raise LookupError("Couldn't find that item")

            new_inventory_item = InventoryItem(
                item_name=item.item_name,
                quick_sell_value=item.quick_sell,
                inventory_id=inventory_id,
                item_id=item_id,
                is_modified=False
            )
            if to_stash:
                new_inventory_item.amount_in_stash = quantity_change
            else:
                new_inventory_item.amount_in_inventory = quantity_change
                await stats_crud.adjust_user_weight(inventory_id, item.weight * quantity_change)

            self.session.add(new_inventory_item)
            return new_inventory_item


    async def get_inv_stats_invitem(self, user_id: int, inventory_item_id: int):
        result = await self.session.execute(
            select(Inventory, Stats, InventoryItem).select_from(User)
            .join(Inventory, User.inventory_id == Inventory.id)  # type: ignore
            .join(InventoryItem, InventoryItem.inventory_id == Inventory.id)
            .join(Stats, User.stats_id == Stats.id)
            .where(User.id == user_id, InventoryItem.id == inventory_item_id)
            .options(
                selectinload(InventoryItem.item).joinedload(Items.clothing_details),  # type: ignore
                selectinload(InventoryItem.item).joinedload(Items.weapon_details),  # type: ignore
                selectinload(InventoryItem.item).joinedload(Items.armor_details)  # type: ignore
            )
        )
        inventory, stats, inventory_item = result.one_or_none()
        return inventory, stats, inventory_item


    @RetryDecorators.db_retry_decorator()
    async def get_all_items_by_inventory_id(self, inventory_id: int) -> Sequence[Row[Any] | RowMapping | Any]:
        """
        Fetch all inventory items by inventory ID, including item names.
        :param inventory_id: int
        :return: List of InventoryItem with item names
        """
        query = (
            select(InventoryItem)
            .options(joinedload(InventoryItem.item))
            .where(InventoryItem.inventory_id == inventory_id)  # type: ignore
        )

        result = await self.session.execute(query)
        return result.unique().scalars().all()
