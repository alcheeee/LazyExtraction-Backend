class ItemType {
  static const Attachments = 'Attachments';
}

class AttachmentTypes {
  static const Bipod = 'bipod';
  static const FrontGrip = 'front_grip';
  static const Muzzle = 'muzzle';
  static const Magazine = 'magazine';
  static const Stock = 'stock';
  static const Laser = 'laser';
  static const Barrel = 'barrel';
  static const Scope = "scope";
}

class ItemTier {
  static const Tier1 = 'Tier1';
  static const Tier2 = 'Tier2';
  static const Tier3 = 'Tier3';
  static const Tier4 = 'Tier4';
  static const Tier5 = 'Tier5';
  static const Tier6 = 'Tier6';
}


final Map<String, Map<String, dynamic>> attachmentsCatalog = {
    'Polymer Rifle Bipod': {
      'item_name': 'Polymer Rifle Bipod',
      'texture': 'assets/items/placeholder_item.png',
      'category': ItemType.Attachments,
      'tier': ItemTier.Tier4,
      'quick_sell': 800,
      'type': AttachmentTypes.Bipod,
      'weight_adj': 0.0,
      'max_durability_adj': 0,
      'damage_adj': 0,
      'range_adj': 0,
      'accuracy_adj': 0,
      'reload_speed_adj': 0.0,
      'fire_rate_adj': 0.0,
      'magazine_size_adj': 0,
      'headshot_chance_adj': 0,
      'agility_penalty_adj': 0.0
    },
    'Tactical Front Grip': {
      'item_name': 'Tactical Front Grip',
      'texture': 'assets/items/placeholder_item.png',
      'category': ItemType.Attachments,
      'tier': ItemTier.Tier3,
      'quick_sell': 500,
      'type': AttachmentTypes.FrontGrip,
      'weight_adj': -0.1,
      'max_durability_adj': 0,
      'damage_adj': 0,
      'range_adj': 0,
      'accuracy_adj': 10,
      'reload_speed_adj': -0.1,
      'fire_rate_adj': 0.0,
      'magazine_size_adj': 0,
      'headshot_chance_adj': 0,
      'agility_penalty_adj': -0.1
    },
    'Flash Suppressor': {
      'item_name': 'Flash Suppressor',
      'texture': 'assets/items/placeholder_item.png',
      'category': ItemType.Attachments,
      'tier': ItemTier.Tier2,
      'quick_sell': 400,
      'type': AttachmentTypes.Muzzle,
      'weight_adj': 0.0,
      'max_durability_adj': 0,
      'damage_adj': 0,
      'range_adj': 5,
      'accuracy_adj': 5,
      'reload_speed_adj': 0.0,
      'fire_rate_adj': 0.0,
      'magazine_size_adj': 0,
      'headshot_chance_adj': 0,
      'agility_penalty_adj': 0.0
    },
    'Extended Magazine': {
      'item_name': 'Extended Magazine',
      'texture': 'assets/items/placeholder_item.png',
      'category': ItemType.Attachments,
      'tier': ItemTier.Tier3,
      'quick_sell': 600,
      'type': AttachmentTypes.Magazine,
      'weight_adj': 0.2,
      'max_durability_adj': 0,
      'damage_adj': 0,
      'range_adj': 0,
      'accuracy_adj': 0,
      'reload_speed_adj': -0.2,
      'fire_rate_adj': 0.0,
      'magazine_size_adj': 15,
      'headshot_chance_adj': 0,
      'agility_penalty_adj': -0.2
    },
    'Adjustable Stock': {
      'item_name': 'Adjustable Stock',
      'texture': 'assets/items/placeholder_item.png',
      'category': ItemType.Attachments,
      'tier': ItemTier.Tier2,
      'quick_sell': 450,
      'type': AttachmentTypes.Stock,
      'weight_adj': -0.1,
      'max_durability_adj': 0,
      'damage_adj': 0,
      'range_adj': 0,
      'accuracy_adj': 8,
      'reload_speed_adj': 0.0,
      'fire_rate_adj': 0.0,
      'magazine_size_adj': 0,
      'headshot_chance_adj': 0,
      'agility_penalty_adj': -0.1
    },
    'Sniper Scope': {
      'item_name': 'Sniper Scope',
      'texture': 'assets/items/placeholder_item.png',
      'category': ItemType.Attachments,
      'tier': ItemTier.Tier4,
      'quick_sell': 1000,
      'type': AttachmentTypes.Scope,
      'weight_adj': 0.3,
      'max_durability_adj': 0,
      'damage_adj': 0,
      'range_adj': 50,
      'accuracy_adj': 20,
      'reload_speed_adj': 0.0,
      'fire_rate_adj': 0.0,
      'magazine_size_adj': 0,
      'headshot_chance_adj': 5,
      'agility_penalty_adj': -0.3
    },
    'Tactical Laser': {
      'item_name': 'Tactical Laser',
      'texture': 'assets/items/placeholder_item.png',
      'category': ItemType.Attachments,
      'tier': ItemTier.Tier3,
      'quick_sell': 700,
      'type': AttachmentTypes.Laser,
      'weight_adj': 0.1,
      'max_durability_adj': 0,
      'damage_adj': 0,
      'range_adj': 0,
      'accuracy_adj': 10,
      'reload_speed_adj': 0.0,
      'fire_rate_adj': 0.0,
      'magazine_size_adj': 0,
      'headshot_chance_adj': 0,
      'agility_penalty_adj': -0.1
    },
    'Long Barrel': {
      'item_name': 'Long Barrel',
      'texture': 'assets/items/placeholder_item.png',
      'category': ItemType.Attachments,
      'tier': ItemTier.Tier3,
      'quick_sell': 900,
      'type': AttachmentTypes.Barrel,
      'weight_adj': 0.3,
      'max_durability_adj': 0,
      'damage_adj': 0,
      'range_adj': 25,
      'accuracy_adj': 15,
      'reload_speed_adj': 0.0,
      'fire_rate_adj': 0.0,
      'magazine_size_adj': 0,
      'headshot_chance_adj': 0,
      'agility_penalty_adj': -0.2
    },
};
