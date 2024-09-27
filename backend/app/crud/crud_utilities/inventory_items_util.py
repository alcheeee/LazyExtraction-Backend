from typing import Optional
from enum import Enum
from app.models import (
    User,
    Inventory,
    InventoryItem,
    Stats,
    Items,
    Weapon,
    Bullets,
    Attachments
)


class AllowedArea(Enum):
    ANY = "any"
    STASH = "stash"
    INVENTORY = "inventory"



class InventoryItemsCRUDUtils:

    @staticmethod
    async def handle_inventory_change(
            inv_item: InventoryItem,
            allowed_area: AllowedArea,
            quantity_change: int
    ) -> tuple[int, int, float]:
        """
        Handles inventory changes and calculates weight change.

        :param inv_item: InventoryItem to modify
        :param allowed_area: Allowed area for changes
        :param quantity_change: The total change in quantity
        :return: Tuple of (new_inventory_amount, new_stash_amount, weight_change)
        """
        await InventoryItemsCRUDUtils.validate_inventory_change(inv_item, quantity_change)
        old_inventory = inv_item.amount_in_inventory
        old_stash = inv_item.amount_in_stash

        new_inventory, new_stash = await InventoryItemsCRUDUtils.amount_handler(
            inv_item, allowed_area, quantity_change
        )
        total_weight_change = InventoryItemsCRUDUtils.calculate_weight_change(
            inv_item.item.weight, (new_inventory - old_inventory) + (new_stash - old_stash)
        )
        return new_inventory, new_stash, total_weight_change


    @staticmethod
    async def amount_handler(
            inv_item: InventoryItem,
            allowed_area: AllowedArea,
            total_change: int

    ) -> tuple[int, int]:
        """
        Handles inventory amount changes based on where the quantity is allowed
        to be taken from.

        :param inv_item: InventoryItem to modify
        :param allowed_area: Allowed area for changes (ANY, STASH, or INVENTORY)
        :param total_change: The total change in quantity (positive for increase, negative for decrease)
        :return: Tuple (new_inventory_amount, new_stash_amount, weight_change)
        """
        inventory_amount: int = inv_item.amount_in_inventory
        stash_amount: int = inv_item.amount_in_stash

        match allowed_area:
            case allowed_area.ANY:
                if total_change > 0:
                    stash_amount += total_change
                else:
                    if stash_amount >= abs(total_change):
                        stash_amount += total_change
                    else:
                        remaining_change = total_change + stash_amount
                        stash_amount = 0
                        inventory_amount += remaining_change

            case allowed_area.STASH:
                stash_amount += total_change

            case allowed_area.INVENTORY:
                inventory_amount += total_change
            case _:
                raise Exception("Didn't specify allowed_area")

        if inventory_amount < 0 or stash_amount < 0:
            raise ValueError("Insufficient quantity available")

        return inventory_amount, stash_amount

    @staticmethod
    async def switch_item_location(
            inv_item: InventoryItem,
            to_stash: bool,
            quantity: int
    ) -> tuple[int, int]:
        """
        Switches item between Inventory and Stash

        :param inv_item: InventoryItem to modify
        :param to_stash: True if moving to stash, False if moving to inventory
        :param quantity: Amount to move
        :return: Tuple of (new_inventory_amount, new_stash_amount)
        """
        inventory_amount = inv_item.amount_in_inventory
        stash_amount = inv_item.amount_in_stash

        if to_stash:
            if inventory_amount < quantity:
                raise ValueError("Not enough quantity to switch")
            inventory_amount -= quantity
            stash_amount += quantity
        else:
            if stash_amount < quantity:
                raise ValueError("Not enough quantity in stash to move to inventory")
            stash_amount -= quantity
            inventory_amount += quantity

        if inventory_amount < 0 or stash_amount < 0:
            raise ValueError("Not enough quantity to switch")

        return inventory_amount, stash_amount

    @staticmethod
    async def validate_inventory_change(
            inv_item: InventoryItem,
            quantity_change: int
    ) -> None:
        total_quantity = inv_item.amount_in_stash + inv_item.amount_in_inventory
        new_total_quantity = total_quantity + quantity_change
        if new_total_quantity < 0:
            raise ValueError("Not enough quantity available")


    @staticmethod
    async def handle_modification(
            inv_item: InventoryItem,
            to_modify: bool
    ) -> tuple[InventoryItem | None, float]:
        """
        Handles the modification status change of an item.

        :param inv_item: The InventoryItem to modify
        :param to_modify: Whether to modify or unmodify the item
        :return: A new InventoryItem if modification status changed, None otherwise
        """
        if not to_modify:
            return None, 0

        weight_change = inv_item.item.weight

        if inv_item.amount_in_stash == 0:
            weight_change = -inv_item.item.weight

        original_modifications = inv_item.modifications if inv_item.modifications and to_modify else {}

        new_item = InventoryItem(
            item_name=inv_item.item_name,
            quick_sell_value=inv_item.quick_sell_value,
            inventory_id=inv_item.inventory_id,
            item_id=inv_item.item_id,
            is_modified=to_modify,
            modifications=original_modifications,
            amount_in_stash=1,
            amount_in_inventory=0
        )

        return new_item, weight_change


    @staticmethod
    def calculate_weight_change(weight: float, quantity_change: int) -> float:
        return weight * quantity_change


