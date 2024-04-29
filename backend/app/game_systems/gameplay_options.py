from enum import Enum

JOB_TYPES = ['General', 'Law', 'Crime']

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





