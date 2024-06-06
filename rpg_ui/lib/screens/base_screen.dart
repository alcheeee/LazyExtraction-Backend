import 'package:flutter/material.dart';
import '../models/user_stats.dart';
import '../models/user_inventory.dart';
import 'profile_screen.dart';
import 'main_screen.dart';
import 'raid_screen.dart';
import 'raid_selection_screen.dart';

class BaseScreen extends StatefulWidget {
  const BaseScreen({super.key});

  @override
  _BaseScreenState createState() => _BaseScreenState();
}

class _BaseScreenState extends State<BaseScreen> {
  int _selectedIndex = 0; // Default to the main menu
  late PageController _pageController;

  bool inRaid = false;

  @override
  void initState() {
    super.initState();
    _pageController = PageController(initialPage: _selectedIndex);
  }

  void _onItemTapped(int index) {
    if (_selectedIndex == index) return;

    if (inRaid && index != 2) {
      // Do nothing if in raid and trying to navigate away
      return;
    }

    setState(() {
      _selectedIndex = index;
    });
    _pageController.animateToPage(index, duration: const Duration(milliseconds: 300), curve: Curves.easeInOut);
  }

  void startRaid() {
    setState(() {
      inRaid = true;
      _onItemTapped(2);
    });
  }

  void extract() {
    setState(() {
      inRaid = false;
      _onItemTapped(0); // Go back to home screen after extraction
    });
  }

  @override
  Widget build(BuildContext context) {
    return PopScope(
      onPopInvoked: (bool didPop) {
        // Prevent back navigation if in raid
        if (inRaid) {
          return;
        }
        Navigator.of(context).maybePop();
      },
      child: Scaffold(
        appBar: AppBar(
          title: const Text('Escape From Menus'),
          automaticallyImplyLeading: false, // Remove the back button
        ),
        body: PageView(
          controller: _pageController,
          onPageChanged: (index) {
            setState(() {
              _selectedIndex = index;
              inRaid = index == 2 && inRaid; // Keep inRaid true only if on the raid screen
            });
          },
          children: <Widget>[
            MainScreen(onNavigate: _onItemTapped), // Safe-House icon
            MainScreen(onNavigate: _onItemTapped), // Search icon
            inRaid ? RaidScreen(onExtract: extract) : RaidSelectionScreen(onStartRaid: startRaid), // Middle icon
            MainScreen(onNavigate: _onItemTapped), // Notifications icon
            ProfileScreen(stats: exampleUserStats, inventory: exampleInventory), // Profile icon
          ],
        ),
        bottomNavigationBar: BottomAppBar(
          shape: const CircularNotchedRectangle(),
          notchMargin: 6.0,
          child: Container(
            height: 60.0,
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: <Widget>[
                buildNavBarItem(Icons.home, 0, isDisabled: inRaid), // Safe-House icon
                buildNavBarItem(Icons.search, 1, isDisabled: inRaid), // Search icon
                const SizedBox(width: 80.0), // Space for the middle button
                buildNavBarItem(Icons.notifications, 3, isDisabled: inRaid), // Notifications icon
                buildNavBarItem(Icons.person, 4, isDisabled: inRaid), // Profile icon
              ],
            ),
          ),
        ),
        floatingActionButtonLocation: FloatingActionButtonLocation.centerDocked,
        floatingActionButton: GestureDetector(
          onTap: () => _onItemTapped(2),
          child: Container(
            height: 80.0,
            width: 80.0,
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              color: Colors.white,
              border: Border.all(
                color: Colors.blue,
                width: 3.0,
              ),
            ),
            child: Icon(
              Icons.favorite,
              color: _selectedIndex == 2 ? Colors.blue : Colors.grey,
              size: 40.0,
            ),
          ),
        ),
      ),
    );
  }

  Widget buildNavBarItem(IconData icon, int index, {bool isMiddle = false, bool isDisabled = false}) {
    return GestureDetector(
      onTap: isDisabled ? null : () => _onItemTapped(index),
      child: Container(
        height: 60.0,
        width: 60.0,
        decoration: index == _selectedIndex
            ? const BoxDecoration(
                border: Border(
                  top: BorderSide(width: 3.0, color: Colors.blue),
                ),
              )
            : null,
        child: Icon(
          icon,
          color: isDisabled ? Colors.grey : (index == _selectedIndex ? Colors.blue : Colors.grey),
          size: isMiddle ? 30.0 : 24.0,
        ),
      ),
    );
  }
}
