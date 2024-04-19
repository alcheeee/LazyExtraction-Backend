import 'package:flutter/material.dart';
import '../common_imports.dart';
import '../api_calls/user_auth_api.dart';


class RegisterScreen extends StatefulWidget {
  const RegisterScreen({super.key});

  @override
  _RegisterScreenState createState() => _RegisterScreenState();
}

class _RegisterScreenState extends State<RegisterScreen> {
  final TextEditingController _usernameController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();
  final TextEditingController _emailController = TextEditingController();
  String _message = '';

  Future<void> register() async {
    String? errorMessage = await UserManager.register(
      _usernameController.text,
      _passwordController.text,
      _emailController.text
    );

    if (!mounted) return;

    if (errorMessage == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Registration and login successful!'))
      );
      Navigator.of(context).pushReplacementNamed(AppRoutes.home);
    } else {
      setState(() {
        _message = errorMessage;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: commonAppBar('Register', GlobalKey<ScaffoldState>(), context, showMenuIcon: false),
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
            TextField(
              controller: _emailController,
              decoration: AppTheme.inputDecoration('Email'),
            ),
            const SizedBox(height: 20),
            AppTheme.customButton(
              label: 'Register',
              onPressed: register
            ),
            const SizedBox(height: 20),
            GestureDetector(
              onTap: () => Navigator.of(context).pushNamed(AppRoutes.login),
              child: Text(
                'Have an account? Login here.',
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
