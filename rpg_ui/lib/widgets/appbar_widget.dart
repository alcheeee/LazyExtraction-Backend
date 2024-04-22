import 'package:flutter/material.dart';
import '../common_imports.dart';
import '../providers/user_info_provider.dart';

// Common AppBar
AppBar commonAppBar(String title, GlobalKey<ScaffoldState> scaffoldKey, BuildContext context, {bool showMenuIcon = true}) {
  final stats = Provider.of<UserStatsProvider>(context);
  return AppBar(
    title: Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Text(title),
        if (SessionManager.isAuthenticated)
          stats.isLoading ? const CircularProgressIndicator() : Row(
            children: [
              const Icon(Icons.flash_on),
              Text("${stats.energy}/${stats.maxEnergy}"),
              const SizedBox(width: 10),
              Text("\$${stats.bank}"),
            ],
          ),
      ],
    ),
    backgroundColor: UIColors.primaryBackgroundColor,
    foregroundColor: UIColors.primaryTextColor,
    leading: showMenuIcon ? IconButton(
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
    ) : null,
  );
}

// Common Drawer
Widget commonDrawer(BuildContext context, String currentRoute) {
  final stats = Provider.of<UserStatsProvider>(context, listen: false);
  return Drawer(
    child: Container(
      color: UIColors.secondaryBackgroundColor,
      child: ListView(
        padding: EdgeInsets.zero,
        children: [
          ListTile(
            title: Text('Level: ${stats.level}', style: const TextStyle(color: UIColors.primaryTextColor, fontWeight: FontWeight.bold)),
            subtitle: Text('Reputation: ${stats.reputation}', style: const TextStyle(color: UIColors.secondaryTextColor)),
          ),
          const Divider(color: UIColors.primaryOutlineColor),
          _buildDrawerItem(Icons.home, 'Home', AppRoutes.home, context, currentRoute),
          _buildDrawerItem(Icons.person, 'Profile', AppRoutes.userProfile, context, currentRoute),
          _buildDrawerItem(Icons.inventory, 'Inventory', AppRoutes.inventory, context, currentRoute),
          _buildDrawerItem(Icons.shopping_cart, 'Market', AppRoutes.market, context, currentRoute),
          _buildDrawerItem(Icons.work, 'Jobs', AppRoutes.jobs, context, currentRoute),
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
