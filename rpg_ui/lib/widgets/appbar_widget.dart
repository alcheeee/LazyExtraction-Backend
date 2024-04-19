import 'package:flutter/material.dart';
import '../common_imports.dart';

// Common AppBar
AppBar commonAppBar(String title, GlobalKey<ScaffoldState> scaffoldKey, BuildContext context, {bool showMenuIcon = true}) {
  return AppBar(
    title: Text(title),
    backgroundColor: UIColors.primaryBackgroundColor,
    foregroundColor: UIColors.primaryTextColor,
    leading: IconButton(
      icon: const Icon(Icons.menu),
      onPressed: () {
        if (SessionManager.isAuthenticated) {
          scaffoldKey.currentState?.openDrawer();
        } else {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text("You must be logged in to access the menu."),
              duration: Duration(seconds: 2),
            )
          );
        }
      },
    ),
  );
}

// Common Drawer
Widget commonDrawer(BuildContext context, String currentRoute) {
  return Drawer(
    child: Container(
      color: UIColors.secondaryBackgroundColor,
      child: ListView(
        padding: EdgeInsets.zero,
        children: [
          const UserAccountsDrawerHeader(
            decoration: BoxDecoration(color: UIColors.secondaryBackgroundColor),
            accountName: Text("UserExample", style: TextStyle(color: UIColors.primaryTextColor)),
            accountEmail: Text("email@example.com", style: TextStyle(color: UIColors.primaryTextColor)),
            currentAccountPicture: CircleAvatar(
              backgroundColor: Colors.grey,
              child: Text("U", style: TextStyle(fontSize: 40.0, color: UIColors.primaryTextColor)),
            ),
          ),
          _buildDrawerItem(Icons.home, 'Home', AppRoutes.home, context, currentRoute),
          _buildDrawerItem(Icons.inventory, 'Inventory', AppRoutes.inventory, context, currentRoute),
          _buildDrawerItem(Icons.shopping_cart, 'Market', AppRoutes.market, context, currentRoute),
          _buildDrawerItem(Icons.exit_to_app, 'Logout', '', context, currentRoute, logout: true),
        ],
      ),
    ),
  );
}

Widget _buildDrawerItem(IconData icon, String title, String routeName, BuildContext context, String currentRoute, {bool logout = false}) {
  return ListTile(
    leading: Icon(icon, color: UIColors.primaryTextColor),
    title: Text(title, style: const TextStyle(color: UIColors.primaryTextColor)),
    onTap: () {
      Navigator.of(context).pop();
      if (logout) {
        SessionManager.logout();
        Navigator.of(context).pushNamedAndRemoveUntil(AppRoutes.login, (Route<dynamic> route) => false);
      } else if (routeName.isNotEmpty && routeName != currentRoute) {
        Navigator.pushReplacementNamed(context, routeName);
      }
    },
  );
}
