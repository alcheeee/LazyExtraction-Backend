from typing import List, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.concurrency import run_in_threadpool
from app.crud import (
    UserInventoryCRUD,
    ItemsCRUD,
    WeaponCRUD
)
from app.models import (
    Items,
    InventoryItem,
    Weapon,
    Attachments
)
from app.schemas.weapon_schemas import (
    AttachmentTypes
)
from ..items_data import attachment_classes


class WeaponAttachmentsHandler:
    def __init__(self, session: AsyncSession, user_id: int, weapon_inventory_id: int):
        self.session = session
        self.user_id = user_id
        self.inventory_id = None
        self.weapon_inventory_id = weapon_inventory_id
        self.user_inventory_crud = UserInventoryCRUD(InventoryItem, session)
        self.items_crud = ItemsCRUD(Items, session)
        self.weapon_crud = WeaponCRUD(session)
        self.weapon_item: Items = None  # type: ignore
        self.weapon_inv_item: InventoryItem = None  # type: ignore
        self.changed_items = {
            'new-inventory-items': [],
            'updated-inventory-items': []
        }

    def get_changes(self) -> Dict:
        return {
            'new-inventory-items': [item for item in self.changed_items['new-inventory-items']],
            'updated-inventory-items': [item for item in self.changed_items['updated-inventory-items']]
        }

    async def get_user_weapon(self) -> tuple[Items, InventoryItem]:
        user_inv_id = await self.user_inventory_crud.get_user_inventory_id_by_userid(self.user_id)
        if user_inv_id is None:
            raise LookupError("Couldn't find users inventory id")

        self.inventory_id = user_inv_id

        weapon_item, weapon_inv_item = await self.weapon_crud.get_user_weapon(
            self.inventory_id, self.weapon_inventory_id
        )
        self.weapon_item = weapon_item
        self.weapon_inv_item = weapon_inv_item
        return weapon_item, weapon_inv_item


    async def return_data(self) -> Dict:
        data = {
            "weapon": self.weapon_inv_item.dict(),
            "inventory-changes": self.get_changes()
        }
        weapon_stats = await run_in_threadpool(
            self.calculate_weapon_stats,
            self.weapon_item.weapon_details,
            self.weapon_inv_item.modifications  # type: ignore
        )
        data['weapon']['stats'] = weapon_stats
        return data

    async def build_weapon(
            self, attachments_to_add: Dict[AttachmentTypes, str]
    ) -> Dict:
        if not attachments_to_add.items():
            raise ValueError("Please select attachments to add")

        await self.get_user_weapon()

        if not self.weapon_inv_item.is_modified:
            new_item, original_item = await self.weapon_crud.update_weapon_for_attachments(
                self.user_id, self.weapon_inv_item
            )
            self.weapon_inv_item = new_item
            self.changed_items['updated-inventory-items'].append(original_item)
            self.changed_items['new-inventory-items'].append(new_item)

        current_attachments = await self.apply_attachments(attachments_to_add)
        self.weapon_inv_item.modifications = current_attachments
        await self.session.flush()
        return await self.return_data()


    async def apply_attachments(
            self, attachments_to_add: Dict[AttachmentTypes, str]
    ) -> Dict[AttachmentTypes, str]:
        current_attachments = self.weapon_inv_item.modifications.copy() or {}
        allowed_modifications = self.weapon_item.allowed_modifications

        for attachment_type, attachment_name in attachments_to_add.items():
            await self._validate_attachment(  # Check if attachment can go on that weapon
                attachment_type, attachment_name, allowed_modifications  # type: ignore
            )
            if attachment_name in current_attachments.get(attachment_type, []):
                break

            # Checks for and updates/removes InventoryItem attachment
            attachment_item = await self._get_and_validate_attachment_item(attachment_name)
            attachment_inv_item = await self._get_and_validate_inventory_item(attachment_item)
            await self._update_inventory(attachment_inv_item, -1)

            if attachment_type in current_attachments:  # Removes same type attachment and adds new one
                await self._handle_existing_attachment(attachment_type, current_attachments)

            current_attachments[attachment_type] = attachment_name
        return current_attachments


    async def remove_attachments(
            self, attachments_to_remove: Dict[AttachmentTypes, str]
    ) -> Dict:
        if not attachments_to_remove.items():
            raise ValueError("Please select attachments to add")

        await self.get_user_weapon()
        current_attachments = self.weapon_inv_item.modifications.copy() or {}

        for attachment_type, attachment_name in attachments_to_remove.items():
            await self._validate_attachment_removal(attachment_type, attachment_name, current_attachments)
            attachment_item = await self._get_and_validate_attachment_item(attachment_name)
            await self._handle_attachment_removal(attachment_item)
            del current_attachments[attachment_type]

        self.weapon_inv_item.modifications = current_attachments
        self.weapon_inv_item.is_modified = bool(current_attachments)
        await self.session.flush()
        return await self.return_data()


    @staticmethod
    async def _validate_attachment_removal(
            attachment_type: AttachmentTypes,
            attachment_name: str,
            current_attachments: Dict[AttachmentTypes, str]
    ) -> None:
        if attachment_name not in current_attachments.get(attachment_type, []):
            raise ValueError(f"A {attachment_name} isn't in the {attachment_type.value} slot")


    @staticmethod
    async def _validate_attachment(
            attachment_type: AttachmentTypes,
            attachment_name: str,
            allowed_modifications: Dict[AttachmentTypes, str]
    ) -> None:
        if (attachment_type not in allowed_modifications or
                attachment_name not in allowed_modifications[attachment_type]):
            raise ValueError(f"A {attachment_name} can't go on the {attachment_type.value} slot")


    async def _handle_attachment_removal(self, attachment_item: Items) -> None:
        existing_item = await self.user_inventory_crud.get_inventory_item_by_item_id(
            self.inventory_id, attachment_item.id
        )
        if existing_item:
            await self._update_inventory(existing_item, 1)
        else:
            await self._create_new_inventory_item(attachment_item)


    async def _get_and_validate_attachment_item(self, attachment_name: str) -> Items:
        attachment_item = await self.items_crud.get_item_from_name(attachment_name)
        if not attachment_item:
            raise LookupError(f"Attachment {attachment_name} not found")
        return attachment_item


    async def _get_and_validate_inventory_item(self, attachment_item: Items) -> InventoryItem:
        attachment_inv_item = await self.user_inventory_crud.get_inventory_item_by_item_id(
            self.inventory_id, attachment_item.id
        )
        if (not attachment_inv_item or
                attachment_inv_item.amount_in_inventory + attachment_inv_item.amount_in_stash <= 0):
            raise LookupError(f"You do not have {attachment_item.item_name} in inventory")
        return attachment_inv_item


    async def _update_inventory(self, inventory_item: InventoryItem, quantity: int) -> None:
        await self.user_inventory_crud.update_any_inventory_quantity(self.user_id, quantity, inventory_item)
        self.changed_items['updated-inventory-items'].append(inventory_item)

    async def _handle_existing_attachment(
            self,
            attachment_type: AttachmentTypes,
            current_attachments: Dict[AttachmentTypes, str]
    ) -> None:
        old_attachment_name = current_attachments[attachment_type]
        old_attachment_item = await self.items_crud.get_item_from_name(old_attachment_name)
        old_inventory_item = await self.user_inventory_crud.get_inventory_item_by_item_id(
            self.inventory_id, old_attachment_item.id
        )

        if old_inventory_item:
            await self._update_inventory(old_inventory_item, 1)
        else:
            await self._create_new_inventory_item(old_attachment_item)

    async def _create_new_inventory_item(self, attachment_item: Items) -> InventoryItem:
        new_item = InventoryItem(
            item_name=attachment_item.item_name,
            quick_sell_value=attachment_item.quick_sell,
            inventory_id=self.inventory_id,
            item_id=attachment_item.id,
            is_modified=False,
            modifications={},
            amount_in_stash=1,
            amount_in_inventory=0
        )
        self.session.add(new_item)
        self.changed_items['new-inventory-items'].append(new_item)
        return new_item


    @staticmethod
    def calculate_weapon_stats(
            weapon: Weapon,
            modifications: Dict[AttachmentTypes, str]
    ) -> Dict[str, int | float]:
        calculated_stats = {
            "damage": weapon.damage,
            "range": weapon.range,
            "accuracy": weapon.accuracy,
            "reload_speed": weapon.reload_speed,
            "fire_rate": weapon.fire_rate,
            "magazine_size": weapon.magazine_size,
            "armor_penetration": weapon.armor_penetration,
            "headshot_chance": weapon.headshot_chance,
            "agility_adj": weapon.agility_adj,
        }

        attachment_instance_map = {cls().item_name: cls() for cls in attachment_classes}

        for attachment_type, attachment_name in modifications.items():
            attachment_instance = attachment_instance_map.get(attachment_name)
            if attachment_instance:
                for stat, value in calculated_stats.items():
                    adj_attr = f"{stat}_adj"
                    if hasattr(attachment_instance, adj_attr):
                        calculated_stats[stat] += getattr(attachment_instance, adj_attr)

        return calculated_stats
