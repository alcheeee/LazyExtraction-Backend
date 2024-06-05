import 'package:flutter/material.dart';

class Inventory {
  final int bank;
  final int energy;
  final int currentWeight;
  final List<InventoryItem> items;

  Inventory({
    required this.bank,
    required this.energy,
    required this.currentWeight,
    required this.items,
  });

  factory Inventory.fromJson(Map<String, dynamic> json) {
    return Inventory(
      bank: json['bank'] ?? 0,
      energy: json['energy'] ?? 0,
      currentWeight: json['currentWeight'] ?? 0,
      items: (json['user-inventory'] as List)
          .map((item) => InventoryItem.fromJson(item))
          .toList(),
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
  final int quantity;
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
