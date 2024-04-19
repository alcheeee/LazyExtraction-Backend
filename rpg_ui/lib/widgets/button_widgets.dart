import 'package:flutter/material.dart';
import 'package:rpg_ui/colors.dart';

class CustomButton extends StatelessWidget {
  final String label;
  final VoidCallback onPressed;
  final Color backgroundColor;
  final TextStyle? textStyle;

  const CustomButton({
    super.key,
    required this.label,
    required this.onPressed,
    this.backgroundColor = ButtonColors.primaryColor, // Use the primary color
    this.textStyle,
  });

  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      onPressed: onPressed,
      style: ElevatedButton.styleFrom(
        backgroundColor: backgroundColor,
        foregroundColor: ButtonColors.primaryTextColor,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(4.0),
        ),
      ),
      child: Text(
        label,
        style: textStyle ??
            const TextStyle(
              color: ButtonColors.primaryTextColor, // Explicitly use the primary text color
              fontSize: 16,
            ),
      ),
    );
  }
}
