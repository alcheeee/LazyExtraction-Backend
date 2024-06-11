import 'package:flutter/material.dart';
import '../models/user_inventory.dart';
import '../item_data/item_utils.dart';

class InventoryUtils {
  static Map<String, List<InventoryItem>> sortItemsByCategory(List<InventoryItem> items) {
    final Map<String, List<InventoryItem>> categorizedItems = {};

    for (var item in items) {
      if (!categorizedItems.containsKey(item.category)) {
        categorizedItems[item.category] = [];
      }
      categorizedItems[item.category]!.add(item);
    }

    return categorizedItems;
  }

  static Widget buildCategorySection(BuildContext context, String category, List<InventoryItem> items, Function(InventoryItem) showItemDetailsPopup) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          category,
          style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
        ),
        const SizedBox(height: 10),
        Wrap(
          spacing: 10.0,
          runSpacing: 10.0,
          children: items.map((item) {
            final itemDetails = getItemByName(item.itemName);

            return GestureDetector(
              onTap: () {
                showItemDetailsPopup(item);
              },
              child: Column(
                children: [
                  Image.asset(itemDetails?['texture'] ?? 'assets/items/placeholder_item.png', height: 40, width: 40),
                  Text(item.itemName, style: const TextStyle(fontSize: 16)),
                  Text('Qty: ${item.quantity}', style: const TextStyle(fontSize: 14)),
                ],
              ),
            );
          }).toList(),
        ),
        const SizedBox(height: 20),
      ],
    );
  }
}
