// ignore_for_file: unused_import
import 'package:flutter/material.dart';
import 'package:rpg_ui/colors.dart';
import 'widgets/button_widgets.dart';
import 'login_screen.dart';
import 'register_screen.dart';
import 'user_actions_screen.dart';
import 'inventory_screen.dart';
import 'market_screen.dart';
import 'config.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'API Tester',
      theme: ThemeData(
        scaffoldBackgroundColor: UIColors.primaryBackgroundColor, // Default background color

        primaryTextTheme: Typography(platform: TargetPlatform.iOS).white,
        textTheme: Typography(platform: TargetPlatform.iOS).white,

        appBarTheme: const AppBarTheme(
          backgroundColor: UIColors.primaryBackgroundColor,
          foregroundColor: UIColors.primaryTextColor
        ),
      ),
      home: const MainScreen(),
    );
  }
}

class MainScreen extends StatefulWidget {
  const MainScreen({super.key});

  @override
  _MainScreenState createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('API Testing'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            // Show login and register only if NOT authenticated
            if (!SessionManager.isAuthenticated)
              CustomButton(
                label: 'Login',
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => const LoginScreen()),
                  ).then((_) => setState(() {}));
                },
              ),
            if (!SessionManager.isAuthenticated)
              CustomButton(
                label: 'Register',
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => const RegisterScreen()),
                  ).then((_) => setState(() {}));
                },
              ),
            if (SessionManager.isAuthenticated)
              CustomButton(
                label: 'User Actions',
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => const UserActionsScreen()),
                  );
                },
              ),
            if (SessionManager.isAuthenticated)
              CustomButton(
                label: 'View Inventory',
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => const InventoryScreen()),
                  );
                },
              ),
            if (SessionManager.isAuthenticated)
              CustomButton(
                label: 'Market Operations',
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => const MarketScreen()),
                  );
                },
              ),
          ],
        ),
      ),
    );
  }
}