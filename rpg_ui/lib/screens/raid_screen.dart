import 'package:flutter/material.dart';
import '../item_data/item_catalog.dart';
import '../widgets/item_details_widget.dart';

class RaidScreen extends StatefulWidget {
  final VoidCallback onExtract;

  const RaidScreen({super.key, required this.onExtract});

  @override
  _RaidScreenState createState() => _RaidScreenState();
}

class _RaidScreenState extends State<RaidScreen> {
  int actionsLeft = 20;
  bool inRaid = true;

  Map<String, dynamic> currentRoom = {
    "id": "5db990fb-6d90-4885-9bae-600002a583f4",
    "room_type": "Regular Room",
    "items": [
      {"id": "M1911", "name": "M1911"},
      {"id": "Beretta M9", "name": "Beretta M9"},
      {"id": "Sawed-off Shotgun", "name": "Sawed-off Shotgun"},
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
          {"id": "M4A1 Carbine", "name": "M4A1 Carbine"},
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
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                ItemDetailWidget(
                  itemName: itemName,
                  actions: [
                    TextButton(
                      onPressed: () {
                        Navigator.of(context).pop();
                        pickup(itemName);
                      },
                      child: const Text('Pick Up', style: TextStyle(color: Colors.blue)),
                    ),
                  ],
                ),
              ],
            ),
          ),
        );
      },
    );
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
            Text('${currentRoom["room_type"]}', style: const TextStyle(fontSize: 18)),
            const SizedBox(height: 10),
            const Text('Items:', style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
            Expanded(
              child: ListView(
                children: [
                  ...currentRoom['items'].map<Widget>((item) {
                    final itemName = item['name'];
                    final itemDescription = itemCatalog[itemName];

                    return GestureDetector(
                      onTap: () => showItemDetailsPopup(context, itemName),
                      child: Container(
                        margin: const EdgeInsets.symmetric(vertical: 5),
                        padding: const EdgeInsets.all(10),
                        decoration: BoxDecoration(
                          color: Colors.grey[800],
                          borderRadius: BorderRadius.circular(10),
                        ),
                        child: Row(
                          children: [
                            Image.asset(
                              itemCatalog[itemName]?['texture'] ?? 'assets/items/placeholder_item.png',
                              height: 40,
                              width: 40,
                            ),
                            const SizedBox(width: 10),
                            Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(itemName, style: const TextStyle(fontSize: 18, color: Colors.white)),
                                Text(
                                  itemDescription != null
                                      ? "${itemDescription['tier']} - ${itemDescription['category']}"
                                      : "No description available.",
                                  style: const TextStyle(fontSize: 14, color: Colors.grey),
                                ),
                              ],
                            ),
                          ],
                        ),
                      ),
                    );
                  }).toList(),
                  const SizedBox(height: 10),
                  const Text('Connections:', style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
                  ...currentRoom['connections'].map<Widget>((connectionId) {
                    return GestureDetector(
                      onTap: () => traverse(connectionId),
                      child: Container(
                        margin: const EdgeInsets.symmetric(vertical: 5),
                        padding: const EdgeInsets.all(10),
                        decoration: BoxDecoration(
                          color: Colors.grey[800],
                          borderRadius: BorderRadius.circular(10),
                        ),
                        child: const Row(
                          children: [
                            Icon(Icons.door_back_door_outlined, color: Colors.white, size: 40),
                            SizedBox(width: 10),
                            Text('Enter next Room', style: TextStyle(fontSize: 18, color: Colors.white)),
                          ],
                        ),
                      ),
                    );
                  }).toList(),
                  const SizedBox(height: 20),
                  if (actionsLeft <= 0)
                    GestureDetector(
                      onTap: widget.onExtract,
                      child: Container(
                        padding: const EdgeInsets.all(10),
                        decoration: BoxDecoration(
                          color: Colors.grey[800],
                          borderRadius: BorderRadius.circular(10),
                        ),
                        child: const Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Icon(Icons.exit_to_app, color: Colors.green, size: 30),
                            SizedBox(width: 10),
                            Text('Extract', style: TextStyle(fontSize: 18, color: Colors.green)),
                          ],
                        ),
                      ),
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
