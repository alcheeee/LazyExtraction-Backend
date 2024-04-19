// ignore_for_file: unused_import
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:rpg_ui/colors.dart';
import 'dart:convert';
import 'config.dart';
import 'widgets/button_widgets.dart';
import 'widgets/app_theme.dart';
import 'widgets/inventory_item_widget.dart';

class InventoryScreen extends StatefulWidget {
  const InventoryScreen({super.key});

  @override
  _InventoryScreenState createState() => _InventoryScreenState();
}

class _InventoryScreenState extends State<InventoryScreen> {
  List<dynamic> _inventoryItems = [];
  String _message = '';

  Future<void> fetchInventory() async {
    final response = await http.post(
      Uri.parse('${APIUrl.apiURL}/game/get-user-inventory'),
      headers: <String, String>{
        'Authorization': 'Bearer ${SessionManager.accessToken}',
      },
    );

    if (response.statusCode == 200) {
      setState(() {
        _inventoryItems = jsonDecode(response.body) as List<dynamic>;
        _message = 'Inventory fetched successfully';
      });
    } else {
      var data = jsonDecode(response.body);
      setState(() {
        _message = 'Failed to fetch inventory: ${data['detail']['message']}';
      });
    }
  }

  Future<void> equipItem(int itemId) async {
    try {
      var url = Uri.parse('${APIUrl.apiURL}/game/equip-item');
      var response = await http.post(
        url,
        headers: <String, String>{
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ${SessionManager.accessToken}',
        },
        body: jsonEncode({'item_id': itemId}),
      );

      if (!mounted) return;
      if (response.statusCode == 200) {
        var data = jsonDecode(response.body);
        ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
                content: Text(data['message'] ?? 'Item equipped successfully'))
        );
      } else {
        throw Exception('Failed to equip item');
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(e.toString()))
      );
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
      appBar: AppBar(title: const Text('Inventory')),
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
            Text(_message, style: const TextStyle(color: UIColors.secondaryTextColor),
            ),
          ],
        ),
      ),
    );
  }
}