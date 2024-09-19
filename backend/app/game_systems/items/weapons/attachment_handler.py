from typing import List, Dict
from sqlalchemy.ext.asyncio import AsyncSession

from ....crud import (
    UserInventoryCRUD,
    ItemsCRUD,
    WeaponCRUD
)
from ....models import (
    Items,
    InventoryItem,
    Weapon,
    Attachments
)
from ....schemas.weapon_schemas import (
    AttachmentTypes
)
from ..items_data.all_attachments import attachment_classes


class WeaponStatsHandler:
    def __init__(self, session: AsyncSession, user_id: int, weapon_inventory_id: int):
        self.session = session
        self.user_id = user_id
        self.weapon_inventory_id = weapon_inventory_id
        self.user_inventory_crud = UserInventoryCRUD(InventoryItem, session)
        self.items_crud = ItemsCRUD(Items, session)
        self.weapon_crud = WeaponCRUD(session)

    async def get_user_weapon(self) -> tuple[Items, InventoryItem]:
        weapon_item, weapon_inv_item = await self.weapon_crud.get_user_weapon(
            self.user_id, self.weapon_inventory_id
        )
        return weapon_item, weapon_inv_item


    async def apply_attachments(self, attachments_to_add: Dict[AttachmentTypes, str]):
        user_inv_id = await self.user_inventory_crud.get_user_inventory_id_by_userid(self.user_id)
        if user_inv_id is None:
            raise LookupError("Couldn't find users inventory id")

        weapon_item, weapon_inv_item = await self.get_user_weapon()
        current_attachments = weapon_inv_item.modifications.copy() or {}
        allowed_modifications = weapon_item.allowed_modifications

        if not weapon_inv_item.is_modified:
            new_item = await self.user_inventory_crud.update_any_inventory_quantity(
                self.user_id, 0, weapon_inv_item, to_modify=True
            )
            await self.user_inventory_crud.update_any_inventory_quantity(self.user_id, -1, weapon_inv_item)
            weapon_inv_item = new_item

        for attachment_type, attachment_name in attachments_to_add.items():
            if (attachment_type not in allowed_modifications or
                    attachment_name not in allowed_modifications[attachment_type]):
                raise ValueError(
                    f"A {attachment_name} can't go on the {attachment_type.value} slot"
                )

            if attachment_name in current_attachments.get(attachment_type, []):
                break

            attachment_item = await self.items_crud.get_item_from_name(attachment_name)
            if not attachment_item:
                raise LookupError(f"Attachment {attachment_name} not found")

            attachment_inv_item = await self.user_inventory_crud.get_inventory_item_by_item_id(
                user_inv_id, attachment_item.id
            )

            if (not attachment_inv_item or
                    attachment_inv_item.amount_in_inventory + attachment_inv_item.amount_in_stash <= 0):
                raise LookupError(f"You do not have {attachment_name} in inventory")

            await self.user_inventory_crud.update_any_inventory_quantity(self.user_id, -1, attachment_inv_item)

            if attachment_type in current_attachments:
                old_attachment_name = current_attachments[attachment_type]
                old_attachment_item = await self.items_crud.get_item_from_name(old_attachment_name)
                old_inventory_item = await self.user_inventory_crud.get_inventory_item_by_item_id(
                    user_inv_id, old_attachment_item.id
                )
                if old_inventory_item:
                    await self.user_inventory_crud.update_any_inventory_quantity(
                        self.user_id, 1, old_inventory_item, to_modify=old_inventory_item.is_modified
                    )
                else:
                    new_item = InventoryItem(
                        item_name=old_attachment_item.item_name,
                        quick_sell_value=old_attachment_item.quick_sell,
                        inventory_id=user_inv_id,
                        item_id=old_attachment_item.id,
                        is_modified=False,
                        modifications={},
                        amount_in_stash=0,
                        amount_in_inventory=0
                    )
                    self.session.add(new_item)
                    await self.user_inventory_crud.update_any_inventory_quantity(
                        self.user_id, 1, new_item
                    )

            current_attachments[attachment_type] = attachment_name

        weapon_inv_item.modifications = current_attachments
        await self.session.flush()
        return weapon_item, weapon_inv_item


    async def remove_attachments(
            self, attachments_to_remove: Dict[AttachmentTypes, str]
    ) -> tuple[Items, InventoryItem]:

        weapon_item, weapon_inv_item = await self.get_user_weapon()
        current_attachments: Dict = weapon_inv_item.modifications.copy() or {}
        user_inv_id: int = weapon_inv_item.inventory_id

        for attachment_type, attachment_name in attachments_to_remove.items():
            if attachment_name in current_attachments.get(attachment_type, []):

                attachment_item: Items | None = await self.items_crud.get_item_from_name(
                    attachment_name
                )
                if not attachment_item:
                    raise LookupError("Couldn't find that attachment")

                existing_item = await self.user_inventory_crud.get_inventory_item_by_item_id(
                    user_inv_id, attachment_item.id
                )
                if existing_item:
                    await self.user_inventory_crud.update_any_inventory_quantity(
                        self.user_id, 1, existing_item, to_modify=existing_item.is_modified
                    )
                else:
                    new_item = InventoryItem(
                        item_name=attachment_item.item_name,
                        quick_sell_value=attachment_item.quick_sell,
                        inventory_id=weapon_inv_item.inventory_id,
                        item_id=attachment_item.id,
                        is_modified=False,
                        modifications={},
                        amount_in_stash=0,
                        amount_in_inventory=0
                    )
                    self.session.add(new_item)
                    await self.session.flush()
                    await self.user_inventory_crud.update_any_inventory_quantity(
                        self.user_id, 1, new_item
                    )

                del current_attachments[attachment_type]
            else:
                raise ValueError(f"A {attachment_name} isn't in the {attachment_type.value} slot")

        weapon_inv_item.modifications = current_attachments
        weapon_inv_item.is_modified = bool(current_attachments)
        await self.session.flush()
        return weapon_item, weapon_inv_item


    @staticmethod
    def calculate_effective_stats(weapon: Weapon, modifications: Dict[AttachmentTypes, str]):
        effective_stats = {
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
                for stat, value in effective_stats.items():
                    adj_attr = f"{stat}_adj"
                    if hasattr(attachment_instance, adj_attr):
                        effective_stats[stat] += getattr(attachment_instance, adj_attr)

        return effective_stats
