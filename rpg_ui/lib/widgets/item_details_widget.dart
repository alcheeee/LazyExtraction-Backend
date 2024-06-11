import 'package:flutter/material.dart';
import '../item_data/item_utils.dart';

class ItemDetailWidget extends StatefulWidget {
  final String itemName;
  final List<Widget> actions;
  final int? maxQuantity;
  final Function(int quantity)? onTransfer;

  const ItemDetailWidget({
    required this.itemName,
    this.actions = const [],
    this.maxQuantity,
    this.onTransfer,
    super.key,
  });

  @override
  _ItemDetailWidgetState createState() => _ItemDetailWidgetState();
}

class _ItemDetailWidgetState extends State<ItemDetailWidget> {
  int _currentQuantity = 1;

  @override
  void initState() {
    super.initState();
    if (widget.maxQuantity != null && widget.maxQuantity! > 0) {
      _currentQuantity = 1;
    }
  }

  @override
  Widget build(BuildContext context) {
    final item = getItemByName(widget.itemName);

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

    // Function to display item details based on category
    List<Widget> getItemDetails(String category) {
      switch (category) {
        case 'Medical':
          return [
            if (item.containsKey('health_increase'))
              Text('Health Increase: ${item['health_increase']}', style: const TextStyle(fontSize: 18, color: Colors.white)),
            if (item.containsKey('pain_reduction'))
              Text('Pain Reduction: ${item['pain_reduction']}', style: const TextStyle(fontSize: 18, color: Colors.white)),
            if (item.containsKey('amount_of_actions'))
              Text('Amount of Actions: ${item['amount_of_actions']}', style: const TextStyle(fontSize: 18, color: Colors.white)),
            if (item.containsKey('agility_bonus'))
              Text('Agility Bonus: ${item['agility_bonus']}', style: const TextStyle(fontSize: 18, color: Colors.white)),
            if (item.containsKey('strength_bonus'))
              Text('Strength Bonus: ${item['strength_bonus']}', style: const TextStyle(fontSize: 18, color: Colors.white)),
          ];
        case 'Weapon':
          return [
            if (item.containsKey('caliber'))
              Text('Caliber: ${item['caliber']}', style: const TextStyle(fontSize: 18, color: Colors.white)),
            if (item.containsKey('damage'))
              Text('Damage: ${item['damage']}', style: const TextStyle(fontSize: 18, color: Colors.white)),
            if (item.containsKey('strength'))
              Text('Strength: ${item['strength']}', style: const TextStyle(fontSize: 18, color: Colors.white)),
            if (item.containsKey('range'))
              Text('Range: ${item['range']}', style: const TextStyle(fontSize: 18, color: Colors.white)),
            if (item.containsKey('accuracy'))
              Text('Accuracy: ${item['accuracy']}', style: const TextStyle(fontSize: 18, color: Colors.white)),
            if (item.containsKey('reload_speed'))
              Text('Reload Speed: ${item['reload_speed']}', style: const TextStyle(fontSize: 18, color: Colors.white)),
            if (item.containsKey('fire_rate'))
              Text('Fire Rate: ${item['fire_rate']}', style: const TextStyle(fontSize: 18, color: Colors.white)),
            if (item.containsKey('magazine_size'))
              Text('Magazine Size: ${item['magazine_size']}', style: const TextStyle(fontSize: 18, color: Colors.white)),
            if (item.containsKey('armor_penetration'))
              Text('Armor Penetration: ${item['armor_penetration']}', style: const TextStyle(fontSize: 18, color: Colors.white)),
            if (item.containsKey('headshot_chance'))
              Text('Headshot Chance: ${item['headshot_chance']}', style: const TextStyle(fontSize: 18, color: Colors.white)),
            if (item.containsKey('agility_penalty'))
              Text('Agility Penalty: ${item['agility_penalty']}', style: const TextStyle(fontSize: 18, color: Colors.white)),
          ];
        case 'Bullets':
          return [
            if (item.containsKey('armor_pen_adj'))
              Text('Armor Penetration Adj: ${item['armor_pen_adj']}', style: const TextStyle(fontSize: 18, color: Colors.white)),
            if (item.containsKey('accuracy_adj'))
              Text('Accuracy Adj: ${item['accuracy_adj']}', style: const TextStyle(fontSize: 18, color: Colors.white)),
            if (item.containsKey('range_adj'))
              Text('Range Adj: ${item['range_adj']}', style: const TextStyle(fontSize: 18, color: Colors.white)),
            if (item.containsKey('damage_adj'))
              Text('Damage Adj: ${item['damage_adj']}', style: const TextStyle(fontSize: 18, color: Colors.white)),
            if (item.containsKey('fire_rate_adj'))
              Text('Fire Rate Adj: ${item['fire_rate_adj']}', style: const TextStyle(fontSize: 18, color: Colors.white)),
            if (item.containsKey('reload_speed_adj'))
              Text('Reload Speed Adj: ${item['reload_speed_adj']}', style: const TextStyle(fontSize: 18, color: Colors.white)),
          ];
        case 'Attachments':
          return [
            if (item.containsKey('weight_adj'))
              Text('Weight Adj: ${item['weight_adj']}', style: const TextStyle(fontSize: 18, color: Colors.white)),
            if (item.containsKey('max_durability_adj'))
              Text('Max Durability Adj: ${item['max_durability_adj']}', style: const TextStyle(fontSize: 18, color: Colors.white)),
            if (item.containsKey('damage_adj'))
              Text('Damage Adj: ${item['damage_adj']}', style: const TextStyle(fontSize: 18, color: Colors.white)),
            if (item.containsKey('range_adj'))
              Text('Range Adj: ${item['range_adj']}', style: const TextStyle(fontSize: 18, color: Colors.white)),
            if (item.containsKey('accuracy_adj'))
              Text('Accuracy Adj: ${item['accuracy_adj']}', style: const TextStyle(fontSize: 18, color: Colors.white)),
            if (item.containsKey('reload_speed_adj'))
              Text('Reload Speed Adj: ${item['reload_speed_adj']}', style: const TextStyle(fontSize: 18, color: Colors.white)),
            if (item.containsKey('fire_rate_adj'))
              Text('Fire Rate Adj: ${item['fire_rate_adj']}', style: const TextStyle(fontSize: 18, color: Colors.white)),
            if (item.containsKey('magazine_size_adj'))
              Text('Magazine Size Adj: ${item['magazine_size_adj']}', style: const TextStyle(fontSize: 18, color: Colors.white)),
            if (item.containsKey('headshot_chance_adj'))
              Text('Headshot Chance Adj: ${item['headshot_chance_adj']}', style: const TextStyle(fontSize: 18, color: Colors.white)),
            if (item.containsKey('agility_penalty_adj'))
              Text('Agility Penalty Adj: ${item['agility_penalty_adj']}', style: const TextStyle(fontSize: 18, color: Colors.white)),
          ];
        case 'Armor':
          return [
            if (item.containsKey('max_durability'))
              Text('Max Durability: ${item['max_durability']}', style: const TextStyle(fontSize: 18, color: Colors.white)),
            if (item.containsKey('current_durability'))
              Text('Current Durability: ${item['current_durability']}', style: const TextStyle(fontSize: 18, color: Colors.white)),
            if (item.containsKey('weight'))
              Text('Weight: ${item['weight']}', style: const TextStyle(fontSize: 18, color: Colors.white)),
            if (item.containsKey('head_protection'))
              Text('Head Protection: ${item['head_protection']}', style: const TextStyle(fontSize: 18, color: Colors.white)),
            if (item.containsKey('chest_protection'))
              Text('Chest Protection: ${item['chest_protection']}', style: const TextStyle(fontSize: 18, color: Colors.white)),
            if (item.containsKey('stomach_protection'))
              Text('Stomach Protection: ${item['stomach_protection']}', style: const TextStyle(fontSize: 18, color: Colors.white)),
            if (item.containsKey('arm_protection'))
              Text('Arm Protection: ${item['arm_protection']}', style: const TextStyle(fontSize: 18, color: Colors.white)),
            if (item.containsKey('agility_penalty'))
              Text('Agility Penalty: ${item['agility_penalty']}', style: const TextStyle(fontSize: 18, color: Colors.white)),
          ];
        default:
          return [];
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
          ...getItemDetails(item['category']),
          const SizedBox(height: 20),
          if (widget.maxQuantity != null && widget.maxQuantity! > 1) ...[
            Text('Quantity to Transfer: $_currentQuantity', style: const TextStyle(fontSize: 18, color: Colors.white)),
            Slider(
              value: _currentQuantity.toDouble(),
              min: 1,
              max: widget.maxQuantity!.toDouble(),
              divisions: (widget.maxQuantity! - 1) > 0 ? widget.maxQuantity! - 1 : 1,
              label: '$_currentQuantity',
              onChanged: (value) {
                setState(() {
                  _currentQuantity = value.toInt();
                });
              },
            ),
          ],
          if (widget.actions.isNotEmpty) ...[
            const Divider(color: Colors.white),
            ButtonBar(
              alignment: MainAxisAlignment.end,
              children: widget.actions,
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