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
        "Magazine": ["Extended Magazine"]
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
        "Magazine": "Extended Magazine"
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


class M4Carbine(StaticItem, WeaponBase):
    __type__ = Weapon
    item_name: str = "M4 Carbine"
    category: ItemType = ItemType.Weapon
    tier: ItemTier = ItemTier.Tier3
    quick_sell: int = 1500
    weight: float = 3.1
    can_be_modified: bool = True
    caliber: str = "5.56x45mm"
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
        "Foregrip": [
            "Compact Foregrip",
            "Heavy Duty Grip",
            "Precision Long Grip",
            "Tactical Short Grip",
            "Vertical Tilt Grip"
        ],
        "Scope": [
            "Holographic (1x)",
            "Holographic (1x-4x)"
        ]
    }



class HoneyBadger(StaticItem, WeaponBase):
    __type__ = Weapon
    item_name: str = "Honey Badger"
    category: ItemType = ItemType.Weapon
    tier: ItemTier = ItemTier.Tier4
    quick_sell: int = 3000
    weight: float = 5.4
    can_be_modified: bool = True
    caliber: str = "300 BLK"
    damage: int = 25
    range: int = 0
    accuracy: int = 75
    reload_speed: float = 1.5
    fire_rate: float = 3.5
    magazine_size: int = 30
    armor_penetration: int = 25
    headshot_chance: int = 40
    agility_adj: float = -1.5
    allowed_modifications: dict = {
        "Foregrip": [
            "Compact Foregrip",
            "Heavy Duty Grip",
            "Precision Long Grip",
            "Tactical Short Grip",
            "Vertical Tilt Grip"
        ],
        "Scope": [
            "Holographic (1x)",
            "Holographic (1x-4x)"
        ]
    }



class AK74(StaticItem, WeaponBase):
    __type__ = Weapon
    item_name: str = "AK 74"
    category: ItemType = ItemType.Weapon
    tier: ItemTier = ItemTier.Tier1
    quick_sell: int = 400
    weight: float = 10.2
    can_be_modified: bool = True
    caliber: str = "5.45x39mm"
    damage: int = 20
    range: int = 200
    accuracy: int = 40
    reload_speed: float = 4.8
    fire_rate: float = 2.4
    magazine_size: int = 30
    armor_penetration: int = 22
    headshot_chance: int = 25
    agility_adj: float = -6.0
    allowed_modifications: dict = {
        "Foregrip": [
            "Compact Foregrip",
            "Heavy Duty Grip",
            "Precision Long Grip",
            "Tactical Short Grip",
            "Vertical Tilt Grip"
        ],
        "Scope": [
            "Holographic (1x)",
            "Holographic (1x-4x)"
        ]
    }


weapon_classes = [
    M1911,
    BerettaM9,
    SawedOffShotgun,
    M890,
    M4Carbine,
    HoneyBadger,
    AK74
]

