// ignore_for_file: unused_import
import '../api_calls/item_manager.dart';
import 'package:flutter/material.dart';
import '../widgets/inventory_item_widget.dart';
import '../common_imports.dart';


class InventoryScreen extends StatefulWidget {
  const InventoryScreen({super.key});

  @override
  _InventoryScreenState createState() => _InventoryScreenState();
}

class _InventoryScreenState extends State<InventoryScreen> {
  final GlobalKey<ScaffoldState> _scaffoldKey = GlobalKey<ScaffoldState>();
  List<dynamic> _inventoryItems = [];
  String _message = '';

  void fetchInventory() async {
    try {
      var inventoryItems = await ItemManager.fetchInventory();
      setState(() {
        _inventoryItems = inventoryItems;
        _message = 'Inventory fetched successfully';
      });
    } catch (e) {
      setState(() {
        _message = e.toString();
      });
    }
  }

 void equipItem(int itemId) async {
    try {
      String message = await ItemManager.equipItem(itemId);
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(message)));
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(e.toString())));
    }
  }

  @override
  void initState() {
    super.initState();
    fetchInventory();
  }

  void _showItemDetails(BuildContext context, Map<String, dynamic> item) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return ItemDetailsDialog(
          context: context,
          item: item,
          showEquipButton: true,
          onEquip: () => equipItem(item['item_id']),
        );
      },
    );
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
                    onTap: () => _showItemDetails(context, _inventoryItems[index]),
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