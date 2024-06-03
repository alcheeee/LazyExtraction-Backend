import 'package:flutter/material.dart';

class RaidSelectionScreen extends StatelessWidget {
  final VoidCallback onStartRaid;

  const RaidSelectionScreen({super.key, required this.onStartRaid});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: <Widget>[
          const Text('Select World:', style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
          const SizedBox(height: 10),
          ElevatedButton(
            onPressed: onStartRaid,
            child: const Text('Forest - Tier 1'),
          ),
          const SizedBox(height: 10),
          ElevatedButton(
            onPressed: onStartRaid,
            child: const Text('Military Base - Tier 3'),
          ),
          const SizedBox(height: 10),
          ElevatedButton(
            onPressed: onStartRaid,
            child: const Text('Laboratory - Tier 3'),
          ),
        ],
      ),
    );
  }
}
