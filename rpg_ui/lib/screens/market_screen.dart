import 'package:flutter/material.dart';
import '../common_imports.dart';
import '../api_calls/items_api.dart';
import '../widgets/item_tile.dart';
import '../widgets/item_details_dialogue.dart';
import '../handlers/item_details_handler.dart';

class MarketScreen extends StatefulWidget {
  const MarketScreen({super.key});

  @override
  _MarketScreenState createState() => _MarketScreenState();
}

class _MarketScreenState extends State<MarketScreen> with SingleTickerProviderStateMixin {
  final GlobalKey<ScaffoldState> _scaffoldKey = GlobalKey<ScaffoldState>();
  late TabController _tabController;
  List<Item> _marketItems = [];
  List<Item> _inventoryItems = [];
  String _message = '';

  final ItemManager _itemManager = ItemManager();

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 5, vsync: this);
    _initializeData();
  }

  void _initializeData() async {
    try {
      _marketItems = await ItemManager.fetchMarketItems();
      _inventoryItems = await ItemManager.fetchInventory();
      setState(() {});
    } catch (e) {
      setState(() {
        _message = e.toString();
      });
    }
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      key: _scaffoldKey,
      appBar: AppBar(
        title: const Text('Public Market'),
        bottom: buildTabBar(),
        backgroundColor: UIColors.primaryBackgroundColor,
        foregroundColor: UIColors.primaryTextColor,
      ),
      drawer: commonDrawer(context, 'MarketScreen'),
      body: buildTabViews(),
    );
  }

  TabBar buildTabBar() {
    return TabBar(
      controller: _tabController,
      labelColor: UIColors.primaryTextColor,
      unselectedLabelColor: UIColors.secondaryTextColor,
      indicatorColor: UIColors.primaryTextColor,
      tabs: const [
        Tab(text: 'All'),
        Tab(text: 'Clothing'),
        Tab(text: 'Weapons'),
        Tab(text: 'Utility'),
        Tab(text: 'Sell'),
      ],
    );
  }

  refreshData() {
    ItemManager.fetchMarketItems();
    ItemManager.fetchInventory();
  }

Widget buildTabViews() {
  return TabBarView(
    controller: _tabController,
    children: [
      GridBuilder.buildItemGrid(_marketItems, (item) => ItemDetailsHandler.showItemDetails(
          context,
          item,
          onTransactionComplete: refreshData
      )),
      GridBuilder.buildItemGrid(_marketItems.where((i) => i.category == 'Clothing').toList(), (item) => ItemDetailsHandler.showItemDetails(
          context,
          item,
          onTransactionComplete: refreshData
      )),
      GridBuilder.buildItemGrid(_marketItems.where((i) => i.category == 'Weapons').toList(), (item) => ItemDetailsHandler.showItemDetails(
          context,
          item,
          onTransactionComplete: refreshData
      )),
      GridBuilder.buildItemGrid(_marketItems.where((i) => i.category == 'Utility').toList(), (item) => ItemDetailsHandler.showItemDetails(
          context,
          item,
          onTransactionComplete: refreshData
      )),
      GridBuilder.buildItemGrid(_inventoryItems, (item) => ItemDetailsHandler.showItemDetails(
          context,
          item,
          isSelling: true,
          onTransactionComplete: refreshData
      )),
    ],
  );
}
}