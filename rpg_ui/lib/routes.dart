import 'package:flutter/material.dart';
import 'screens/login_screen.dart';
import 'screens/register_screen.dart';
import 'screens/user_actions_screen.dart';
import 'screens/inventory_screen.dart';
import 'screens/market_screen.dart';
import 'screens/jobs_screen.dart';
import 'screens/user_profile_screen.dart';
import 'main.dart';

class AppRoutes {
  static const String home = '/';
  static const String login = '/login';
  static const String register = '/register';
  static const String userProfile = '/userProfile';
  static const String userActions = '/userActions';
  static const String inventory = '/inventory';
  static const String market = '/market';
  static const String jobs = '/jobs';

  static Map<String, WidgetBuilder> getRoutes() {
    return {
      home: (context) => const MainScreen(),
      login: (context) => const LoginScreen(),
      register: (context) => const RegisterScreen(),
      userProfile: (context) => const UserProfileScreen(),
      userActions: (context) => const UserActionsScreen(),
      inventory: (context) => const InventoryScreen(),
      market: (context) => const MarketScreen(),
      jobs: (context) => const JobsScreen(),
    };
  }
}
