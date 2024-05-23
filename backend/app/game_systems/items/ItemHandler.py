from typing import Optional, Union
from sqlalchemy.ext.asyncio import AsyncSession
from .ItemCreatorClasses import (
    MedicalCreator,
    ArmorCreator,
    WeaponCreator,
    ClothingCreator
)
from . import (
    ItemTier,
    MedicalCreate,
    ClothingCreate,
    ArmorCreate,
    ArmorType
)
from ...schemas import WeaponCreate
from .items_data import (
    medical_items,
    armor_items,
    weapon_items,
    clothing_items
)


class NewItem:
    class BaseItem:
        def __init__(self, item_name: str, item_variant: Optional[Union[str, ItemTier]], session: AsyncSession):
            self.item_name = item_name
            self.item_variant = item_variant
            self.session = session

        def get_item_data(self, item_dict):
            item_data = item_dict.get(self.item_name, {}).get(self.item_variant)
            if not item_data:
                raise Exception(f"Item or tier not found for {self.item_name} with tier {self.item_variant}")
            return item_data

    class Medical(BaseItem):
        async def create(self):
            request = self.create_medical_request()
            creator = MedicalCreator(request, self.session)
            return await creator.create_medical()

        def create_medical_request(self):
            item_data = self.get_item_data(medical_items)
            return MedicalCreate(
                item_name=item_data['item_name'],
                category=item_data['category'],
                tier=item_data['tier'],
                quick_sell=item_data['quick_sell'],
                health_increase=item_data.get('health_increase', 0),
                pain_reduction=item_data.get('pain_reduction', 0),
                weight_bonus=item_data.get('weight_bonus', 0),
                agility_bonus=item_data.get('agility_bonus', 0),
                amount_of_actions=item_data.get('amount_of_actions', 0)
            )


    class Clothing(BaseItem):
        async def create(self):
            request = self.create_clothing_request()
            creator = ClothingCreator(request, self.session)
            return await creator.create_clothing()

        def create_clothing_request(self):
            item_data = self.get_item_data(clothing_items)
            return ClothingCreate(
                item_name=item_data['item_name'],
                category=item_data['category'],
                tier=item_data['tier'],
                quick_sell=item_data['quick_sell'],
                clothing_type=item_data.get('clothing_type', None),
                reputation_bonus=item_data.get('reputation_bonus', 0),
                max_energy_bonus=item_data.get('max_energy_bonus', 0),
                damage_bonus=item_data.get('damage_bonus', 0),
                agility_bonus=item_data.get('agility_bonus', 0.01),
                health_bonus=item_data.get('health_bonus', 0),
                luck_bonus=item_data.get('luck_bonus', 0.01),
                strength_bonus=item_data.get('strength_bonus', 0.01),
                knowledge_bonus=item_data.get('knowledge_bonus', 0.01),
                randomize_all=item_data.get('randomize_all', False),
                randomize_stats=item_data.get('randomize_stats', False)
            )


    class Weapon(BaseItem):
        async def create(self):
            request = self.create_weapon_request()
            creator = WeaponCreator(request, self.session)
            return await creator.create_weapon()

        def create_weapon_request(self):
            item_data = self.get_item_data(weapon_items)
            return WeaponCreate(
                item_name=item_data['item_name'],
                category=item_data['category'],
                tier=item_data['tier'],
                quick_sell=item_data['quick_sell'],
                weight=item_data.get('weight', 3.5),
                max_durability=item_data.get('max_durability', 100),
                current_durability=item_data.get('current_durability', 100.00),
                damage_bonus=item_data.get('damage_bonus', 0),
                strength_bonus=item_data.get('strength_bonus', 0.00),
                range=item_data.get('range', 5),
                accuracy=item_data.get('accuracy', 50),
                reload_speed=item_data.get('reload_speed', 0),
                fire_rate=item_data.get('fire_rate', 0),
                magazine_size=item_data.get('magazine_size', 0),
                armor_penetration=item_data.get('armor_penetration', 0),
                headshot_chance=item_data.get('headshot_chance', 0),
                agility_penalty=item_data.get('agility_penalty', -1.4)
            )


    class Armor(BaseItem):
        async def create(self):
            request = self.create_armor_request()
            creator = ArmorCreator(request, self.session)
            return await creator.create_armor()

        def create_armor_request(self):
            item_data = self.get_item_data(armor_items)
            return ArmorCreate(
                item_name=item_data['item_name'],
                category=item_data['category'],
                tier=item_data['tier'],
                quick_sell=item_data['quick_sell'],
                type=item_data.get('type', ArmorType.Head),
                max_durability=item_data.get('max_durability', 100),
                current_durability=item_data.get('current_durability', 100.00),
                weight=item_data.get('weight', 5.5),
                head_protection=item_data.get('head_protection', 0),
                chest_protection=item_data.get('chest_protection', 0),
                stomach_protection=item_data.get('stomach_protection', 0),
                arm_protection=item_data.get('arm_protection', 0),
                agility_penalty=item_data.get('agility_penalty', -0.4)
            )


