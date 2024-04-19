import 'package:flutter/material.dart';
import 'package:rpg_ui/colors.dart';
import 'package:rpg_ui/widgets/button_widgets.dart';

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

  static Widget customButton({
    required String label,
    required VoidCallback onPressed,
    Color? backgroundColor,
    TextStyle? textStyle,
  }) {
    return CustomButton(
      label: label,
      onPressed: onPressed,
      backgroundColor: backgroundColor ?? ButtonColors.primaryColor,
      textStyle: textStyle ?? const TextStyle(
        color: ButtonColors.primaryTextColor,
        fontSize: 16,
      ),
    );
  }
    static TextStyle linkTextStyle() {
    return const TextStyle(
      color: UIColors.secondaryTextColor,
      fontSize: 14,
      fontWeight: FontWeight.bold,
    );
  }
}
