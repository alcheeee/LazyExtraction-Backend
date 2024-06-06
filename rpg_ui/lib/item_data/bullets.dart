class ItemType {
  static const Bullets = 'Bullets';
}


class ItemTier {
  static const Tier1 = 'Tier1';
  static const Tier2 = 'Tier2';
  static const Tier3 = 'Tier3';
  static const Tier4 = 'Tier4';
  static const Tier5 = 'Tier5';
  static const Tier6 = 'Tier6';
}

final Map<String, Map<String, dynamic>> bulletsCatalog = {
    '9x19mm': {
        'item_name': '9x19mm',
        'texture': 'assets/items/placeholder_item.png',
        'category': ItemType.Bullets,
        'tier': ItemTier.Tier1,
        'quick_sell': 1,
        'armor_pen_adj': 0,
        'accuracy_adj': 0,
        'range_adj': 0,
        'damage_adj': 0,
        'fire_rate_adj': 0.0,
        'reload_speed_adj': 0.0
    },
    '9x19mm AP': {
        'item_name': '9x19mm AP',
        'texture': 'assets/items/placeholder_item.png',
        'category': ItemType.Bullets,
        'tier': ItemTier.Tier2,
        'quick_sell': 2,
        'armor_pen_adj': 5,
        'accuracy_adj': 0,
        'range_adj': 5,
        'damage_adj': 2,
        'fire_rate_adj': 0.0,
        'reload_speed_adj': -0.1
    },
    '12 Gauge': {
        'item_name': '12 Gauge',
        'texture': 'assets/items/placeholder_item.png',
        'category': ItemType.Bullets,
        'tier': ItemTier.Tier1,
        'quick_sell': 2,
        'armor_pen_adj': 0,
        'accuracy_adj': 0,
        'range_adj': 0,
        'damage_adj': 10,
        'fire_rate_adj': 0.0,
        'reload_speed_adj': 0.0
    },
    '12 Gauge Slug': {
        'item_name': '12 Gauge Slug',
        'texture': 'assets/items/placeholder_item.png',
        'category': ItemType.Bullets,
        'tier': ItemTier.Tier2,
        'quick_sell': 3,
        'armor_pen_adj': 10,
        'accuracy_adj': 5,
        'range_adj': 10,
        'damage_adj': 15,
        'fire_rate_adj': 0.0,
        'reload_speed_adj': -0.1
    },
    '5.56x45mm NATO': {
        'item_name': '5.56x45mm NATO',
        'texture': 'assets/items/placeholder_item.png',
        'category': ItemType.Bullets,
        'tier': ItemTier.Tier2,
        'quick_sell': 3,
        'armor_pen_adj': 10,
        'accuracy_adj': 5,
        'range_adj': 10,
        'damage_adj': 5,
        'fire_rate_adj': 0.0,
        'reload_speed_adj': -0.1
    },
    '5.56x45mm NATO AP': {
        'item_name': '5.56x45mm NATO AP',
        'texture': 'assets/items/placeholder_item.png',
        'category': ItemType.Bullets,
        'tier': ItemTier.Tier3,
        'quick_sell': 4,
        'armor_pen_adj': 15,
        'accuracy_adj': 5,
        'range_adj': 15,
        'damage_adj': 10,
        'fire_rate_adj': 0.0,
        'reload_speed_adj': -0.1
    },
    '300 BLK': {
        'item_name': '300 BLK',
        'texture': 'assets/items/placeholder_item.png',
        'category': ItemType.Bullets,
        'tier': ItemTier.Tier3,
        'quick_sell': 4,
        'armor_pen_adj': 10,
        'accuracy_adj': 5,
        'range_adj': 10,
        'damage_adj': 7,
        'fire_rate_adj': 0.0,
        'reload_speed_adj': -0.1
    },
    '300 BLK AP': {
        'item_name': '300 BLK AP',
        'texture': 'assets/items/placeholder_item.png',
        'category': ItemType.Bullets,
        'tier': ItemTier.Tier4,
        'quick_sell': 5,
        'armor_pen_adj': 20,
        'accuracy_adj': 10,
        'range_adj': 20,
        'damage_adj': 12,
        'fire_rate_adj': 0.0,
        'reload_speed_adj': -0.1
    }
};
