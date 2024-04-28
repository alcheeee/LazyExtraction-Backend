from enum import Enum

class ItemType(Enum):
    Drug = "Drug"
    Weapon = "Weapon"
    Clothing = "Clothing"
    Other = "Other"


class ItemQuality(Enum):
    Junk = 'Junk'
    Common = 'Common'
    Uncommon = 'Uncommon'
    Rare = 'Rare'
    Special = 'Special'
    Unique = 'Unique'
