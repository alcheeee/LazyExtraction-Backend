import 'package:flutter/material.dart';
import '../common_imports.dart';
import '../api_calls/items_api.dart';
import '../widgets/item_tile.dart';
import '../widgets/item_details_dialogue.dart';

class MarketScreen extends StatefulWidget {
  const MarketScreen({super.key});

  @override
  _MarketScreenState createState() => _MarketScreenState();
}

class _MarketScreenState extends State<MarketScreen> {
  final GlobalKey<ScaffoldState> _scaffoldKey = GlobalKey<ScaffoldState>();
  List<Item> _marketItems = [];
  String _message = '';

  Future<void> fetchMarketItems() async {
    try {
      List<Item> marketItems = await ItemManager.fetchMarketItems();
      setState(() {
        _marketItems = marketItems;
      });
    } catch (e) {
      setState(() {
        _message = e.toString();
      });
    }
  }

  void buyItem(Item item) async {
    try {
      String result = await ItemManager.buyItem(item.itemId, 1);
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(result)));
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(e.toString())));
    }
  }

  void _showItemDetails(Item item) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return ItemDetailsDialog(
          item: item,
          showBuyButton: true,
          onBuy: () => buyItem(item),
        );
      },
    );
  }

  @override
  void initState() {
    super.initState();
    fetchMarketItems();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
            key: _scaffoldKey,
      appBar: commonAppBar('Market', _scaffoldKey, context),
      drawer: commonDrawer(context, 'MarketScreen'),
      body: Padding(
        padding: const EdgeInsets.all(8.0),
        child: GridView.builder(
          gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: 4,
            childAspectRatio: 1,
            crossAxisSpacing: 4,
            mainAxisSpacing: 4,
          ),
          itemCount: _marketItems.length,
          itemBuilder: (context, index) {
            return ItemTile(
              item: _marketItems[index],
              onTap: () => _showItemDetails(_marketItems[index]),
              bottomInfoKeys: const ['quantity', 'item_cost'],
            );
          },
        ),
      ),
    );
  }
}