from .. import (
    ItemType,
    ItemTier,
    ArmorType,
    ArmorBase,
    Armor,
    StaticItem
)


class TacticalHelmet(StaticItem, ArmorBase):
    __type__ = Armor
    item_name: str = "Tactical Helmet"
    category: ItemType = ItemType.Armor
    tier: ItemTier = ItemTier.Tier1
    quick_sell: int = 500
    weight: float = 1.5
    type: ArmorType = ArmorType.Head
    head_protection_adj: int = 15
    agility_adj: float = -0.1


class CombatHelmet(StaticItem, ArmorBase):
    __type__ = Armor
    item_name: str = "Combat Helmet"
    category: ItemType = ItemType.Armor
    tier: ItemTier = ItemTier.Tier2
    quick_sell: int = 1000
    type: ArmorType = ArmorType.Head
    weight: float = 2.0
    head_protection_adj: int = 25
    agility_adj: float = -0.15


class AdvancedCombatHelmet(StaticItem, ArmorBase):
    __type__ = Armor
    item_name: str = "Advanced Combat Helmet"
    category: ItemType = ItemType.Armor
    tier: ItemTier = ItemTier.Tier3
    quick_sell: int = 2000
    type: ArmorType = ArmorType.Head
    weight: float = 2.5
    head_protection_adj: int = 35
    agility_adj: float = -0.2


class LightweightVest(StaticItem, ArmorBase):
    __type__ = Armor
    item_name: str = "Lightweight Vest"
    category: ItemType = ItemType.Armor
    tier: ItemTier = ItemTier.Tier1
    quick_sell: int = 750
    type: ArmorType = ArmorType.Body
    weight: float = 3.0
    chest_protection_adj: int = 20
    stomach_protection_adj: int = 10
    arm_protection_adj: int = 5
    agility_adj: float = -0.2


class TacticalVest(StaticItem, ArmorBase):
    __type__ = Armor
    item_name: str = "Tactical Vest"
    category: ItemType = ItemType.Armor
    tier: ItemTier = ItemTier.Tier2
    quick_sell: int = 1500
    type: ArmorType = ArmorType.Body
    weight: float = 4.0
    chest_protection_adj: int = 30
    stomach_protection_adj: int = 20
    arm_protection_adj: int = 10
    agility_adj: float = -0.3


class HeavyDutyVest(StaticItem, ArmorBase):
    __type__ = Armor
    item_name: str = "Heavy Duty Vest"
    category: ItemType = ItemType.Armor
    tier: ItemTier = ItemTier.Tier3
    quick_sell: int = 2500
    type: ArmorType = ArmorType.Body
    weight: float = 5.0
    chest_protection_adj: int = 40
    stomach_protection_adj: int = 30
    arm_protection_adj: int = 15
    agility_adj: float = -0.4



armor_classes = [
    TacticalHelmet,
    CombatHelmet,
    AdvancedCombatHelmet,
    LightweightVest,
    TacticalVest,
    HeavyDutyVest
]

