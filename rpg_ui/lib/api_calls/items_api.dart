import 'package:http/http.dart' as http;
import 'dart:convert';
import '../config.dart';
import '../models/item_model.dart';

class ItemManager {

  // Fetch Users Inventory
  static Future<List<Item>> fetchInventory() async {
    var response = await http.post(Uri.parse('${APIUrl.apiURL}/user-info/get-user-inventory'),
      headers: {
        'Authorization': 'Bearer ${SessionManager.accessToken}',
      },
    );

    if (response.statusCode == 200) {
      List<dynamic> jsonData = jsonDecode(response.body);
      return jsonData.map((item) => Item.fromJson(item)).toList();
    } else {
      throw Exception('Failed to load inventory');
    }
  }

  // Equip Item
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


  // Fetch Market Items
  static Future<List<Item>> fetchMarketItems() async {
    var response = await http.post(Uri.parse('${APIUrl.apiURL}/market/get-generalmarket-items'),
      headers: {
        'Authorization': 'Bearer ${SessionManager.accessToken}',
      },
    );

    if (response.statusCode == 200) {
      List<dynamic> jsonData = jsonDecode(response.body);
      return jsonData.map((item) => Item.fromJson(item)).toList();
    } else {
      throw Exception('Failed to load inventory');
    }
  }
  static Future<String> buyItem(int itemId, int quantity) async {
    var response = await http.post(Uri.parse('${APIUrl.apiURL}/market/buy-market-item'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ${SessionManager.accessToken}',
      },
      body: jsonEncode({
        'item_id': itemId,
        'quantity': quantity
      }),
    );

    if (response.statusCode == 200) {
      return 'Purchase successful';
    } else {
      var data = jsonDecode(response.body);
      return 'Failed to buy item: ${data['detail']['message']}';
    }
  }
}
