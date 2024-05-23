import tenacity
from sqlalchemy.ext.asyncio import AsyncSession
from .ItemCreationLogic import GenerateItemTier, GenerateItemStats
from . import (
    tier_multipliers,
    ItemType,
    MedicalCreate,
    ClothingCreate,
    ArmorCreate,
    WeaponCreate
)
from ...models import (
    Items,
    Medical,
    Weapon,
    Clothing,
    Armor
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

        total_quick_sell = int(request.quick_sell * tier_multipliers[item_data['tier']])
        item_data['quick_sell'] = total_quick_sell

        item = Items(**item_data)
        session.add(item)
        await session.flush()
        return item


class ArmorCreator(BaseItemCreator):
    def __init__(self, request: ArmorCreate, session: AsyncSession):
        super().__init__(request, session)

    @tenacity.retry(
        wait=tenacity.wait_fixed(1),
        stop=tenacity.stop_after_attempt(3),
        retry=tenacity.retry_if_not_exception_type(ValueError)
    )
    async def create_armor(self):
        item = await self.create_base_item(self.request, self.session)
        armor_details = Armor(
            item_id=item.id,
            type=self.request.type,
            max_durability=self.request.max_durability,
            current_durability=self.request.current_durability,
            weight=self.request.weight,
            head_protection=self.request.head_protection,
            chest_protection=self.request.chest_protection,
            stomach_protection=self.request.stomach_protection,
            arm_protection=self.request.arm_protection,
            agility_penalty=self.request.agility_penalty
        )
        self.session.add(armor_details)
        return armor_details


class MedicalCreator(BaseItemCreator):
    def __init__(self, request: MedicalCreate, session: AsyncSession):
        super().__init__(request, session)

    @tenacity.retry(
        wait=tenacity.wait_fixed(1),
        stop=tenacity.stop_after_attempt(3),
        retry=tenacity.retry_if_not_exception_type(ValueError)
    )
    async def create_medical(self):
        item = await self.create_base_item(self.request, self.session)
        medical_details = Medical(
            item_id=item.id,
            health_increase=self.request.health_increase,
            pain_reduction=self.request.weight_bonus,
            weight_bonus=self.request.weight_bonus,
            agility_bonus=self.request.agility_bonus,
            amount_of_actions=self.request.amount_of_actions
        )
        self.session.add(medical_details)
        return medical_details


class WeaponCreator(BaseItemCreator):
    def __init__(self, request: WeaponCreate, session: AsyncSession):
        super().__init__(request, session)

    @tenacity.retry(
        wait=tenacity.wait_fixed(1),
        stop=tenacity.stop_after_attempt(3),
        retry=tenacity.retry_if_not_exception_type(ValueError)
    )
    async def create_weapon(self):
        item = await self.create_base_item(self.request, self.session)
        weapon_details = Weapon(
            item_id=item.id,
            caliber=self.request.caliber,
            damage_bonus=self.request.damage_bonus,
            strength_bonus=self.request.strength_bonus,
            weight=self.request.weight,
            max_durability=self.request.max_durability,
            current_durability=self.request.current_durability,
            range=self.request.range,
            accuracy=self.request.accuracy,
            reload_speed=self.request.reload_speed,
            fire_rate=self.request.fire_rate,
            magazine_size=self.request.magazine_size,
            armor_penetration=self.request.armor_penetration,
            headshot_chance=self.request.headshot_chance,
            agility_penalty=self.request.agility_penalty
        )
        self.session.add(weapon_details)
        return weapon_details


class ClothingCreator:
    def __init__(self, request: ClothingCreate, session: AsyncSession, user_luck=1.0):
        self.request = request
        self.session = session
        self.user_luck = user_luck

    def generators(self, tier=None, randomize_all=True):
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

        if self.request.randomize_all:
            tier, clothing_details, quick_sell_value = self.generators(randomize_all=True)
        elif self.request.randomize_stats:
            _, clothing_details, quick_sell_value = self.generators(tier=tier, randomize_all=False)
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













