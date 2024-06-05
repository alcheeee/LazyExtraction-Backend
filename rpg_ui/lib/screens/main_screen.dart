import 'package:flutter/material.dart';
import 'profile_screen.dart';
import 'market_screen.dart';
import 'crew_screen.dart';
import '../models/user_stats.dart';
import '../models/user_inventory.dart';

class MainScreen extends StatelessWidget {
  final Function(int) onNavigate;

  const MainScreen({super.key, required this.onNavigate});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[900],
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: GridView.count(
          crossAxisCount: 2,
          crossAxisSpacing: 20,
          mainAxisSpacing: 20,
          children: [
            buildMenuItem(
              context,
              icon: Icons.person,
              label: 'Profile',
              onTap: () {
                onNavigate(4);
              },
            ),
            buildMenuItem(
              context,
              icon: Icons.shopping_cart,
              label: 'Market',
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => const MarketScreen(),
                  ),
                );
              },
            ),
            buildMenuItem(
              context,
              icon: Icons.assignment,
              label: 'Quests',
              onTap: () {},
              disabled: true,
              subtitle: 'Work In Progress',
            ),
            buildMenuItem(
              context,
              icon: Icons.group,
              label: 'Crew',
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => const CrewScreen(),
                  ),
                );
              },
            ),
            // Add any additional relevant features here
          ],
        ),
      ),
    );
  }

  Widget buildMenuItem(BuildContext context, {
    required IconData icon,
    required String label,
    required VoidCallback onTap,
    bool disabled = false,
    String? subtitle,
  }) {
    return GestureDetector(
      onTap: disabled ? null : onTap,
      child: Container(
        decoration: BoxDecoration(
          color: disabled ? Colors.grey[800] : Colors.grey[700],
          borderRadius: BorderRadius.circular(10),
        ),
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, size: 50, color: Colors.white),
            const SizedBox(height: 10),
            Text(
              label,
              style: const TextStyle(fontSize: 18, color: Colors.white),
              textAlign: TextAlign.center,
            ),
            if (subtitle != null) ...[
              const SizedBox(height: 5),
              Text(
                subtitle,
                style: const TextStyle(fontSize: 14, color: Colors.white),
                textAlign: TextAlign.center,
              ),
            ]
          ],
        ),
      ),
    );
  }
}
