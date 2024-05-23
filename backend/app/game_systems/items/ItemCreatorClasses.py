import json
import tenacity
from sqlalchemy.ext.asyncio import AsyncSession
from .ItemCreationLogic import GenerateItemTier, GenerateItemStats
from . import (
    ItemType,
    MedicalCreate,
    ClothingCreate,
    ArmorCreate,
    WeaponCreate,
    BulletCreate,
    AttachmentCreate
)
from ...models import (
    Items,
    Medical,
    Clothing,
    Armor,
    Weapon,
    Bullets,
    Attachments
)


class BaseItemCreator:
    def __init__(self, request, session: AsyncSession):
        self.request = request
        self.session = session

    @staticmethod
    async def create_base_item(request, session: AsyncSession):
        item_data = {
            "item_name": request.item_name,
            "category": request.category,
            "tier": request.tier,
            "quick_sell": request.quick_sell
        }
        item = Items(**item_data)
        session.add(item)
        await session.flush()
        return item


class ArmorCreator(BaseItemCreator):
    @tenacity.retry(
        wait=tenacity.wait_fixed(1),
        stop=tenacity.stop_after_attempt(3),
        retry=tenacity.retry_if_not_exception_type(ValueError)
    )
    async def create_armor(self):
        item = await self.create_base_item(self.request, self.session)
        armor_details = Armor(
            item_id=item.id,
            **self.request.dict(exclude={'item_name', 'category', 'tier', 'quick_sell'})
        )
        self.session.add(armor_details)
        return armor_details


class MedicalCreator(BaseItemCreator):
    @tenacity.retry(
        wait=tenacity.wait_fixed(1),
        stop=tenacity.stop_after_attempt(3),
        retry=tenacity.retry_if_not_exception_type(ValueError)
    )
    async def create_medical(self):
        item = await self.create_base_item(self.request, self.session)
        medical_details = Medical(
            item_id=item.id,
            **self.request.dict(exclude={'item_name', 'category', 'tier', 'quick_sell'})
        )
        self.session.add(medical_details)
        return medical_details


class WeaponCreator(BaseItemCreator):
    @tenacity.retry(
        wait=tenacity.wait_fixed(1),
        stop=tenacity.stop_after_attempt(3),
        retry=tenacity.retry_if_not_exception_type(ValueError)
    )
    async def create_weapon(self):
        item = await self.create_base_item(self.request, self.session)
        weapon_data = self.request.dict(exclude={'item_name', 'category', 'tier', 'quick_sell'})
        weapon_details = Weapon(
            item_id=item.id,
            **weapon_data
        )
        self.session.add(weapon_details)
        return weapon_details


class BulletCreator(BaseItemCreator):
    @tenacity.retry(
        wait=tenacity.wait_fixed(1),
        stop=tenacity.stop_after_attempt(3),
        retry=tenacity.retry_if_not_exception_type(ValueError)
    )
    async def create_bullet(self):
        item = await self.create_base_item(self.request, self.session)
        bullet_details = Bullets(
            item_id=item.id,
            **self.request.dict(exclude={'item_name', 'category', 'tier', 'quick_sell'})
        )
        self.session.add(bullet_details)
        return bullet_details


class AttachmentCreator(BaseItemCreator):
    @tenacity.retry(
        wait=tenacity.wait_fixed(1),
        stop=tenacity.stop_after_attempt(3),
        retry=tenacity.retry_if_not_exception_type(ValueError)
    )
    async def create_attachment(self):
        item = await self.create_base_item(self.request, self.session)
        attachment_details = Attachments(
            item_id=item.id,
            **self.request.dict(exclude={'item_name', 'category', 'tier', 'quick_sell'})
        )
        self.session.add(attachment_details)
        return attachment_details




class ClothingCreator:
    def __init__(self, request: ClothingCreate, session: AsyncSession, user_luck=1.0):
        self.request = request
        self.session = session
        self.user_luck = user_luck

    def generators(self, randomize_all=True):
        tier = self.request.tier
        if randomize_all:
            tier_generator = GenerateItemTier(self.user_luck)
            tier = tier_generator.generate_item_tier()

        stats_generator = GenerateItemStats(self.request.category, tier, self.user_luck)
        item_specific_details = stats_generator.generate_stats()
        quick_sell_value = stats_generator.generate_quick_sell(self.request.quick_sell)
        return tier, item_specific_details, quick_sell_value


    @tenacity.retry(
        wait=tenacity.wait_fixed(1),
        stop=tenacity.stop_after_attempt(3),
        retry=tenacity.retry_if_not_exception_type(ValueError)
    )
    async def create_clothing(self):
        tier = self.request.tier
        quick_sell_value = self.request.quick_sell

        if self.request.randomize_all:
            tier, clothing_details, quick_sell_value = self.generators(randomize_all=True)
        elif self.request.randomize_stats:
            _, clothing_details, quick_sell_value = self.generators(randomize_all=False)
        else:
            clothing_details = self.request.dict(
                exclude_unset=True, exclude={
                    "item_name", "tier", "randomize_stats",
                    "randomize_all", "category", "quick_sell"
                })

        item_data = {
            "item_name": self.request.item_name,
            "category": ItemType.Clothing,
            "tier": tier,
            "quick_sell": quick_sell_value
        }

        if 'clothing_type' not in clothing_details and hasattr(self.request, 'clothing_type'):
            clothing_details['clothing_type'] = self.request.clothing_type


        item = Items(**item_data)
        self.session.add(item)
        await self.session.flush()

        item_detail_instance = Clothing(item_id=item.id, **clothing_details)
        self.session.add(item_detail_instance)

        full_item_details = {**item_data, **clothing_details}
        return full_item_details













