// ignore_for_file: unused_import

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:rpg_ui/colors.dart';
import 'widgets/button_widgets.dart';
import 'dart:convert';
import 'config.dart';
import 'widgets/app_theme.dart';

class MarketScreen extends StatefulWidget {
  const MarketScreen({super.key});

  @override
  _MarketScreenState createState() => _MarketScreenState();
}

class _MarketScreenState extends State<MarketScreen> {
  List<dynamic> _marketItems = [];
  String _message = '';

  Future<void> fetchMarketItems() async {
    final response = await http.post(
      Uri.parse('${APIUrl.apiURL}/market/get-generalmarket-items'),
      headers: <String, String>{
        'Authorization': 'Bearer ${SessionManager.accessToken}',
      },
    );

    if (response.statusCode == 200) {
      setState(() {
        _marketItems = jsonDecode(response.body) as List<dynamic>;
        _message = 'Market items fetched successfully';
      });
    } else {
      var data = jsonDecode(response.body);
      setState(() {
        _message = 'Failed to fetch market items: ${data['detail']['message']}';
      });
    }
  }

  @override
  void initState() {
    super.initState();
    fetchMarketItems();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('General Market')),
      body: Padding(
        padding: const EdgeInsets.all(8.0),
        child: Column(
          children: [
            Expanded(
              child: ListView.builder(
                itemCount: _marketItems.length,
                itemBuilder: (context, index) {
                  var item = _marketItems[index];
                  return ListTile(
                    title: Text(item['item_name'], style: const TextStyle(color: UIColors.primaryTextColor)),
                    subtitle: Text('Price: \$${item['item_cost']} Quantity: ${item['quantity']}', style: const TextStyle(color: UIColors.secondaryTextColor)),
                  );
                },
              ),
            ),
            Text(_message),
          ],
        ),
      ),
    );
  }
}
