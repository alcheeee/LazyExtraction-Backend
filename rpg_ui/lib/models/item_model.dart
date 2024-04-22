import 'package:flutter/material.dart';

class Item {
  final int itemId;
  final String itemName;
  final String itemQuality;
  final int quantity;
  final bool illegal;
  final String category;
  final String? slotType;
  String? equippedSlot;
  final Map<String, dynamic>? stats;
  final String itemAsset;
  final int? itemCost;
  final int? sellPrice;

  Item({
    required this.itemId,
    required this.itemName,
    required this.itemQuality,
    required this.quantity,
    required this.illegal,
    required this.category,
    required this.itemAsset,
    this.slotType,
    this.equippedSlot,
    this.stats,
    this.itemCost,
    this.sellPrice,
  });

  Map<String, dynamic> toMap() {
    return {
      'item_id': itemId,
      'item_name': itemName,
      'item_quality': itemQuality,
      'quantity': quantity,
      'item_cost': itemCost,
      'sell_price': sellPrice,
      'illegal': illegal,
      'category': category,
      'slot_type': slotType,
      'equipped_slot': equippedSlot,
      'stats': stats,
    };
  }

  factory Item.fromJson(Map<String, dynamic> json) {
    return Item(
      itemId: json['item_id'],
      itemName: json['item_name'],
      itemQuality: json['item_quality'],
      quantity: json['quantity'],
      illegal: json['illegal'],
      category: json['category'],
      slotType: json['slot_type'],
      equippedSlot: json['equipped_slot'],
      stats: json['stats'],
      itemAsset: 'assets/placeholder_item.png', // Placeholder
      itemCost: json['item_cost'],
      sellPrice: json['item_price'],
    );
  }

  Color get qualityColor => _getColorForQuality(itemQuality);
  Color _getColorForQuality(String quality) {
    switch (quality) {
      case 'Unique': return const Color(0xfffff533);
      case 'Special': return const Color(0xff7400a5);
      case 'Rare': return const Color(0xff232eff);
      case 'Uncommon': return const Color(0xff008e35);
      case 'Common': return const Color(0xffa5a5a5);
      case 'Junk':default: return const Color(0xff737373);
    }
  }

  Map<String, dynamic>? additionalDetails;
  dynamic getPropertyValue(String key) {
      switch(key) {
        case 'quantity':
          return quantity;
        case 'itemQuality':
          return itemQuality;
        case 'item_cost':
          return itemCost;
        case 'item_price':
          return sellPrice;
        default:
          return additionalDetails?[key];
      }
    }
}