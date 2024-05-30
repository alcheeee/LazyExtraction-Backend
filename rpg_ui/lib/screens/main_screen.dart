import 'package:flutter/material.dart';
import 'base_screen.dart';

class MainScreen extends StatelessWidget {
  const MainScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Text(
        'Welcome to the Main Screen',
        style: const TextStyle(fontSize: 24),
      ),
    );
  }
}
