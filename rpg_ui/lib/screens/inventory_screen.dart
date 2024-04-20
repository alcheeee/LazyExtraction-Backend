import '../common_imports.dart';
import '../api_calls/items_api.dart';
import 'package:flutter/material.dart';
import '../widgets/item_tile.dart';
import '../widgets/item_details_dialogue.dart';

class InventoryScreen extends StatefulWidget {
  const InventoryScreen({super.key});

  @override
  _InventoryScreenState createState() => _InventoryScreenState();
}

class _InventoryScreenState extends State<InventoryScreen> {
  final GlobalKey<ScaffoldState> _scaffoldKey = GlobalKey<ScaffoldState>();
  List<Item> _inventoryItems = [];
  Map<String, Item?> _equippedItems = {
    'Mask': null,
    'Body': null,
    'Legs': null,
    'Weapon': null
  };
  String _message = '';

  void fetchInventory() async {
  try {
    List<Item> inventoryItems = await ItemManager.fetchInventory();
    setState(() {
      _inventoryItems = inventoryItems.where((item) => item.equippedSlot == null).toList();
      _equippedItems = {};
      for (var item in inventoryItems.where((item) => item.equippedSlot != null)) {
        _equippedItems[item.equippedSlot!] = item;
      }
    });
  } catch (e) {
    setState(() {
      _message = e.toString();
    });
  }
}

void toggleEquipItem(Item item) async {
  String message = await ItemManager.equipItem(item.itemId);
  if (!mounted) return;
  ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(message)));
  fetchInventory();
}

  void _showItemDetails(Item item) {
    showDialog(
      context: context,
      builder: (BuildContext context) => ItemDetailsDialog(
        item: item,
        showEquipButton: item.slotType != null,
        onEquip: () => toggleEquipItem(item),
      ),
    );
  }

  @override
  void initState() {
    super.initState();
    fetchInventory();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      key: _scaffoldKey,
      appBar: commonAppBar('Inventory', _scaffoldKey, context),
      drawer: commonDrawer(context, 'InventoryScreen'),
      body: Padding(
        padding: const EdgeInsets.all(8.0),
        child: Column(
          children: [
            SizedBox(
              height: 120,
              child: Padding(
              padding: const EdgeInsets.only(bottom: 20),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: _equippedItems.entries.map((entry) {
                    Item? item = entry.value;
                    return Expanded(
                      child: GestureDetector(
                        onTap: () => item != null ? _showItemDetails(item) : null,
                        child: Container(
                          margin: const EdgeInsets.symmetric(horizontal: 4),
                          padding: const EdgeInsets.all(8),
                          decoration: BoxDecoration(
                            color: UIColors.secondaryBackgroundColor.withOpacity(0.8),
                            border: Border.all(color: UIColors.primaryOutlineColor, width: 2),
                            borderRadius: BorderRadius.circular(8),
                            boxShadow: [
                              BoxShadow(
                                color: Colors.black.withOpacity(0.15),
                                spreadRadius: 1,
                                blurRadius: 4,
                                offset: const Offset(0, 2),
                              ),
                            ],
                          ),
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Icon(
                                item != null ? Icons.check_circle_outline : Icons.remove_circle_outline,
                                color: item != null ? Colors.green : Colors.red,
                                size: 24,
                              ),
                              Text(
                                entry.key,
                                style: const TextStyle(
                                  color: UIColors.primaryTextColor,
                                  fontSize: 14,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                              Text(
                                item?.itemName ?? 'Empty',
                                style: const TextStyle(
                                  color: UIColors.secondaryTextColor,
                                  fontSize: 12,
                                  fontStyle: FontStyle.italic,
                                ),
                                overflow: TextOverflow.ellipsis,
                              ),
                            ],
                          ),
                        ),
                      ),
                    );
                  }).toList(),
                ),
              )
            ),
            Expanded(
              child: GridView.builder(
                gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: 4,
                  childAspectRatio: 1,
                  crossAxisSpacing: 4,
                  mainAxisSpacing: 4,
                ),
                itemCount: _inventoryItems.length,
                itemBuilder: (context, index) {
                  return ItemTile(
                    item: _inventoryItems[index],
                    bottomInfoKeys: const ['quantity'],
                    onTap: () => _showItemDetails(_inventoryItems[index]),
                  );
                },
              ),
            ),
            Text(_message, style: const TextStyle(color: UIColors.secondaryTextColor)),
          ],
        ),
      ),
    );
  }
}