import 'package:flutter/material.dart';
import '../models/user_stats.dart';
import '../models/user_inventory.dart';
import '../widgets/item_details_widget.dart';
import '../utils/inventory_utils.dart';

class ProfileScreen extends StatelessWidget {
  final UserStats stats;
  final Inventory inventory;

  const ProfileScreen({super.key, required this.stats, required this.inventory});

  void showItemDetailsPopup(BuildContext context, String itemName) {
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
            child: ItemDetailWidget(itemName: itemName),
          ),
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    final categorizedItems = InventoryUtils.sortItemsByCategory(inventory.items);

    // Log categorized items
    print('Categorized Items: $categorizedItems');

    return Scaffold(
      appBar: AppBar(
        title: const Text('Profile'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: <Widget>[
              const Text(
                'Username',
                style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 10),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    'Level: ${stats.level}',
                    style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                  ),
                  Text(
                    'Reputation: ${stats.reputation}',
                    style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                  ),
                ],
              ),
              const Divider(height: 20, thickness: 2),
              ExpansionTile(
                title: const Text(
                  'Stats',
                  style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
                ),
                children: <Widget>[
                  ListTile(
                    title: Text('Max Energy: ${stats.maxEnergy}', style: const TextStyle(fontSize: 18)),
                  ),
                  ListTile(
                    title: Text('Luck: ${stats.luck}', style: const TextStyle(fontSize: 18)),
                  ),
                  ListTile(
                    title: Text('Knowledge: ${stats.knowledge}', style: const TextStyle(fontSize: 18)),
                  ),
                  ListTile(
                    title: Text('Max Weight: ${stats.maxWeight}', style: const TextStyle(fontSize: 18)),
                  ),
                  ListTile(
                    title: Text('Agility: ${stats.agility}', style: const TextStyle(fontSize: 18)),
                  ),
                  ListTile(
                    title: Text('Health: ${stats.health}', style: const TextStyle(fontSize: 18)),
                  ),
                  ListTile(
                    title: Text('Damage: ${stats.damage}', style: const TextStyle(fontSize: 18)),
                  ),
                  ListTile(
                    title: Text('Strength: ${stats.strength}', style: const TextStyle(fontSize: 18)),
                  ),
                  ListTile(
                    title: Text('Head Protection: ${stats.headProtection}', style: const TextStyle(fontSize: 18)),
                  ),
                  ListTile(
                    title: Text('Chest Protection: ${stats.chestProtection}', style: const TextStyle(fontSize: 18)),
                  ),
                  ListTile(
                    title: Text('Stomach Protection: ${stats.stomachProtection}', style: const TextStyle(fontSize: 18)),
                  ),
                  ListTile(
                    title: Text('Arm Protection: ${stats.armProtection}', style: const TextStyle(fontSize: 18)),
                  ),
                ],
              ),
              const Divider(height: 20, thickness: 2),
              const Text(
                'Bank and Energy',
                style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 10),
              Text(
                'Bank: \$${inventory.bank}',
                style: const TextStyle(fontSize: 18),
              ),
              Text(
                'Energy: ${inventory.energy}',
                style: const TextStyle(fontSize: 18),
              ),
              const Divider(height: 20, thickness: 2),
              ...categorizedItems.entries.map((entry) {
                return InventoryUtils.buildCategorySection(context, entry.key, entry.value, showItemDetailsPopup);
              }),
            ],
          ),
        ),
      ),
    );
  }
}
