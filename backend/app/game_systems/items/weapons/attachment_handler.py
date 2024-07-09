import json
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from ....crud import UserInventoryCRUD, ItemsCRUD
from ..items_data.all_attachments import attachment_items


class AttachmentsHandler:
    def __init__(self, user_id: int, session: AsyncSession):
        self.allowed_attachments = None
        self.attachments = None
        self.session = session
        self.user_id = user_id
        self.inv_crud = UserInventoryCRUD(None, session)
        self.item_crud = ItemsCRUD(None, session)

    async def add_attachment(self, weapon, attachment_name: str):
        attachment_id = await self.item_crud.check_item_exists(attachment_name)

        # Ensure the user has the attachment
        attachment_item = await self.inv_crud.get_inventory_item_by_userid(self.user_id, attachment_id)
        if not attachment_item or attachment_item.quantity < 1:
            raise ValueError("You do not have the required attachment")

        user_inv_id = await self.inv_crud.get_user_inventory_id_by_userid(self.user_id)

        # Apply attachment stats to the weapon
        attachment_data = attachment_items.get(attachment_name)
        if not attachment_data:
            raise ValueError("Attachment not found")

        weapon.apply_attachment_stats(attachment_data)

        # Remove one quantity of the attachment from the user's inventory
        await self.inv_crud.update_user_inventory_item(user_inv_id, attachment_id, -1, attachment_item)

        # Add the attachment to the weapon's attachments list
        attachments_list = json.loads(weapon.attachments) if weapon.attachments else []
        if attachment_name not in attachments_list:
            attachments_list.append(attachment_name)
            weapon.attachments = json.dumps(attachments_list)
            self.session.add(weapon)
            await self.session.commit()


    async def remove_attachment(self, weapon, attachment_name: str):
        attachments_list = json.loads(weapon.attachments) if weapon.attachments else []
        if attachment_name in attachments_list:
            # Remove attachment stats from the weapon
            attachment_data = attachment_items.get(attachment_name)
            if not attachment_data:
                raise ValueError("Attachment not found")

            weapon.remove_attachment_stats(attachment_data)

            # Add one quantity of the attachment back to the user's inventory
            attachment_id = await self.item_crud.check_item_exists(attachment_name)
            user_inv_id = await self.inv_crud.get_user_inventory_id_by_userid(self.user_id)
            await self.inv_crud.update_user_inventory_item(user_inv_id, attachment_id, 1)

            # Remove the attachment from the weapon's attachments list
            attachments_list.remove(attachment_name)
            weapon.attachments = json.dumps(attachments_list)
            self.session.add(weapon)
            await self.session.commit()

    def get_attachments(self) -> List[str]:
        return json.loads(self.attachments) if self.attachments else []
