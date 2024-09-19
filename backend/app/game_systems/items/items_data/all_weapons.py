from .. import (
    ItemType,
    ItemTier,
    WeaponBase,
    Weapon,
    StaticItem
)


class M1911(StaticItem, WeaponBase):
    __type__ = Weapon
    item_name: str = "M1911"
    category: ItemType = ItemType.Weapon
    tier: ItemTier = ItemTier.Tier1
    quick_sell: int = 150
    weight: float = 1.1
    can_be_modified: bool = True
    caliber: str = "9x19mm"
    damage: int = 7
    range: int = 50
    accuracy: int = 60
    reload_speed: float = 2.0
    fire_rate: float = 1.2
    magazine_size: int = 7
    armor_penetration: int = 0
    headshot_chance: int = 15
    agility_adj: float = -0.5
    allowed_modifications: dict = {
        "Muzzle": ["Flash Suppressor", "Suppressor"],
        "Magazine": ["Extended Magazine"],
        "Laser": ["Tactical Laser"]
    }


class BerettaM9(StaticItem, WeaponBase):
    __type__ = Weapon
    item_name: str = "Beretta M9"
    category: ItemType = ItemType.Weapon
    tier: ItemTier = ItemTier.Tier2
    quick_sell: int = 300
    weight: float = 0.95
    can_be_modified: bool = True
    caliber: str = "9x19mm"
    damage: int = 8
    range: int = 50
    accuracy: int = 65
    reload_speed: float = 1.7
    fire_rate: float = 1.5
    magazine_size: int = 15
    armor_penetration: int = 5
    headshot_chance: int = 18
    agility_adj: float = -0.3
    allowed_modifications: dict = {
        "Muzzle": "Flash Suppressor",
        "Magazine": "Extended Magazine",
        "Laser": "Tactical Laser"
    }


class SawedOffShotgun(StaticItem, WeaponBase):
    __type__ = Weapon
    item_name: str = "Sawed-off Shotgun"
    category: ItemType = ItemType.Weapon
    tier: ItemTier = ItemTier.Tier1
    quick_sell: int = 200
    weight: float = 2.5
    can_be_modified: bool = True
    caliber: str = "12 Gauge"
    damage: int = 15
    range: int = 20
    accuracy: int = 25
    reload_speed: float = 2.5
    fire_rate: float = 0.8
    magazine_size: int = 2
    armor_penetration: int = 10
    headshot_chance: int = 25
    agility_adj: float = -1.5
    allowed_modifications: dict = {
        "Muzzle": "Flash Suppressor"
    }


class M890(StaticItem, WeaponBase):
    __type__ = Weapon
    item_name: str = "M890"
    category: ItemType = ItemType.Weapon
    tier: ItemTier = ItemTier.Tier2
    quick_sell: int = 400
    weight: float = 3.0
    can_be_modified: bool = True
    caliber: str = "12 Gauge"
    damage: int = 18
    range: int = 30
    accuracy: int = 30
    reload_speed: float = 2.3
    fire_rate: float = 1.0
    magazine_size: int = 6
    armor_penetration: int = 12
    headshot_chance: int = 30
    agility_adj: float = -1.2
    allowed_modifications: dict = {
        "Muzzle": "Flash Suppressor"
    }


class M4A1Carbine(StaticItem, WeaponBase):
    __type__ = Weapon
    item_name: str = "M4A1 Carbine"
    category: ItemType = ItemType.Weapon
    tier: ItemTier = ItemTier.Tier3
    quick_sell: int = 1500
    weight: float = 3.1
    can_be_modified: bool = True
    caliber: str = "5.56x45mm NATO"
    damage: int = 20
    range: int = 300
    accuracy: int = 70
    reload_speed: float = 2.0
    fire_rate: float = 3.0
    magazine_size: int = 30
    armor_penetration: int = 20
    headshot_chance: int = 35
    agility_adj: float = -2.0
    allowed_modifications: dict = {
        "Muzzle": ["Flash Suppressor", "Universal Suppressor"],
        "Magazine": ["Extended Magazine"],
        "Scope": ["Sniper Scope"],
        "Stock": ["Adjustable Stock"],
        "Laser": ["Tactical Laser"]
    }


class AACHoneyBadger(StaticItem, WeaponBase):
    __type__ = Weapon
    item_name: str = "AAC Honey Badger"
    category: ItemType = ItemType.Weapon
    tier: ItemTier = ItemTier.Tier5
    quick_sell: int = 3000
    weight: float = 2.8
    can_be_modified: bool = True
    caliber: str = "300 BLK"
    damage: int = 25
    range: int = 200
    accuracy: int = 75
    reload_speed: float = 1.5
    fire_rate: float = 3.5
    magazine_size: int = 30
    armor_penetration: int = 25
    headshot_chance: int = 40
    agility_adj: float = -1.5
    allowed_modifications: dict = {
        "Muzzle": "Flash Suppressor",
        "Magazine": "Extended Magazine",
        "Scope": "Sniper Scope",
        "Stock": "Adjustable Stock",
        "Laser": "Tactical Laser"
    }


weapon_classes = [
    M1911,
    BerettaM9,
    SawedOffShotgun,
    M890,
    M4A1Carbine,
    AACHoneyBadger
]

