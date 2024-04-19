// ignore_for_file: unused_import
import 'package:flutter/material.dart';
import 'common_imports.dart';

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
        scaffoldBackgroundColor: UIColors.primaryBackgroundColor,
        primaryTextTheme: Typography(platform: TargetPlatform.iOS).white,
        textTheme: Typography(platform: TargetPlatform.iOS).white,
        appBarTheme: const AppBarTheme(
          backgroundColor: UIColors.primaryBackgroundColor,
          foregroundColor: UIColors.primaryTextColor
        ),
      ),
      initialRoute: SessionManager.isAuthenticated ? AppRoutes.home : AppRoutes.login,
      routes: AppRoutes.getRoutes(),
    );
  }
}

class MainScreen extends StatefulWidget {
  const MainScreen({super.key});

  @override
  _MainScreenState createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> {
  final GlobalKey<ScaffoldState> _scaffoldKey = GlobalKey<ScaffoldState>();

  @override
  Widget build(BuildContext context) {

    return Scaffold(
      key: _scaffoldKey,
      appBar: commonAppBar('API Testing', _scaffoldKey, context, showMenuIcon: true),
      drawer: commonDrawer(context, 'HomeScreenRoute'),
      body: Center(
        child: Text(
          SessionManager.isAuthenticated ? "Welcome" : "Log in",
          style: const TextStyle(color: UIColors.primaryTextColor, fontSize: 24),
        ),
      ),
    );
  }
}