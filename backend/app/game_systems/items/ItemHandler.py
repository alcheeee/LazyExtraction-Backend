from typing import Optional, Union
from sqlalchemy.ext.asyncio import AsyncSession
from .ItemCreatorClasses import (
    MedicalCreator,
    ArmorCreator,
    WeaponCreator,
    ClothingCreator,
    BulletCreator,
    AttachmentCreator
)
from . import (
    MedicalCreate,
    ClothingCreate,
    ArmorCreate,
    ArmorType,
    WeaponCreate,
    ItemType,
    BulletCreate,
    AttachmentCreate
)
from .items_data import (
    medical_items,
    armor_items,
    weapon_items,
    clothing_items,
    bullet_items,
    attachment_items
)


class NewItem:
    class BaseItem:
        def __init__(self, item_name: str, session: AsyncSession):
            self.item_name = item_name
            self.session = session

        def get_item_data(self, item_dict: dict):
            for category_dict in item_dict.values():
                item_data = category_dict.get(self.item_name)
                if item_data:
                    return item_data
            raise Exception(f"Item {self.item_name} not found")


        @staticmethod
        def create_request(item_data, schema_class):
            return schema_class(**item_data)


    class Medical(BaseItem):
        async def create(self):
            item_data = self.get_item_data(medical_items)
            request = self.create_request(item_data, MedicalCreate)
            creator = MedicalCreator(request, self.session)
            return await creator.create_medical()


    class Clothing(BaseItem):
        async def create(self):
            item_data = self.get_item_data(clothing_items)
            request = self.create_request(item_data, ClothingCreate)
            creator = ClothingCreator(request, self.session)
            return await creator.create_clothing()


    class Weapon(BaseItem):
        async def create(self):
            item_data = self.get_item_data(weapon_items)
            request = self.create_request(item_data, WeaponCreate)
            creator = WeaponCreator(request, self.session)
            return await creator.create_weapon()


    class Armor(BaseItem):
        async def create(self):
            item_data = self.get_item_data(armor_items)
            request = self.create_request(item_data, ArmorCreate)
            creator = ArmorCreator(request, self.session)
            return await creator.create_armor()


    class Bullet(BaseItem):
        async def create(self):
            item_data = self.get_item_data(bullet_items)
            request = self.create_request(item_data, BulletCreate)
            creator = BulletCreator(request, self.session)
            return await creator.create_bullet()


    class Attachment(BaseItem):
        async def create(self):
            item_data = self.get_item_data(attachment_items)
            request = self.create_request(item_data, AttachmentCreate)
            creator = AttachmentCreator(request, self.session)
            return await creator.create_attachment()


    @classmethod
    async def create_item(cls, item_data, session: AsyncSession):
        item_name = item_data['item_name']
        item_category = item_data['category']
        item_class = {
            ItemType.Medical: cls.Medical,
            ItemType.Clothing: cls.Clothing,
            ItemType.Weapon: cls.Weapon,
            ItemType.Armor: cls.Armor,
            ItemType.Bullets: cls.Bullet,
            ItemType.Attachments: cls.Attachment
        }.get(item_category)

        if item_class:
            item_instance = item_class(item_name, session)
            return await item_instance.create()
        else:
            raise ValueError(f"Unsupported item category: {item_category}")

    @classmethod
    async def initialize_static_items(cls, item_data, session):
        return await cls.create_item(item_data, session)

