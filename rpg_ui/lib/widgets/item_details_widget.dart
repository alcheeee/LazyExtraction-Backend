import 'package:flutter/material.dart';
import '../item_data/item_utils.dart';

class ItemDetailWidget extends StatelessWidget {
  final String itemName;
  final List<Widget> actions;

  const ItemDetailWidget({
    required this.itemName,
    this.actions = const [],
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    final item = getItemByName(itemName);

    if (item == null) {
      return const Center(
        child: Text('Item not found', style: TextStyle(color: Colors.white)),
      );
    }

    // Determine the color based on the tier
    Color getTierColor(String tier) {
      switch (tier) {
        case 'Tier1':
          return Colors.grey;
        case 'Tier2':
          return Colors.green;
        case 'Tier3':
          return Colors.blue;
        case 'Tier4':
          return Colors.purple;
        case 'Tier5':
          return Colors.yellow;
        default:
          return Colors.grey;
      }
    }

    return Container(
      color: Colors.grey[900],
      padding: const EdgeInsets.all(16.0),
      constraints: BoxConstraints(maxWidth: MediaQuery.of(context).size.width * 0.8),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisSize: MainAxisSize.min,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                item['item_name'],
                style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: Colors.white),
              ),
              IconButton(
                icon: const Icon(Icons.close, color: Colors.white),
                onPressed: () => Navigator.of(context).pop(),
              ),
            ],
          ),
          const SizedBox(height: 10),
          Center(
            child: Image.asset(
              item['texture'],
              height: 100,
              width: 100,
              fit: BoxFit.cover,
            ),
          ),
          const SizedBox(height: 10),
          SectionTitle(title: 'General Information', color: getTierColor(item['tier'])),
          Text('${item['category']}', style: const TextStyle(fontSize: 18, color: Colors.white)),
          Text('${item['tier']}', style: TextStyle(fontSize: 18, color: getTierColor(item['tier']))),
          Text('Est Value: ${item['quick_sell']}', style: const TextStyle(fontSize: 18, color: Colors.white)),
          if (item.containsKey('weight')) Text('Weight: ${item['weight']}', style: const TextStyle(fontSize: 18, color: Colors.white)),
          if (item.containsKey('caliber')) Text('Caliber: ${item['caliber']}', style: const TextStyle(fontSize: 18, color: Colors.white)),
          if (item.containsKey('damage')) Text('Damage: ${item['damage']}', style: const TextStyle(fontSize: 18, color: Colors.white)),
          if (item.containsKey('strength')) Text('Strength: ${item['strength']}', style: const TextStyle(fontSize: 18, color: Colors.white)),
          if (item.containsKey('range')) Text('Range: ${item['range']}', style: const TextStyle(fontSize: 18, color: Colors.white)),
          if (item.containsKey('accuracy')) Text('Accuracy: ${item['accuracy']}', style: const TextStyle(fontSize: 18, color: Colors.white)),
          if (item.containsKey('reload_speed')) Text('Reload Speed: ${item['reload_speed']}', style: const TextStyle(fontSize: 18, color: Colors.white)),
          if (item.containsKey('fire_rate')) Text('Fire Rate: ${item['fire_rate']}', style: const TextStyle(fontSize: 18, color: Colors.white)),
          if (item.containsKey('magazine_size')) Text('Magazine Size: ${item['magazine_size']}', style: const TextStyle(fontSize: 18, color: Colors.white)),
          if (item.containsKey('armor_penetration')) Text('Armor Penetration: ${item['armor_penetration']}', style: const TextStyle(fontSize: 18, color: Colors.white)),
          if (item.containsKey('headshot_chance')) Text('Headshot Chance: ${item['headshot_chance']}', style: const TextStyle(fontSize: 18, color: Colors.white)),
          if (item.containsKey('agility_penalty')) Text('Agility Penalty: ${item['agility_penalty']}', style: const TextStyle(fontSize: 18, color: Colors.white)),
          const SizedBox(height: 20),
          if (actions.isNotEmpty) ...[
            const Divider(color: Colors.white),
            ButtonBar(
              alignment: MainAxisAlignment.end,
              children: actions,
            ),
          ],
        ],
      ),
    );
  }
}

class SectionTitle extends StatelessWidget {
  final String title;
  final Color color;

  const SectionTitle({required this.title, required this.color, super.key});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 2.0),
      child: Text(
        title,
        style: TextStyle(
          fontSize: 22,
          fontWeight: FontWeight.bold,
          color: color,
        ),
      ),
    );
  }
}
