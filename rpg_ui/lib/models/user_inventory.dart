// lib/models/user_inventory.dart

class Inventory {
  List<InventoryItem> items;
  InventoryItem? _equippedWeapon;
  InventoryItem? _equippedHelmet;
  InventoryItem? _equippedChest;
  InventoryItem? _equippedLegs;
  int bank;
  int energy;
  double currentWeight;

  Inventory({
    required this.items,
    InventoryItem? equippedWeapon,
    InventoryItem? equippedHelmet,
    InventoryItem? equippedChest,
    InventoryItem? equippedLegs,
    required this.bank,
    required this.energy,
    required this.currentWeight,
  })  : _equippedWeapon = equippedWeapon,
        _equippedHelmet = equippedHelmet,
        _equippedChest = equippedChest,
        _equippedLegs = equippedLegs;

  // Define setters for the equipped items
  set equippedWeapon(InventoryItem? item) {
    _equippedWeapon = item;
  }

  set equippedHelmet(InventoryItem? item) {
    _equippedHelmet = item;
  }

  set equippedChest(InventoryItem? item) {
    _equippedChest = item;
  }

  set equippedLegs(InventoryItem? item) {
    _equippedLegs = item;
  }

  // Define getters for the equipped items
  InventoryItem? get equippedWeapon => _equippedWeapon;
  InventoryItem? get equippedHelmet => _equippedHelmet;
  InventoryItem? get equippedChest => _equippedChest;
  InventoryItem? get equippedLegs => _equippedLegs;

  // Define fromJson method
  factory Inventory.fromJson(Map<String, dynamic> json) {
    return Inventory(
      items: (json['user-inventory'] as List<dynamic>)
          .map((item) => InventoryItem.fromJson(item))
          .toList(),
      equippedWeapon: json['equipped_weapon'] != null
          ? InventoryItem.fromJson(json['equipped_weapon'])
          : null,
      equippedHelmet: json['equipped_helmet'] != null
          ? InventoryItem.fromJson(json['equipped_helmet'])
          : null,
      equippedChest: json['equipped_chest'] != null
          ? InventoryItem.fromJson(json['equipped_chest'])
          : null,
      equippedLegs: json['equipped_legs'] != null
          ? InventoryItem.fromJson(json['equipped_legs'])
          : null,
      bank: json['bank'] ?? 0,
      energy: json['energy'] ?? 0,
      currentWeight: (json['currentWeight'] ?? 0).toDouble(),
    );
  }
}

class InventoryItem {
  final int id;
  final String itemName;
  final String category;
  final int itemId;
  final bool inStash;
  final double weight;
  int quantity;
  final int inventoryId;

  InventoryItem({
    required this.id,
    required this.itemName,
    required this.category,
    required this.itemId,
    required this.inStash,
    required this.weight,
    required this.quantity,
    required this.inventoryId,
  });

  factory InventoryItem.fromJson(Map<String, dynamic> json) {
    return InventoryItem(
      id: json['id'] ?? 0,
      itemName: json['item_name'] ?? '',
      category: json['category'] ?? '',
      itemId: json['item_id'] ?? 0,
      inStash: json['in_stash'] ?? false,
      weight: (json['weight'] ?? 0).toDouble(),
      quantity: json['quantity'] ?? 0,
      inventoryId: json['inventory_id'] ?? 0,
    );
  }
}

final Map<String, dynamic> sampleJson = {
  "status": "success",
  "message": "",
  "bank": 1000,
  "energy": 100,
  "currentWeight": 0,
  "equipped_helmet": {
    "id": 10,
    "item_name": "Tactical Helmet",
    "category": "Armor",
    "item_id": 30,
    "in_stash": false,
    "weight": 1.5,
    "quantity": 1,
    "inventory_id": 1,
  },
  "equipped_chest": {
    "id": 11,
    "item_name": "Heavy Duty Vest",
    "category": "Armor",
    "item_id": 31,
    "in_stash": false,
    "weight": 3.0,
    "quantity": 1,
    "inventory_id": 1,
  },
  "equipped_legs": null,
  "equipped_weapon": {
    "id": 13,
    "item_name": "M4A1 Carbine",
    "category": "Weapon",
    "item_id": 33,
    "in_stash": false,
    "weight": 3.5,
    "quantity": 1,
    "inventory_id": 1,
  },
  "user-inventory": [
    {
      "in_stash": false,
      "quantity": 39,
      "inventory_id": 1,
      "weight": 0,
      "id": 4,
      "item_id": 13,
      "item_name": "9x19mm",
      "category": "Bullets"
    },
    {
      "in_stash": false,
      "quantity": 1,
      "inventory_id": 1,
      "weight": 0,
      "id": 2,
      "item_id": 15,
      "item_name": "12 Gauge",
      "category": "Bullets"
    },
    {
      "in_stash": true,
      "quantity": 3,
      "inventory_id": 1,
      "weight": 0,
      "id": 1,
      "item_id": 15,
      "item_name": "12 Gauge",
      "category": "Bullets"
    },
    {
      "in_stash": false,
      "quantity": 1,
      "inventory_id": 1,
      "weight": 0,
      "id": 5,
      "item_id": 16,
      "item_name": "12 Gauge Slug",
      "category": "Bullets"
    },
    {
      "in_stash": false,
      "quantity": 2,
      "inventory_id": 1,
      "weight": 0,
      "id": 3,
      "item_id": 21,
      "item_name": "Gauze",
      "category": "Medical"
    }
  ]
};

final Inventory exampleInventory = Inventory.fromJson(sampleJson);
