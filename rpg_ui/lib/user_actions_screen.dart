// ignore_for_file: unused_import

import 'package:flutter/material.dart';
import 'package:rpg_ui/colors.dart';
import 'widgets/button_widgets.dart';
import 'widgets/app_theme.dart';

class UserActionsScreen extends StatelessWidget {
  const UserActionsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("User Actions Screen"),
      ),
      body: const Center(
        child: Text("No actions to display yet."),
      ),
    );
  }
}
