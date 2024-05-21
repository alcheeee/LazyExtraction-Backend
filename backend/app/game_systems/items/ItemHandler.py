import tenacity
from typing import Dict, Type
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from .ItemCreationLogic import GenerateItemQuality, GenerateItemStats
from ...schemas.item_schema import ItemType, ClothingCreate, ArmorCreate, ArmorType, WeaponCreate
from ...models import (
    Items,
    Weapon,
    Clothing,
    Armor
)


class ClothingCreator:
    def __init__(self, request: ClothingCreate, session: AsyncSession, user_luck=1.0):
        self.request = request
        self.session = session
        self.user_luck = user_luck

    def generators(self, quality=None, randomize_all=True):
        if randomize_all:
            quality_generator = GenerateItemQuality(self.user_luck)
            quality = quality_generator.generate_item_quality()

        stats_generator = GenerateItemStats(self.request.category, quality, self.user_luck)
        item_specific_details = stats_generator.generate_stats()
        quick_sell_value = stats_generator.generate_quick_sell(self.request.quick_sell)
        return quality, item_specific_details, quick_sell_value

    @tenacity.retry(
        wait=tenacity.wait_fixed(1),
        stop=tenacity.stop_after_attempt(3),
        retry=tenacity.retry_if_not_exception_type(ValueError)
    )
    async def create_clothing_item(self):
        quality = self.request.quality

        if self.request.randomize_all:
            quality, clothing_details, quick_sell_value = self.generators(randomize_all=True)
        elif self.request.randomize_stats:
            _, clothing_details, quick_sell_value = self.generators(quality=quality, randomize_all=False)
        else:
            clothing_details = self.request.dict(
                exclude_unset=True, exclude={
                    "item_name", "illegal", "quality",
                    "randomize_stats", "randomize_all", "category", "quick_sell"
                })

        item_data = {
            "item_name": self.request.item_name,
            "illegal": self.request.illegal,
            "category": ItemType.Clothing,
            "quality": quality,
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


class ArmorCreator:
    def __init__(self, request: ArmorCreate, session: AsyncSession):
        self.request = request
        self.session = session

    @tenacity.retry(
        wait=tenacity.wait_fixed(1),
        stop=tenacity.stop_after_attempt(3),
        retry=tenacity.retry_if_not_exception_type(ValueError)
    )
    async def create_armor(self):
        item_data = {
            "item_name": self.request.item_name,
            "illegal": self.request.illegal,
            "category": ItemType.Armor,
            "quality": self.request.quality,
            "quick_sell": self.request.quick_sell
        }
        item = Items(**item_data)
        self.session.add(item)
        await self.session.flush()

        armor_details = Armor(
            item_id=item.id,
            type=self.request.type,
            durability=self.request.durability,
            weight=self.request.weight,
            head_protection=self.request.head_protection,
            chest_protection=self.request.chest_protection,
            stomach_protection=self.request.stomach_protection,
            arm_protection=self.request.arm_protection,
            agility_penalty=self.request.agility_penalty
        )
        self.session.add(armor_details)

        return armor_details


class WeaponCreator:
    def __init__(self, request: WeaponCreate, session: AsyncSession):
        self.request = request
        self.session = session

    @tenacity.retry(
        wait=tenacity.wait_fixed(1),
        stop=tenacity.stop_after_attempt(3),
        retry=tenacity.retry_if_not_exception_type(ValueError)
    )
    async def create_weapon(self):

        item_data = {
            "item_name": self.request.item_name,
            "illegal": self.request.illegal,
            "category": ItemType.Weapon,
            "quality": self.request.quality,
            "quick_sell": self.request.quick_sell
        }

        item = Items(**item_data)
        self.session.add(item)
        await self.session.flush()

        weapon_details = Weapon(
            item_id=item.id,
            damage_bonus=self.request.damage_bonus,
            strength_bonus=self.request.strength_bonus,
            weight=self.request.weight,
            durability=self.request.durability,
            range=self.request.range,
            accuracy=self.request.accuracy,
            reload_speed=self.request.reload_speed,
            fire_rate=self.request.fire_rate,
            magazine_size=self.request.magazine_size,
            armor_penetration=self.request.armor_penetration,
            headshot_chance=self.request.headshot_chance,
            agility_bonus=self.request.agility_bonus
        )

        self.session.add(weapon_details)
        return weapon_details
















