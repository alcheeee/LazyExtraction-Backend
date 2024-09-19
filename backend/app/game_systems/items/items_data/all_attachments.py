from .. import (
    ItemType,
    ItemTier,
    AttachmentTypes,
    AttachmentBase,
    Attachments,
    StaticItem
)


class PolymerRifleBipod(StaticItem, AttachmentBase):
    __type__ = Attachments
    item_name: str = "Polymer Rifle Bipod"
    category: ItemType = ItemType.Attachments
    tier: ItemTier = ItemTier.Tier4
    quick_sell: int = 800
    type: AttachmentTypes = AttachmentTypes.Bipod
    weight: float = 0.0
    damage_adj: int = 0
    range_adj: int = 0
    accuracy_adj: int = 0
    reload_speed_adj: float = 0.0
    fire_rate_adj: float = 0.0
    magazine_size_adj: int = 0
    headshot_chance_adj: int = 0
    agility_adj: float = 0.0


class TacticalFrontGrip(StaticItem, AttachmentBase):
    __type__ = Attachments
    item_name: str = "Tactical Front Grip"
    category: ItemType = ItemType.Attachments
    tier: ItemTier = ItemTier.Tier3
    quick_sell: int = 500
    type: AttachmentTypes = AttachmentTypes.FrontGrip
    weight: float = 0.1
    damage_adj: int = 0
    range_adj: int = 0
    accuracy_adj: int = 10
    reload_speed_adj: float = -0.1
    fire_rate_adj: float = 0.0
    magazine_size_adj: int = 0
    headshot_chance_adj: int = 0
    agility_adj: float = -0.1


class FlashSuppressor(StaticItem, AttachmentBase):
    __type__ = Attachments
    item_name: str = "Flash Suppressor"
    category: ItemType = ItemType.Attachments
    tier: ItemTier = ItemTier.Tier2
    quick_sell: int = 400
    type: AttachmentTypes = AttachmentTypes.Muzzle
    weight: float = 0.3
    damage_adj: int = 0
    range_adj: int = 4
    accuracy_adj: int = 3
    reload_speed_adj: float = 0.0
    fire_rate_adj: float = 0.0
    magazine_size_adj: int = 0
    headshot_chance_adj: int = 0
    agility_adj: float = 0.8


class UniversalSuppressor(StaticItem, AttachmentBase):
    __type__ = Attachments
    item_name: str = "Universal Suppressor"
    category: ItemType = ItemType.Attachments
    tier: ItemTier = ItemTier.Tier5
    quick_sell: int = 2200
    type: AttachmentTypes = AttachmentTypes.Muzzle
    weight: float = 0.8
    damage_adj: int = 0
    range_adj: int = -4
    accuracy_adj: int = -1
    reload_speed_adj: float = 0.0
    fire_rate_adj: float = 0.0
    magazine_size_adj: int = 0
    headshot_chance_adj: int = 0
    agility_adj: float = 2.6


class ExtendedMagazine(StaticItem, AttachmentBase):
    __type__ = Attachments
    item_name: str = "Extended Magazine"
    category: ItemType = ItemType.Attachments
    tier: ItemTier = ItemTier.Tier3
    quick_sell: int = 600
    type: AttachmentTypes = AttachmentTypes.Magazine
    weight: float = 0.2
    damage_adj: int = 0
    range_adj: int = 0
    accuracy_adj: int = 0
    reload_speed_adj: float = -0.2
    fire_rate_adj: float = 0.0
    magazine_size_adj: int = 15
    headshot_chance_adj: int = 0
    agility_adj: float = -0.2


class AdjustableStock(StaticItem, AttachmentBase):
    __type__ = Attachments
    item_name: str = "Adjustable Stock"
    category: ItemType = ItemType.Attachments
    tier: ItemTier = ItemTier.Tier2
    quick_sell: int = 450
    type: AttachmentTypes = AttachmentTypes.Stock
    weight: float = 0.1
    damage_adj: int = 0
    range_adj: int = 0
    accuracy_adj: int = 8
    reload_speed_adj: float = 0.0
    fire_rate_adj: float = 0.0
    magazine_size_adj: int = 0
    headshot_chance_adj: int = 0
    agility_adj: float = -0.1


class SniperScope(StaticItem, AttachmentBase):
    __type__ = Attachments
    item_name: str = "Sniper Scope"
    category: ItemType = ItemType.Attachments
    tier: ItemTier = ItemTier.Tier4
    quick_sell: int = 1000
    type: AttachmentTypes = AttachmentTypes.Scope
    weight: float = 0.3
    damage_adj: int = 0
    range_adj: int = 50
    accuracy_adj: int = 20
    reload_speed_adj: float = 0.0
    fire_rate_adj: float = 0.0
    magazine_size_adj: int = 0
    headshot_chance_adj: int = 5
    agility_adj: float = -0.3


class TacticalLaser(StaticItem, AttachmentBase):
    __type__ = Attachments
    item_name: str = "Tactical Laser"
    category: ItemType = ItemType.Attachments
    tier: ItemTier = ItemTier.Tier3
    quick_sell: int = 700
    type: AttachmentTypes = AttachmentTypes.Laser
    weight: float = 0.1
    damage_adj: int = 0
    range_adj: int = 0
    accuracy_adj: int = 10
    reload_speed_adj: float = 0.0
    fire_rate_adj: float = 0.0
    magazine_size_adj: int = 0
    headshot_chance_adj: int = 0
    agility_adj: float = -0.1


class LongBarrel(StaticItem, AttachmentBase):
    __type__ = Attachments
    item_name: str = "Long Barrel"
    category: ItemType = ItemType.Attachments
    tier: ItemTier = ItemTier.Tier3
    quick_sell: int = 900
    type: AttachmentTypes = AttachmentTypes.Barrel
    weight: float = 0.3
    damage_adj: int = 0
    range_adj: int = 25
    accuracy_adj: int = 15
    reload_speed_adj: float = 0.0
    fire_rate_adj: float = 0.0
    magazine_size_adj: int = 0
    headshot_chance_adj: int = 0
    agility_adj: float = -0.2



attachment_classes = [
    PolymerRifleBipod,
    TacticalFrontGrip,
    FlashSuppressor,
    UniversalSuppressor,
    ExtendedMagazine,
    AdjustableStock,
    SniperScope,
    TacticalLaser,
    LongBarrel
]

