class ItemType {
  static const Weapon = 'Weapon';
  static const Armor = 'Armor';
  static const Clothing = 'Clothing';
  static const Medical = 'Medical';
  static const Bullets = 'Bullets';
  static const Attachments = 'Attachments';
  static const Valuable = 'Valuable';
}

class ArmorType {
  static const Head = 'Head';
  static const Body = 'Body';
}

class ItemTier {
  static const Tier1 = 'Tier1';
  static const Tier2 = 'Tier2';
  static const Tier3 = 'Tier3';
  static const Tier4 = 'Tier4';
  static const Tier5 = 'Tier5';
}

final Map<String, Map<String, dynamic>> itemCatalog = {
  'M1911': {
    'item_name': 'M1911',
    'texture': 'assets/items/placeholder_item.png',
    'category': ItemType.Weapon,
    'tier': ItemTier.Tier1,
    'quick_sell': 150,
    'weight': 1.1,
    'max_durability': 100.0,
    'current_durability': 100.0,
    'caliber': '9x19mm',
    'damage': 7,
    'strength': 0.0,
    'range': 50,
    'accuracy': 60,
    'reload_speed': 2.0,
    'fire_rate': 1.2,
    'magazine_size': 7,
    'armor_penetration': 0,
    'headshot_chance': 15,
    'agility_penalty': -0.5,
    'allowed_attachments': {
      "Muzzle": "Flash Suppressor",
      "Magazine": "Extended Magazine",
      "Laser": "Tactical Laser"
    },
    'attachments': {},
  },
  // Add the rest of the items from your catalogs here...
};
