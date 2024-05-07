from sqlalchemy import select, update, values, delete
from .BaseCRUD import BaseCRUD
from ..models.models import InventoryItem, Inventory


class UserInventoryCRUD(BaseCRUD):

    async def update_user_inventory_item(self, inventory_id: int, item_id: int, quantity_change: int):
        """Add a new item to the inventory or update the quantity if it exists."""
        result = await self.session.execute(
            select(InventoryItem).where(
                InventoryItem.inventory_id == inventory_id,
                InventoryItem.item_id == item_id
            ))
        inventory_item = result.scalars().first()

        if inventory_item:
            if quantity_change < 0 and abs(quantity_change) > inventory_item.quantity:
                raise ValueError("Insufficient quantity to remove.")
            inventory_item.quantity += quantity_change
            if inventory_item.quantity <= 0:
                await self.delete_inventory_item(inventory_id, item_id)
        else:
            if quantity_change <= 0:
                raise ValueError("Cannot add zero or negative quantity.")
            new_inventory_item = InventoryItem(
                inventory_id=inventory_id,
                item_id=item_id,
                quantity=quantity_change
            )
            self.session.add(new_inventory_item)
        return inventory_item

    async def delete_inventory_item(self, inventory_id: int, item_id: int):
        """Delete an item from the inventory"""
        delete_statement = (
            delete(InventoryItem)
            .where(
                InventoryItem.inventory_id == inventory_id,
                InventoryItem.item_id == item_id
            )
        )
        await self.session.execute(delete_statement)