from .. import (
    ItemType,
    ItemTier,
    ClothingType,
    ClothingBase,
    Clothing,
    StaticItem
)


class StealthBalaclava(StaticItem, ClothingBase):
    __type__ = Clothing
    item_name: str = "Stealth Balaclava"
    category: ItemType = ItemType.Clothing
    tier: ItemTier = ItemTier.Tier1
    quick_sell: int = 200
    clothing_type: ClothingType = ClothingType.Mask
    reputation_adj: int = 0
    max_energy_adj: int = 0
    agility_adj: float = 0.0
    health_adj: int = 0
    luck_adj: float = 0.0
    strength_adj: float = 0.0
    knowledge_adj: float = 0.0


class ReconBandana(StaticItem, ClothingBase):
    __type__ = Clothing
    item_name: str = "Recon Bandana"
    category: ItemType = ItemType.Clothing
    tier: ItemTier = ItemTier.Tier2
    quick_sell: int = 500
    clothing_type: ClothingType = ClothingType.Mask
    reputation_adj: int = 0
    max_energy_adj: int = 0
    agility_adj: float = 0.0
    health_adj: int = 0
    luck_adj: float = 0.0
    strength_adj: float = 0.0
    knowledge_adj: float = 0.0


class CommandoJacket(StaticItem, ClothingBase):
    __type__ = Clothing
    item_name: str = "Commando Jacket"
    category: ItemType = ItemType.Clothing
    tier: ItemTier = ItemTier.Tier1
    quick_sell: int = 300
    clothing_type: ClothingType = ClothingType.Shirt
    reputation_adj: int = 0
    max_energy_adj: int = 0
    agility_adj: float = 0.0
    health_adj: int = 0
    luck_adj: float = 0.0
    strength_adj: float = 0.0
    knowledge_adj: float = 0.0


class TacticalHoodie(StaticItem, ClothingBase):
    __type__ = Clothing
    item_name: str = "Tactical Hoodie"
    category: ItemType = ItemType.Clothing
    tier: ItemTier = ItemTier.Tier3
    quick_sell: int = 1500
    clothing_type: ClothingType = ClothingType.Shirt
    reputation_adj: int = 0
    max_energy_adj: int = 0
    agility_adj: float = 0.0
    health_adj: int = 0
    luck_adj: float = 0.0
    strength_adj: float = 0.0
    knowledge_adj: float = 0.0


class CargoPants(StaticItem, ClothingBase):
    __type__ = Clothing
    item_name: str = "Cargo Pants"
    category: ItemType = ItemType.Clothing
    tier: ItemTier = ItemTier.Tier1
    quick_sell: int = 250
    clothing_type: ClothingType = ClothingType.Legs
    reputation_adj: int = 0
    max_energy_adj: int = 0
    agility_adj: float = 0.0
    health_adj: int = 0
    luck_adj: float = 0.0
    strength_adj: float = 0.0
    knowledge_adj: float = 0.0


class StealthOpsCargoPants(StaticItem, ClothingBase):
    __type__ = Clothing
    item_name: str = "Stealth Ops Cargo Pants"
    category: ItemType = ItemType.Clothing
    tier: ItemTier = ItemTier.Tier2
    quick_sell: int = 750
    clothing_type: ClothingType = ClothingType.Legs
    reputation_adj: int = 0
    max_energy_adj: int = 0
    agility_adj: float = 0.0
    health_adj: int = 0
    luck_adj: float = 0.0
    strength_adj: float = 0.0
    knowledge_adj: float = 0.0


clothing_classes = [
    StealthBalaclava,
    ReconBandana,
    CommandoJacket,
    TacticalHoodie,
    CargoPants,
    StealthOpsCargoPants
]
