// ignore_for_file: unused_import

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:rpg_ui/colors.dart';
import 'dart:convert';
import 'config.dart';
import 'main.dart';
import 'widgets/button_widgets.dart';
import 'widgets/app_theme.dart';

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
    final response = await http.post(
      Uri.parse('${APIUrl.apiURL}/user/login'),
      headers: <String, String>{
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: {
        'username': _usernameController.text,
        'password': _passwordController.text,
      },
    );

    if (!mounted) return;
    if (response.statusCode == 200) {
      var data = jsonDecode(response.body);
      SessionManager.accessToken = data['access_token']; // Store the token

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Login successful'))
      );

      Navigator.of(context).pushAndRemoveUntil(
        MaterialPageRoute(builder: (context) => const MainScreen()),
        (Route<dynamic> route) => false,
      );
    } else {
      var data = jsonDecode(response.body);
      setState(() {
        _message = 'Failed login: ${data['detail']['message']}';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Login Screen')),
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
            CustomButton(
              label: 'Login',
              onPressed: login),
              Text(_message),
          ],
        ),
      ),
    );
  }
}
