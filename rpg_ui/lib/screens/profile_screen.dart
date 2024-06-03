import 'package:flutter/material.dart';
import '../models/user_stats.dart';
import '../models/user_inventory.dart';

class ProfileScreen extends StatelessWidget {
  final UserStats stats;
  final Inventory inventory;

  const ProfileScreen({super.key, required this.stats, required this.inventory});

  @override
  Widget build(BuildContext context) {
    return Padding(
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
            const Text(
              'Equipment',
              style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 10),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: inventory.items.map((item) {
                return Column(
                  children: [
                    Icon(item.icon, size: 40),
                    Text(item.name, style: const TextStyle(fontSize: 16)),
                  ],
                );
              }).toList(),
            ),
            const Divider(height: 20, thickness: 2),
            const Text(
              'Inventory',
              style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 10),
            Wrap(
              spacing: 10.0,
              runSpacing: 10.0,
              children: inventory.items.map((item) {
                return Column(
                  children: [
                    Icon(item.icon, size: 40),
                    Text(item.name, style: const TextStyle(fontSize: 16)),
                    Text('Qty: ${item.quantity}', style: const TextStyle(fontSize: 14)),
                  ],
                );
              }).toList(),
            ),
          ],
        ),
      ),
    );
  }
}
