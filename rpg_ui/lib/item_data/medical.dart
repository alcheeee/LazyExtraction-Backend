class ItemType {
  static const Medical = 'Medical';
}


class ItemTier {
  static const Tier1 = 'Tier1';
  static const Tier2 = 'Tier2';
  static const Tier3 = 'Tier3';
  static const Tier4 = 'Tier4';
  static const Tier5 = 'Tier5';
  static const Tier6 = 'Tier6';
}

final Map<String, Map<String, dynamic>> medicalCatalog = {
    'Gauze': {
        'item_name': 'Gauze',
        'texture': 'assets/items/placeholder_item.png',
        'category': ItemType.Medical,
        'tier': ItemTier.Tier1,
        'quick_sell': 60,
        'health_increase': 6
    },
    'Compression Bandage': {
        'item_name': 'Compression Bandage',
        'texture': 'assets/items/placeholder_item.png',
        'category': ItemType.Medical,
        'tier': ItemTier.Tier2,
        'quick_sell': 100,
        'health_increase': 8
    },
    'Tylopain': {
        'item_name': 'Tylopain',
        'texture': 'assets/items/placeholder_item.png',
        'category': ItemType.Medical,
        'tier': ItemTier.Tier1,
        'quick_sell': 80,
        'pain_reduction': 6,
        'amount_of_actions': 3
    },
    'Morphine': {
        'item_name': 'Morphine',
        'texture': 'assets/items/placeholder_item.png',
        'category': ItemType.Medical,
        'tier': ItemTier.Tier2,
        'quick_sell': 120,
        'pain_reduction': 10,
        'amount_of_actions': 1
    },
    'Adrenaline': {
        'item_name': 'Adrenaline',
        'texture': 'assets/items/placeholder_item.png',
        'category': ItemType.Medical,
        'tier': ItemTier.Tier2,
        'quick_sell': 200,
        'agility_bonus': 10,
        'strength_bonus': 5,
        'amount_of_actions': 1
    },
    'Ephedrine': {
        'item_name': 'Ephedrine',
        'texture': 'assets/items/placeholder_item.png',
        'category': ItemType.Medical,
        'tier': ItemTier.Tier1,
        'quick_sell': 150,
        'agility_bonus': 5,
        'strength_bonus': 3,
        'amount_of_actions': 2
    },
    'First Aid Kit': {
        'item_name': 'First Aid Kit',
        'texture': 'assets/items/placeholder_item.png',
        'category': ItemType.Medical,
        'tier': ItemTier.Tier2,
        'quick_sell': 300,
        'health_increase': 20,
        'pain_reduction': 5,
        'amount_of_actions': 1
    },
    'Advanced First Aid Kit': {
        'item_name': 'Advanced First Aid Kit',
        'texture': 'assets/items/placeholder_item.png',
        'category': ItemType.Medical,
        'tier': ItemTier.Tier3,
        'quick_sell': 500,
        'health_increase': 30,
        'pain_reduction': 10,
        'amount_of_actions': 1
    },
    'Steroid Injection': {
        'item_name': 'Steroid Injection',
        'texture': 'assets/items/placeholder_item.png',
        'category': ItemType.Medical,
        'tier': ItemTier.Tier3,
        'quick_sell': 400,
        'strength_bonus': 10,
        'agility_bonus': 5,
        'amount_of_actions': 1
    },
    'Pain Relief Injection': {
        'item_name': 'Pain Relief Injection',
        'texture': 'assets/items/placeholder_item.png',
        'category': ItemType.Medical,
        'tier': ItemTier.Tier2,
        'quick_sell': 250,
        'pain_reduction': 15,
        'amount_of_actions': 1
    }
};