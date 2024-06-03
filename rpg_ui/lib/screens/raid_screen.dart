import 'package:flutter/material.dart';

class RaidScreen extends StatefulWidget {
  final VoidCallback onExtract;

  const RaidScreen({super.key, required this.onExtract});

  @override
  _RaidScreenState createState() => _RaidScreenState();
}

class _RaidScreenState extends State<RaidScreen> {
  int actionsLeft = 20;
  bool inRaid = true;

  Map<String, String> itemDescriptions = {
    "5.56x45mm NATO": "Standard NATO rifle round. Effective against light armor.",
    "9x19mm AP": "Armor-piercing pistol round. High penetration capability.",
    "12 Gauge Slug": "Solid slug for shotguns. High damage, great for unarmored targets.",
  };

  Map<String, dynamic> currentRoom = {
    "id": "5db990fb-6d90-4885-9bae-600002a583f4",
    "room_type": "Regular Room",
    "items": [
      {"id": "d0906ac8-e8fc-4d07-b7f4-14fb2764635d", "name": "5.56x45mm NATO"},
      {"id": "b93c2a23-d7ab-4b34-8723-0f88ee74ee75", "name": "5.56x45mm NATO"},
      {"id": "08a39d59-96c3-42ad-add3-62b4c5ccace2", "name": "9x19mm AP"},
    ],
    "connections": [
      "f8426e4e-3a26-499a-9b48-011a33589fa7",
      "31468aa4-f722-4b12-8613-5e507faef795"
    ]
  };

  void traverse(String connectionId) {
    setState(() {
      currentRoom = {
        "id": "a3d1ade9-e3da-4c37-87e2-44afc8f7a51a",
        "room_type": "Regular Room",
        "items": [
          {"id": "fe8a5456-c499-45cb-8052-d1a91a9a8d5e", "name": "12 Gauge Slug"},
        ],
        "connections": ["4f7051fa-1b57-43aa-8a22-2e52d1154a3f"]
      };
      actionsLeft--;
    });
  }

  void pickup(String itemId) {
    setState(() {
      currentRoom['items'].removeWhere((item) => item['id'] == itemId);
      actionsLeft--;
    });
  }

    @override
  Widget build(BuildContext context) {
    return PopScope(
      onPopInvoked: (bool didPop) {
        if (inRaid) {
          return;
        }
        Navigator.of(context).maybePop();
      },
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: <Widget>[
            Text('Room Type: ${currentRoom["room_type"]}', style: const TextStyle(fontSize: 18)),
            const SizedBox(height: 10),
            const Text('Items:', style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
            Expanded(
              child: ListView(
                children: [
                  ...currentRoom['items'].map<Widget>((item) {
                    return ListTile(
                      title: Text(item['name']),
                      subtitle: Text(itemDescriptions[item['name']] ?? "No description available."),
                      trailing: ElevatedButton(
                        onPressed: () => pickup(item['id']),
                        child: const Text('Pick Up'),
                      ),
                    );
                  }).toList(),
                  const SizedBox(height: 10),
                  const Text('Connections:', style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
                  ...currentRoom['connections'].map<Widget>((connectionId) {
                    return ListTile(
                      title: const Text('A Door'),
                      trailing: ElevatedButton(
                        onPressed: () => traverse(connectionId),
                        child: const Text('Traverse'),
                      ),
                    );
                  }).toList(),
                  const SizedBox(height: 20),
                  if (actionsLeft <= 0)
                    ElevatedButton(
                      onPressed: widget.onExtract,
                      child: const Text('Extract'),
                    ),
                  Text('Actions Left: $actionsLeft', style: const TextStyle(fontSize: 18)),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
