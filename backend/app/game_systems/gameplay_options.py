from enum import Enum

JOB_TYPES = ['General', 'Law', 'Crime']

# USER DEFAULTS
default_stats_data = {
    'level': 1.00,
    'reputation': 0,
    'max_energy': 100,
    'damage': 1,
    'evasiveness': 1.00,
    'health': 100,
    'luck': 1.00,
    'strength': 1.00,
    'knowledge': 1.00
}

default_inventory_data = {
    'bank': 1000,
    'energy': 100
}

equipment_map = {
    "Weapon": "equipped_weapon_id",
    "Mask": "equipped_mask_id",
    "Body": "equipped_body_id",
    "Legs": "equipped_legs_id"
}

item_bonus_mapper = {
    "reputation": "reputation_bonus",
    "max_energy": "max_energy_bonus",
    "damage": "damage_bonus",
    "evasiveness": "evasiveness_bonus",
    "health": "health_bonus",
    "luck": "luck_bonus",
    "strength": "strength_bonus",
    "knowledge": "knowledge_bonus",
}

class CORPORATION_TYPES(Enum):
    Industrial = 'Industrial'
    Law = 'Law'
    Criminal = 'Criminal'





