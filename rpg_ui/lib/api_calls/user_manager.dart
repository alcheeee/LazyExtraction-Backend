import 'package:http/http.dart' as http;
import 'dart:convert';
import '../config.dart';

class UserManager {
  static Future<String?> login(String username, String password) async {
    try {
      var response = await http.post(
        Uri.parse('${APIUrl.apiURL}/user/login'),
        headers: <String, String>{
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: {
          'username': username,
          'password': password,
        },
      );
      if (response.statusCode == 200) {
        var data = jsonDecode(response.body);
        SessionManager.accessToken = data['access_token'];
        return null;
      } else {
        var data = jsonDecode(response.body);
        return data['detail']['message'];
      }
    } catch (e) {
      return e.toString();
    }
  }

  static Future<String?> register(String username, String password, String email) async {
    try {
      final response = await http.post(
        Uri.parse('${APIUrl.apiURL}/user/register'),
        headers: <String, String>{
          'Content-Type': 'application/json',
        },
        body: jsonEncode({
          'username': username,
          'password': password,
          'email': email,
        }),
      );

      if (response.statusCode == 200) {
        // Auto login after success
        String? loginError = await login(username, password);
        if (loginError != null) {
          return "Registration successful, but login failed: $loginError";
        }
        return null;
      } else {
        var data = jsonDecode(response.body);
        return data['detail']['message'];
      }
    } catch (e) {
      return e.toString();
    }
  }
}
