import 'package:flutter/material.dart';
import '../models/user_inventory.dart';
import '../utils/inventory_utils.dart';
import '../widgets/item_details_widget.dart';
import '../item_data/item_utils.dart';

class InventoryScreen extends StatefulWidget {
  final Inventory inventory;

  const InventoryScreen({super.key, required this.inventory});

  @override
  _InventoryScreenState createState() => _InventoryScreenState();
}

class _InventoryScreenState extends State<InventoryScreen> with SingleTickerProviderStateMixin {
  late TabController _tabController;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 2, vsync: this);
  }

  void showItemDetailsPopup(InventoryItem item) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return Dialog(
          backgroundColor: Colors.grey[900],
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(10),
          ),
          child: Container(
            constraints: BoxConstraints(maxWidth: MediaQuery.of(context).size.width * 0.8),
            padding: const EdgeInsets.all(16.0),
            child: ItemDetailWidget(
              itemName: item.itemName,
              maxQuantity: item.quantity,
              onTransfer: (quantity) {
                Navigator.of(context).pop(); // Close the dialog
                _transferItem(item, quantity); // Pass the quantity to transfer
              },
              actions: [
                if (item.category == 'Weapon' || item.category == 'Armor') ...[
                  TextButton(
                    onPressed: () {
                      _equipItem(item);
                    },
                    child: const Text('Equip'),
                  ),
                ],
                if (!item.inStash) ...[
                  TextButton(
                    onPressed: () {
                      _unequipItem(item);
                    },
                    child: const Text('Unequip'),
                  ),
                ],
              ],
            ),
          ),
        );
      },
    );
  }

  void _transferItem(InventoryItem item, int quantity) {
    setState(() {
      final newStatus = !item.inStash;
      final updatedItems = <InventoryItem>[];

      for (var i in widget.inventory.items) {
        if (i.id == item.id) {
          if (i.quantity > quantity) {
            updatedItems.add(InventoryItem(
              id: i.id,
              itemName: i.itemName,
              category: i.category,
              itemId: i.itemId,
              inStash: newStatus,
              weight: i.weight,
              quantity: quantity,
              inventoryId: i.inventoryId,
            ));
            updatedItems.add(InventoryItem(
              id: i.id,
              itemName: i.itemName,
              category: i.category,
              itemId: i.itemId,
              inStash: i.inStash,
              weight: i.weight,
              quantity: i.quantity - quantity,
              inventoryId: i.inventoryId,
            ));
          } else {
            updatedItems.add(InventoryItem(
              id: i.id,
              itemName: i.itemName,
              category: i.category,
              itemId: i.itemId,
              inStash: newStatus,
              weight: i.weight,
              quantity: i.quantity,
              inventoryId: i.inventoryId,
            ));
          }
        } else {
          updatedItems.add(i);
        }
      }

      widget.inventory.items.clear();
      widget.inventory.items.addAll(updatedItems);
    });
  }

  void _equipItem(InventoryItem item) {
    setState(() {
      switch (item.category) {
        case 'Weapon':
          widget.inventory.equippedWeapon = item;
          break;
        case 'Armor':
          if (item.itemName.contains('Helmet')) {
            widget.inventory.equippedHelmet = item;
          } else if (item.itemName.contains('Chest')) {
            widget.inventory.equippedChest = item;
          } else if (item.itemName.contains('Legs')) {
            widget.inventory.equippedLegs = item;
          }
          break;
        default:
          break;
      }

      if (item.quantity > 1) {
        item.quantity -= 1;
      } else {
        widget.inventory.items.remove(item);
      }
    });
    print('Equipped ${item.itemName}');
  }

  void _unequipItem(InventoryItem item) {
    setState(() {
      switch (item.category) {
        case 'Weapon':
          widget.inventory.equippedWeapon = null;
          break;
        case 'Armor':
          if (item.itemName.contains('Helmet')) {
            widget.inventory.equippedHelmet = null;
          } else if (item.itemName.contains('Chest')) {
            widget.inventory.equippedChest = null;
          } else if (item.itemName.contains('Legs')) {
            widget.inventory.equippedLegs = null;
          }
          break;
        default:
          break;
      }

      final existingItem = widget.inventory.items.firstWhere(
        (i) => i.id == item.id,
        orElse: () => InventoryItem(
          id: item.id,
          itemName: item.itemName,
          category: item.category,
          itemId: item.itemId,
          inStash: item.inStash,
          weight: item.weight,
          quantity: 0,
          inventoryId: item.inventoryId,
        ),
      );

      if (existingItem.quantity > 0) {
        existingItem.quantity += 1;
      } else {
        widget.inventory.items.add(item);
      }
    });
    print('Unequipped ${item.itemName}');
  }

  @override
  Widget build(BuildContext context) {
    final stashItems = widget.inventory.items.where((item) => item.inStash).toList();
    final playerItems = widget.inventory.items.where((item) => !item.inStash).toList();

    return Scaffold(
      appBar: TabBar(
        controller: _tabController,
        tabs: const [
          Tab(text: 'Stash'),
          Tab(text: 'Player'),
        ],
      ),
      body: TabBarView(
        controller: _tabController,
        children: [
          buildInventoryList(context, stashItems, 'Stash'),
          buildPlayerInventoryList(context, playerItems),
        ],
      ),
    );
  }

  Widget buildInventoryList(BuildContext context, List<InventoryItem> items, String title) {
    if (items.isEmpty) {
      return Center(child: Text('No items in $title'));
    }
    final categorizedItems = InventoryUtils.sortItemsByCategory(items) ?? {};

    return ListView(
      padding: const EdgeInsets.all(16.0),
      children: categorizedItems.entries.map((entry) {
        return InventoryUtils.buildCategorySection(context, entry.key, entry.value, showItemDetailsPopup);
      }).toList(),
    );
  }

  Widget buildPlayerInventoryList(BuildContext context, List<InventoryItem> items) {
    final equipment = {
      'Helmet': widget.inventory.equippedHelmet,
      'Chest': widget.inventory.equippedChest,
      'Legs': widget.inventory.equippedLegs,
      'Weapon': widget.inventory.equippedWeapon,
    };

    return Column(
      children: [
        ExpansionTile(
          title: const Text('Equipment', style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
          children: [
            Center(
              child: Column(
                children: [
                  equipmentSlot(context, 'Helmet', equipment['Helmet']),
                  const SizedBox(height: 10),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      equipmentSlot(context, 'Weapon', equipment['Weapon']),
                      const SizedBox(width: 20),
                      equipmentSlot(context, 'Chest', equipment['Chest']),
                    ],
                  ),
                  const SizedBox(height: 10),
                  equipmentSlot(context, 'Legs', equipment['Legs']),
                ],
              ),
            ),
          ],
        ),
        const SizedBox(height: 20),
        const Divider(),
        Expanded(
          child: buildInventoryList(context, items, 'Player Inventory'),
        ),
      ],
    );
  }

  Widget equipmentSlot(BuildContext context, String slotName, InventoryItem? item) {
    return GestureDetector(
      onTap: () {
        if (item != null) {
          showItemDetailsPopup(item);
        }
      },
      child: Column(
        children: [
          Container(
            width: 60, // Reduced size
            height: 60, // Reduced size
            decoration: BoxDecoration(
              color: Colors.grey[800],
              borderRadius: BorderRadius.circular(10),
              border: Border.all(color: Colors.white, width: 2),
            ),
            child: item != null
                ? Image.asset(getItemByName(item.itemName)?['texture'] ?? 'assets/items/placeholder_item.png')
                : Center(child: Text(slotName, style: const TextStyle(color: Colors.white))),
          ),
          const SizedBox(height: 5),
          Text(slotName, style: const TextStyle(fontSize: 14, color: Colors.white)), // Smaller font size
        ],
      ),
    );
  }
}
