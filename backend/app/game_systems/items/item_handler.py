from typing import Type, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from .item_creator_classes import BaseItemCreator
from . import (
    MedicalCreate,
    ClothingCreate,
    ArmorCreate,
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
from ...models import (
    Medical,
    Weapon,
    Attachments,
    Armor,
    Bullets,
    Clothing,
)


class NewItem:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.creator = BaseItemCreator(session)

    @staticmethod
    def get_item_data(item_name: str, item_dict: Dict[str, Dict[str, Any]]):
        item_data = item_dict.get(item_name)
        if item_data:
            return item_data
        raise Exception(f"Item {item_name} not found")

    @staticmethod
    def create_request(item_data: Dict[str, Any], schema_class: Type):
        return schema_class(**item_data)

    async def create_item(self, item_data: Dict[str, Any], admin_request: bool = False):
        item_name = item_data['item_name']
        item_category = item_data['category']

        category_mapping = {
            ItemType.Medical: (medical_items, MedicalCreate, Medical),
            ItemType.Clothing: (clothing_items, ClothingCreate, Clothing),
            ItemType.Weapon: (weapon_items, WeaponCreate, Weapon),
            ItemType.Armor: (armor_items, ArmorCreate, Armor),
            ItemType.Bullets: (bullet_items, BulletCreate, Bullets),
            ItemType.Attachments: (attachment_items, AttachmentCreate, Attachments)
        }

        if item_category not in category_mapping:
            raise ValueError(f"Unsupported item category: {item_category}")

        data_dictionary, schema_class, detail_class = category_mapping[item_category]

        if admin_request:
            request = self.create_request(item_data, schema_class)
        else:
            static_item_data = self.get_item_data(item_name, data_dictionary)
            request = self.create_request(static_item_data, schema_class)

        return await self.creator.create_item(request, detail_class)

    @classmethod
    async def initialize_static_items(cls, item_data: Dict[str, Any], session: AsyncSession):
        new_item = cls(session)
        return await new_item.create_item(item_data)

