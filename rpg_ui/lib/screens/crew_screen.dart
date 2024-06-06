import 'package:flutter/material.dart';

class CrewScreen extends StatelessWidget {
  const CrewScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Crew'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: <Widget>[
            const Text(
              'Create Crew',
              style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 10),
            const TextField(
              decoration: InputDecoration(
                border: OutlineInputBorder(),
                labelText: 'Crew Name',
                fillColor: Colors.white,
                filled: true,
              ),
            ),
            const SizedBox(height: 10),
            ElevatedButton(
              onPressed: () {
                // Add logic to create a crew
              },
              child: const Text('Create'),
            ),
            const SizedBox(height: 20),
            const Text(
              'Your Crews',
              style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
            ),
            // Add a list of user's crews here
          ],
        ),
      ),
    );
  }
}
