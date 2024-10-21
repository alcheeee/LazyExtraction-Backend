from .. import (
    ItemType,
    ItemTier,
    AttachmentTypes,
    AttachmentBase,
    Attachments,
    StaticItem
)


class TacticalShortGrip(StaticItem, AttachmentBase):
    __type__ = Attachments
    item_name: str = "Tactical Short Grip"
    category: ItemType = ItemType.Attachments
    tier: ItemTier = ItemTier.Tier1
    quick_sell: int = 300
    type: AttachmentTypes = AttachmentTypes.Foregrip
    weight: float = 0.1
    damage_adj: int = 0
    range_adj: int = 0
    accuracy_adj: int = 5
    reload_speed_adj: float = 0.15
    fire_rate_adj: float = 0
    magazine_size_adj: int = 0
    headshot_chance_adj: int = 2
    agility_adj: float = 0.15


class CompactForegrip(StaticItem, AttachmentBase):
    __type__ = Attachments
    item_name: str = "Compact Foregrip"
    category: ItemType = ItemType.Attachments
    tier: ItemTier = ItemTier.Tier2
    quick_sell: int = 450
    type: AttachmentTypes = AttachmentTypes.Foregrip
    weight: float = 0.15
    damage_adj: int = 0
    range_adj: int = 0
    accuracy_adj: int = 8
    reload_speed_adj: float = 0.1
    fire_rate_adj: float = 0.05
    magazine_size_adj: int = 0
    headshot_chance_adj: int = 3
    agility_adj: float = 0.5


class HeavyDutyGrip(StaticItem, AttachmentBase):
    __type__ = Attachments
    item_name: str = "Heavy Duty Grip"
    category: ItemType = ItemType.Attachments
    tier: ItemTier = ItemTier.Tier2
    quick_sell: int = 500
    type: AttachmentTypes = AttachmentTypes.Foregrip
    weight: float = 0.3
    damage_adj: int = 0
    range_adj: int = 5
    accuracy_adj: int = 10
    reload_speed_adj: float = -0.05
    fire_rate_adj: float = 0.0
    magazine_size_adj: int = 0
    headshot_chance_adj: int = 3
    agility_adj: float = -0.4


class PrecisionLongGrip(StaticItem, AttachmentBase):
    __type__ = Attachments
    item_name: str = "Precision Long Grip"
    category: ItemType = ItemType.Attachments
    tier: ItemTier = ItemTier.Tier3
    quick_sell: int = 720
    type: AttachmentTypes = AttachmentTypes.Foregrip
    weight: float = 0.3
    damage_adj: int = 0
    range_adj: int = 15
    accuracy_adj: int = 10
    reload_speed_adj: float = -0.05
    fire_rate_adj: float = 0.0
    magazine_size_adj: int = 0
    headshot_chance_adj: int = 8
    agility_adj: float = -0.3


class VerticalTiltGrip(StaticItem, AttachmentBase):
    __type__ = Attachments
    item_name: str = "Vertical Tilt Grip"
    category: ItemType = ItemType.Attachments
    tier: ItemTier = ItemTier.Tier4
    quick_sell: int = 950
    type: AttachmentTypes = AttachmentTypes.Foregrip
    weight: float = 0.4
    damage_adj: int = 0
    range_adj: int = 12
    accuracy_adj: int = 24
    reload_speed_adj: float = -0.24
    fire_rate_adj: float = 0.0
    magazine_size_adj: int = 0
    headshot_chance_adj: int = 18
    agility_adj: float = -0.35


class Holographic1x(StaticItem, AttachmentBase):
    __type__ = Attachments
    item_name: str = "Holographic (1x)"
    category: ItemType = ItemType.Attachments
    tier: ItemTier = ItemTier.Tier2
    quick_sell: int = 550
    type: AttachmentTypes = AttachmentTypes.Scope
    weight: float = 0.3
    damage_adj: int = 0
    range_adj: int = 12
    accuracy_adj: int = 14
    reload_speed_adj: float = 0.0
    fire_rate_adj: float = 0.0
    magazine_size_adj: int = 0
    headshot_chance_adj: int = 6
    agility_adj: float = -0.28


class Holographic1x4x(StaticItem, AttachmentBase):
    __type__ = Attachments
    item_name: str = "Holographic (1x-4x)"
    category: ItemType = ItemType.Attachments
    tier: ItemTier = ItemTier.Tier4
    quick_sell: int = 1350
    type: AttachmentTypes = AttachmentTypes.Scope
    weight: float = 0.4
    damage_adj: int = 0
    range_adj: int = 28
    accuracy_adj: int = 32
    reload_speed_adj: float = 0.0
    fire_rate_adj: float = 0.0
    magazine_size_adj: int = 0
    headshot_chance_adj: int = 28
    agility_adj: float = -0.52



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


attachment_classes = [
    TacticalShortGrip,
    CompactForegrip,
    FlashSuppressor,
    UniversalSuppressor,
    ExtendedMagazine,
    AdjustableStock,
    SniperScope,
    HeavyDutyGrip,
    PrecisionLongGrip,
    VerticalTiltGrip,
    Holographic1x,
    Holographic1x4x
]


