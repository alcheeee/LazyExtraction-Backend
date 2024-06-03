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
}

class InventoryItem {
  final int id;
  final String name;
  final IconData icon;
  final bool inStash;
  final double weight;
  final int quantity;

  InventoryItem({
    required this.id,
    required this.name,
    required this.icon,
    required this.inStash,
    required this.weight,
    required this.quantity,
  });
}

final Inventory exampleInventory = Inventory(
  bank: 2000,
  energy: 80,
  currentWeight: 35,
  items: [
    InventoryItem(id: 1, name: "Sword", icon: Icons.security, inStash: true, weight: 10.0, quantity: 1),
    InventoryItem(id: 2, name: "Headset", icon: Icons.headset, inStash: true, weight: 5.0, quantity: 1),
    InventoryItem(id: 3, name: "Shield", icon: Icons.shield, inStash: true, weight: 7.0, quantity: 1),
  ],
);
