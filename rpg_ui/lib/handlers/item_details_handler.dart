import 'package:flutter/material.dart';
import 'package:rpg_ui/common_imports.dart';
import 'package:rpg_ui/api_calls/items_api.dart';
import '../widgets/item_details_dialogue.dart';
import '../models/item_model.dart';
import '../widgets/item_tile.dart';

class ItemDetailsHandler {
  static void showItemDetails(BuildContext context, Item item, {bool isSelling = false, required VoidCallback onTransactionComplete}) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return ItemDetailsDialog(
          item: item,
          showBuyButton: !isSelling,
          showSellButton: isSelling,
          onBuy: () async {
            await ItemManager.buyItem(item.itemId, 1);
            onTransactionComplete();
            Navigator.pop(context);
          },
          onSell: () async {
            await ItemManager.sellItem(item.itemId, 1);
            onTransactionComplete();
            Navigator.pop(context);
          },
        );
      },
    );
  }
}

class GridBuilder {
  static Widget buildItemGrid(List<Item> items, Function(Item) onTap) {
    return GridView.builder(
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 3,
        childAspectRatio: 1,
        crossAxisSpacing: 8,
        mainAxisSpacing: 8,
      ),
      itemCount: items.length,
      itemBuilder: (context, index) {
        return ItemTile(
          item: items[index],
          onTap: () => onTap(items[index]),
          bottomInfoKeys: const ['quantity', 'item_cost'],
        );
      },
    );
  }
}

