from typing import Optional, List, Any, Sequence
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
from .crud_utilities.inventory_items_util import (
    InventoryItemsCRUDUtils as InvItemUtils,
    AllowedArea
)


class UserInventoryCRUD(BaseCRUD):

    async def get_inventory_item_by_userid(
            self, user_id: int, inventory_item_id: int
    ) -> InventoryItem | None:
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

    async def get_inventory_item_by_item_id(
            self, inventory_id: int, item_id: int
    ) -> Optional[InventoryItem]:
        """
        :param inventory_id: Inventory.id
        :param item_id: Items.id
        :return: InventoryItem or None
        """
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


    async def switch_item_stash_status(
            self, user_id: int, inventory_item_id: int, to_stash: bool, quantity: int
    ):
        inventory_item = await self.get_inventory_item_by_userid(user_id, inventory_item_id)
        if not inventory_item:
            raise LookupError("Item not found in inventory")

        await InvItemUtils.validate_inventory_change(
            inventory_item, quantity if to_stash else -quantity  # type: ignore
        )
        new_inventory_amount, new_stash_amount = await InvItemUtils.switch_item_location(
            inventory_item, to_stash, quantity  # type: ignore
        )
        inventory_item.amount_in_inventory = new_inventory_amount
        inventory_item.amount_in_stash = new_stash_amount

        weight_change = InvItemUtils.calculate_weight_change(
            inventory_item.item.weight, -quantity if to_stash else quantity  # type: ignore
        )
        stats_crud = StatsCRUD(self.session)
        await stats_crud.adjust_user_weight(user_id, weight_change)

        return inventory_item


    async def update_any_inventory_quantity(
            self,
            user_id: int,
            quantity_change: int,
            inventory_item: InventoryItem | None = None,
            to_modify: bool = False
    ) -> InventoryItem:
        """ Not to be used while user is in_raid """
        if not inventory_item:
            raise LookupError("Not inventory item found")

        total_weight_change = 0

        new_item, mod_weight_change = await InvItemUtils.handle_modification(inventory_item, to_modify)
        if new_item:
            self.session.add(new_item)
            total_weight_change += mod_weight_change
            await self.session.flush()
            inventory_item = new_item

        new_inventory, new_stash, change_weight_change = await InvItemUtils.handle_inventory_change(
            inventory_item, AllowedArea.ANY, quantity_change
        )

        inventory_item.amount_in_inventory = new_inventory
        inventory_item.amount_in_stash = new_stash
        total_weight_change += change_weight_change

        if total_weight_change != 0:
            stats_crud = StatsCRUD(self.session)
            await stats_crud.adjust_user_weight(user_id, total_weight_change)

        if new_inventory + new_stash == 0 and not inventory_item.one_equipped:
            await self.session.delete(inventory_item)
            return inventory_item

        await self.session.flush()
        return inventory_item


    async def update_user_inventory_item(
            self,
            user_id: int,
            item_id: int,
            quantity_change: int,
            to_stash=True
    ) -> InventoryItem | None:

        inventory_id = await self.get_user_inventory_id_by_userid(user_id)
        inventory_item: InventoryItem | None = await self.get_inventory_item_by_item_id(user_id, item_id)

        if not inventory_item:
            if quantity_change <= 0:
                raise ValueError("Cannot add zero or negative quantity for a new item")
            item = await self.session.get(Items, item_id)
            if not item:
                raise LookupError("Couldn't find that item")
            inventory_item = InventoryItem(
                item_name=item.item_name,
                quick_sell_value=item.quick_sell,
                inventory_id=inventory_id,
                item_id=item_id,
                is_modified=False
            )
            self.session.add(inventory_item)
            await self.session.flush()

        allowed_area = AllowedArea.STASH if to_stash else AllowedArea.INVENTORY
        total_weight_change = 0

        if inventory_item.is_modified and quantity_change < 0:
            raise ValueError("Cannot reduce quantity of modified items")

        new_inventory, new_stash, change_weight_change = await InvItemUtils.handle_inventory_change(
            inventory_item, allowed_area, quantity_change
        )

        inventory_item.amount_in_inventory = new_inventory
        inventory_item.amount_in_stash = new_stash
        total_weight_change += change_weight_change
        if total_weight_change != 0:
            stats_crud = StatsCRUD(self.session)
            await stats_crud.adjust_user_weight(inventory_id, total_weight_change)

        if new_inventory + new_stash == 0 and not inventory_item.one_equipped:
            await self.session.delete(inventory_item)
            return None

        await self.session.flush()
        return inventory_item

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
