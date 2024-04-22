import 'package:http/http.dart' as http;
import 'dart:convert';
import '../config.dart';
import '../models/user_model.dart';

class UserInfoManager {
  static Future<UserInfo> fetchUserInfo() async {
    var response = await http.get(Uri.parse('${APIUrl.apiURL}/user-info/get-user-info'),
      headers: {
        'Accept': 'application/json',
        'Authorization': 'Bearer ${SessionManager.accessToken}',
      },
    );

    if (response.statusCode == 200) {
      Map<String, dynamic> jsonData = jsonDecode(response.body);
      return UserInfo.fromJson(jsonData);
    } else {
      throw Exception('Failed to load user');
    }
  }
}