from sqlalchemy import select, update, values, delete
from .BaseCRUD import BaseCRUD
from ..models.models import InventoryItem
from ..models.item_models import Items


class ItemsCRUD(BaseCRUD):

    async def update_inventory_item_quantity(self, inventory_id: int, item_id: int, quantity_delta: int):
        """Update the quantity of an item in the inventory"""
        update_statement = (
            update(InventoryItem)
            .where(
                InventoryItem.inventory_id == inventory_id,
                InventoryItem.item_id == item_id
            )
            .values(quantity=InventoryItem.quantity + quantity_delta)
            .returning(InventoryItem.quantity)
        )
        result = await self.session.execute(update_statement)
        new_quantity = result.scalar()
        if new_quantity <= 0:
            await self.delete_inventory_item(inventory_id, item_id)
        return new_quantity

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