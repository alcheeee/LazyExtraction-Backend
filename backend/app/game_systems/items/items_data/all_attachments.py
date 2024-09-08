from .. import (
    ItemType,
    ItemTier,
    AttachmentTypes
)


attachment_items = {
    'Bipod': {
        'Polymer Rifle Bipod': {
            'item_name': 'Polymer Rifle Bipod',
            'category': ItemType.Attachments,
            'tier': ItemTier.Tier4,
            'quick_sell': 800,
            'type': AttachmentTypes.Bipod,
            'weight_adj': 0.0,
            'damage_adj': 0,
            'range_adj': 0,
            'accuracy_adj': 0,
            'reload_speed_adj': 0.0,
            'fire_rate_adj': 0.0,
            'magazine_size_adj': 0,
            'headshot_chance_adj': 0,
            'agility_penalty_adj': 0.0
        },
    },
    'FrontGrip': {
        'Tactical Front Grip': {
            'item_name': 'Tactical Front Grip',
            'category': ItemType.Attachments,
            'tier': ItemTier.Tier3,
            'quick_sell': 500,
            'type': AttachmentTypes.FrontGrip,
            'weight_adj': -0.1,
            'damage_adj': 0,
            'range_adj': 0,
            'accuracy_adj': 10,
            'reload_speed_adj': -0.1,
            'fire_rate_adj': 0.0,
            'magazine_size_adj': 0,
            'headshot_chance_adj': 0,
            'agility_penalty_adj': -0.1
        },
    },
    'Muzzle': {
        'Flash Suppressor': {
            'item_name': 'Flash Suppressor',
            'category': ItemType.Attachments,
            'tier': ItemTier.Tier2,
            'quick_sell': 400,
            'type': AttachmentTypes.Muzzle,
            'weight_adj': 0.0,
            'damage_adj': 0,
            'range_adj': 5,
            'accuracy_adj': 5,
            'reload_speed_adj': 0.0,
            'fire_rate_adj': 0.0,
            'magazine_size_adj': 0,
            'headshot_chance_adj': 0,
            'agility_penalty_adj': 0.0
        },
    },
    'Magazine': {
        'Extended Magazine': {
            'item_name': 'Extended Magazine',
            'category': ItemType.Attachments,
            'tier': ItemTier.Tier3,
            'quick_sell': 600,
            'type': AttachmentTypes.Magazine,
            'weight_adj': 0.2,
            'damage_adj': 0,
            'range_adj': 0,
            'accuracy_adj': 0,
            'reload_speed_adj': -0.2,
            'fire_rate_adj': 0.0,
            'magazine_size_adj': 15,
            'headshot_chance_adj': 0,
            'agility_penalty_adj': -0.2
        },
    },
    'Stock': {
        'Adjustable Stock': {
            'item_name': 'Adjustable Stock',
            'category': ItemType.Attachments,
            'tier': ItemTier.Tier2,
            'quick_sell': 450,
            'type': AttachmentTypes.Stock,
            'weight_adj': -0.1,
            'damage_adj': 0,
            'range_adj': 0,
            'accuracy_adj': 8,
            'reload_speed_adj': 0.0,
            'fire_rate_adj': 0.0,
            'magazine_size_adj': 0,
            'headshot_chance_adj': 0,
            'agility_penalty_adj': -0.1
        },
    },
    'Scope': {
        'Sniper Scope': {
            'item_name': 'Sniper Scope',
            'category': ItemType.Attachments,
            'tier': ItemTier.Tier4,
            'quick_sell': 1000,
            'type': AttachmentTypes.Scope,
            'weight_adj': 0.3,
            'damage_adj': 0,
            'range_adj': 50,
            'accuracy_adj': 20,
            'reload_speed_adj': 0.0,
            'fire_rate_adj': 0.0,
            'magazine_size_adj': 0,
            'headshot_chance_adj': 5,
            'agility_penalty_adj': -0.3
        },
    },
    'Laser': {
        'Tactical Laser': {
            'item_name': 'Tactical Laser',
            'category': ItemType.Attachments,
            'tier': ItemTier.Tier3,
            'quick_sell': 700,
            'type': AttachmentTypes.Laser,
            'weight_adj': 0.1,
            'damage_adj': 0,
            'range_adj': 0,
            'accuracy_adj': 10,
            'reload_speed_adj': 0.0,
            'fire_rate_adj': 0.0,
            'magazine_size_adj': 0,
            'headshot_chance_adj': 0,
            'agility_penalty_adj': -0.1
        },
    },
    'Barrel': {
        'Long Barrel': {
            'item_name': 'Long Barrel',
            'category': ItemType.Attachments,
            'tier': ItemTier.Tier3,
            'quick_sell': 900,
            'type': AttachmentTypes.Barrel,
            'weight_adj': 0.3,
            'damage_adj': 0,
            'range_adj': 25,
            'accuracy_adj': 15,
            'reload_speed_adj': 0.0,
            'fire_rate_adj': 0.0,
            'magazine_size_adj': 0,
            'headshot_chance_adj': 0,
            'agility_penalty_adj': -0.2
        },
    },
}
