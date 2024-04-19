import 'package:flutter/material.dart';
import 'package:rpg_ui/colors.dart';

class AppTheme {
  static InputDecoration inputDecoration(String label) {
    return InputDecoration(
      labelText: label,
      labelStyle: const TextStyle(color: UIColors.secondaryTextColor),
      enabledBorder: const UnderlineInputBorder(
        borderSide: BorderSide(color: UIColors.secondaryBackgroundColor),
      ),
      focusedBorder: const UnderlineInputBorder(
        borderSide: BorderSide(color: UIColors.secondaryBackgroundColor),
      ),
    );
  }

  static ButtonStyle elevatedButtonStyle() {
    return ElevatedButton.styleFrom(
      backgroundColor: ButtonColors.primaryColor,
      foregroundColor: ButtonColors.primaryTextColor,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(4.0),
      ),
    );
  }
}
