class ItemType {
  static const Armor = 'Armor';
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
  static const Tier6 = 'Tier6';
}

final Map<String, Map<String, dynamic>> armorCatalog = {
    'Tactical Helmet': {
        'item_name': 'Tactical Helmet',
        'texture': 'assets/items/placeholder_item.png',
        'category': ItemType.Armor,
        'tier': ItemTier.Tier1,
        'quick_sell': 500,
        'type': ArmorType.Head,
        'max_durability': 80,
        'current_durability': 80,
        'weight': 1.5,
        'head_protection': 15,
        'chest_protection': 0,
        'stomach_protection': 0,
        'arm_protection': 0,
        'agility_penalty': -0.1
    },
    'Combat Helmet': {
        'item_name': 'Combat Helmet',
        'texture': 'assets/items/placeholder_item.png',
        'category': ItemType.Armor,
        'tier': ItemTier.Tier2,
        'quick_sell': 1000,
        'type': ArmorType.Head,
        'max_durability': 120,
        'current_durability': 120,
        'weight': 2.0,
        'head_protection': 25,
        'chest_protection': 0,
        'stomach_protection': 0,
        'arm_protection': 0,
        'agility_penalty': -0.15
    },
    'Advanced Combat Helmet': {
        'item_name': 'Advanced Combat Helmet',
        'texture': 'assets/items/placeholder_item.png',
        'category': ItemType.Armor,
        'tier': ItemTier.Tier3,
        'quick_sell': 2000,
        'type': ArmorType.Head,
        'max_durability': 150,
        'current_durability': 150,
        'weight': 2.5,
        'head_protection': 35,
        'chest_protection': 0,
        'stomach_protection': 0,
        'arm_protection': 0,
        'agility_penalty': -0.2
    },
    'Lightweight Vest': {
        'item_name': 'Lightweight Vest',
        'texture': 'assets/items/placeholder_item.png',
        'category': ItemType.Armor,
        'tier': ItemTier.Tier1,
        'quick_sell': 750,
        'type': ArmorType.Body,
        'max_durability': 100,
        'current_durability': 100,
        'weight': 3.0,
        'head_protection': 0,
        'chest_protection': 20,
        'stomach_protection': 10,
        'arm_protection': 5,
        'agility_penalty': -0.2
    },
    'Tactical Vest': {
        'item_name': 'Tactical Vest',
        'texture': 'assets/items/placeholder_item.png',
        'category': ItemType.Armor,
        'tier': ItemTier.Tier2,
        'quick_sell': 1500,
        'type': ArmorType.Body,
        'max_durability': 150,
        'current_durability': 150,
        'weight': 4.0,
        'head_protection': 0,
        'chest_protection': 30,
        'stomach_protection': 20,
        'arm_protection': 10,
        'agility_penalty': -0.3
    },
    'Heavy Duty Vest': {
        'item_name': 'Heavy Duty Vest',
        'texture': 'assets/items/placeholder_item.png',
        'category': ItemType.Armor,
        'tier': ItemTier.Tier3,
        'quick_sell': 2500,
        'type': ArmorType.Body,
        'max_durability': 200,
        'current_durability': 200,
        'weight': 5.0,
        'head_protection': 0,
        'chest_protection': 40,
        'stomach_protection': 30,
        'arm_protection': 15,
        'agility_penalty': -0.4
    },
};
