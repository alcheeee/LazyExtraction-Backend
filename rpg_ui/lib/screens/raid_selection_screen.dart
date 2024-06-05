import 'package:flutter/material.dart';

class RaidSelectionScreen extends StatelessWidget {
  final VoidCallback onStartRaid;

  const RaidSelectionScreen({super.key, required this.onStartRaid});

  @override
  Widget build(BuildContext context) {
    final screenHeight = MediaQuery.of(context).size.height;
    final boxHeight = screenHeight * 0.2;

    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: <Widget>[
          const Text('Select World:', style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: Colors.white)),
          const SizedBox(height: 10),
          buildWorldBox(context, 'Forest', 'Tier 1', 'A lush forest filled with hidden dangers.', 'assets/worlds/forest.jpg', boxHeight, 0),
          const SizedBox(height: 10),
          buildWorldBox(context, 'Military Base', 'Tier 2', 'An abandoned military base with high-level loot.', 'assets/worlds/military-base.jpg', boxHeight, 50),
          const SizedBox(height: 10),
          buildWorldBox(context, 'Laboratory', 'Tier 3', 'A secret laboratory with rare and dangerous items.', 'assets/worlds/laboratory.jpg', boxHeight, 100),
        ],
      ),
    );
  }

  Widget buildWorldBox(BuildContext context, String worldName, String tier, String description, String imagePath, double height, int cost) {
    return GestureDetector(
      onTap: () => showWorldDetails(context, worldName, tier, description, cost),
      child: Container(
        height: height,
        decoration: BoxDecoration(
          image: DecorationImage(
            image: AssetImage(imagePath),
            fit: BoxFit.cover,
            colorFilter: ColorFilter.mode(Colors.black.withOpacity(0.6), BlendMode.dstATop),
          ),
          borderRadius: BorderRadius.circular(8.0),
        ),
        child: Stack(
          children: [
            Positioned(
              top: 10,
              left: 10,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    worldName,
                    style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: Colors.white),
                  ),
                  Text(
                    tier,
                    style: const TextStyle(fontSize: 16, color: Colors.white),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  void showWorldDetails(BuildContext context, String worldName, String tier, String description, int cost) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          backgroundColor: Colors.grey[900],
          title: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(worldName, style: const TextStyle(color: Colors.white, fontSize: 22, fontWeight: FontWeight.bold)),
              Text('Tier: $tier', style: const TextStyle(color: Colors.grey, fontSize: 16)),
            ],
          ),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: <Widget>[
              Container(
                padding: const EdgeInsets.all(8.0),
                decoration: BoxDecoration(
                  color: Colors.grey[800],
                  borderRadius: BorderRadius.circular(8.0),
                ),
                child: Text(description, style: const TextStyle(fontSize: 16, color: Colors.white)),
              ),
              const SizedBox(height: 10),
              Text('Cost to enter: $cost', style: const TextStyle(fontSize: 14, color: Colors.grey)),
            ],
          ),
          actions: <Widget>[
            TextButton(
              onPressed: () {
                Navigator.of(context).pop();
                onStartRaid();
              },
              child: const Text('Start Raid', style: TextStyle(color: Colors.blue)),
            ),
            TextButton(
              onPressed: () {
                Navigator.of(context).pop();
              },
              child: const Text('Cancel', style: TextStyle(color: Colors.white)),
            ),
          ],
        );
      },
    );
  }
}
