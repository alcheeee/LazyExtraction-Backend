from .. import (
    ItemType,
    ItemTier,
    BulletBase,
    Bullets,
    StaticItem
)


class NineX19mm(StaticItem, BulletBase):
    __type__ = Bullets
    item_name: str = "9x19mm"
    category: ItemType = ItemType.Bullets
    tier: ItemTier = ItemTier.Tier1
    quick_sell: int = 1
    armor_pen_adj: int = 0
    accuracy_adj: int = 0
    range_adj: int = 0
    damage_adj: int = 0
    fire_rate_adj: float = 0.0
    reload_speed_adj: float = 0.0


class NineX19mmAP(StaticItem, BulletBase):
    __type__ = Bullets
    item_name: str = "9x19mm AP"
    category: ItemType = ItemType.Bullets
    tier: ItemTier = ItemTier.Tier2
    quick_sell: int = 2
    armor_pen_adj: int = 5
    accuracy_adj: int = 0
    range_adj: int = 5
    damage_adj: int = 2
    fire_rate_adj: float = 0.0
    reload_speed_adj: float = -0.1


class TwelveGauge(StaticItem, BulletBase):
    __type__ = Bullets
    item_name: str = "12 Gauge"
    category: ItemType = ItemType.Bullets
    tier: ItemTier = ItemTier.Tier1
    quick_sell: int = 2
    armor_pen_adj: int = 0
    accuracy_adj: int = 0
    range_adj: int = 0
    damage_adj: int = 10
    fire_rate_adj: float = 0.0
    reload_speed_adj: float = 0.0


class TwelveGaugeSlug(StaticItem, BulletBase):
    __type__ = Bullets
    item_name: str = "12 Gauge Slug"
    category: ItemType = ItemType.Bullets
    tier: ItemTier = ItemTier.Tier2
    quick_sell: int = 3
    armor_pen_adj: int = 10
    accuracy_adj: int = 5
    range_adj: int = 10
    damage_adj: int = 15
    fire_rate_adj: float = 0.0
    reload_speed_adj: float = -0.1


class FiveFiveSixX45mmNATO(StaticItem, BulletBase):
    __type__ = Bullets
    item_name: str = "5.56x45mm NATO"
    category: ItemType = ItemType.Bullets
    tier: ItemTier = ItemTier.Tier2
    quick_sell: int = 3
    armor_pen_adj: int = 10
    accuracy_adj: int = 5
    range_adj: int = 10
    damage_adj: int = 5
    fire_rate_adj: float = 0.0
    reload_speed_adj: float = -0.1


class FiveFiveSixX45mmNATOAP(StaticItem, BulletBase):
    __type__ = Bullets
    item_name: str = "5.56x45mm NATO AP"
    category: ItemType = ItemType.Bullets
    tier: ItemTier = ItemTier.Tier3
    quick_sell: int = 4
    armor_pen_adj: int = 15
    accuracy_adj: int = 5
    range_adj: int = 15
    damage_adj: int = 10
    fire_rate_adj: float = 0.0
    reload_speed_adj: float = -0.1


class ThreeHundredBLK(StaticItem, BulletBase):
    __type__ = Bullets
    item_name: str = "300 BLK"
    category: ItemType = ItemType.Bullets
    tier: ItemTier = ItemTier.Tier3
    quick_sell: int = 4
    armor_pen_adj: int = 10
    accuracy_adj: int = 5
    range_adj: int = 10
    damage_adj: int = 7
    fire_rate_adj: float = 0.0
    reload_speed_adj: float = -0.1


class ThreeHundredBLKAP(StaticItem, BulletBase):
    __type__ = Bullets
    item_name: str = "300 BLK AP"
    category: ItemType = ItemType.Bullets
    tier: ItemTier = ItemTier.Tier4
    quick_sell: int = 5
    armor_pen_adj: int = 20
    accuracy_adj: int = 10
    range_adj: int = 20
    damage_adj: int = 12
    fire_rate_adj: float = 0.0
    reload_speed_adj: float = -0.1



bullet_classes = [
    NineX19mm,
    NineX19mmAP,
    TwelveGauge,
    TwelveGaugeSlug,
    FiveFiveSixX45mmNATO,
    FiveFiveSixX45mmNATOAP,
    ThreeHundredBLK,
    ThreeHundredBLKAP
]

