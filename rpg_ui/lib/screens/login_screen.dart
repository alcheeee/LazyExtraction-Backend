// ignore_for_file: unused_import
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:rpg_ui/widgets/app_theme.dart';
import 'dart:convert';
import '../common_imports.dart';
import '../api_calls/user_auth_api.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  _LoginScreenState createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final TextEditingController _usernameController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  String _message = '';

  Future<void> login() async {
    try {
      String? errorMessage = await UserManager.login(
        _usernameController.text,
        _passwordController.text
      );
      if (!mounted) return;

      if (errorMessage == null) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Login successful'))
        );
        Navigator.of(context).pushReplacementNamed(AppRoutes.home);
      } else {
        setState(() {
          _message = errorMessage;
        });
      }
    } catch (error) {
      if (!mounted) return;
      setState(() {
        _message = "An unexpected error occurred: ${error.toString()}";
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final GlobalKey<ScaffoldState> scaffoldKey = GlobalKey<ScaffoldState>();

    return Scaffold(
      key: scaffoldKey,
      appBar: commonAppBar('Login Screen', scaffoldKey, context, showMenuIcon: false),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            TextField(
              controller: _usernameController,
              decoration: AppTheme.inputDecoration('Username'),
            ),
            TextField(
              controller: _passwordController,
              decoration: AppTheme.inputDecoration('Password'),
              obscureText: true,
            ),
            const SizedBox(height: 20),
            AppTheme.customButton(
              label: 'Login',
              onPressed: login
            ),
            const SizedBox(height: 20),
            GestureDetector(
              onTap: () => Navigator.of(context).pushNamed(AppRoutes.register),
              child: Text(
                'No account? Register here.',
                style: AppTheme.linkTextStyle(),
              ),
            ),
            Text(_message),
          ],
        ),
      ),
    );
  }
}
