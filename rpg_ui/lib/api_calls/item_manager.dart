import 'package:http/http.dart' as http;
import 'dart:convert';
import '../config.dart';

class ItemManager {
  static Future<List<dynamic>> fetchInventory() async {
    final response = await http.post(
      Uri.parse('${APIUrl.apiURL}/game/get-user-inventory'),
      headers: {
        'Authorization': 'Bearer ${SessionManager.accessToken}',
      },
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body) as List<dynamic>;
    } else {
      throw Exception('Failed to fetch inventory: ${jsonDecode(response.body)['detail']['message']}');
    }
  }

  static Future<String> equipItem(int itemId) async {
    var response = await http.post(
      Uri.parse('${APIUrl.apiURL}/game/equip-item'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ${SessionManager.accessToken}',
      },
      body: jsonEncode({'item_id': itemId}),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body)['message'] ?? 'Item equipped successfully';
    } else {
      throw Exception('${jsonDecode(response.body)['detail']['message']}');
    }
  }
}
