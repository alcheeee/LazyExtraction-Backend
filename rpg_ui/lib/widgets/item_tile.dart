import 'package:flutter/material.dart';
import '../common_imports.dart';

class ItemTile extends StatelessWidget {
  final Item item;
  final VoidCallback onTap;
  final List<String> bottomInfoKeys;

  const ItemTile({
    super.key,
    required this.item,
    required this.onTap,
    required this.bottomInfoKeys,
  });


  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.all(2),
        decoration: BoxDecoration(
          color: UIColors.secondaryBackgroundColor.withOpacity(0.85),
          border: Border.all(color: UIColors.primaryOutlineColor, width: 2),
          borderRadius: BorderRadius.circular(4),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.2),
              spreadRadius: 1,
              blurRadius: 4,
              offset: const Offset(0, 2),
            ),
          ],
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(
              item.itemName,
              style: TextStyle(
                color: item.qualityColor,
                fontWeight: FontWeight.w400,
                fontSize: 14,
              ),
            ),
            Expanded(
              child: Center(
                child: Opacity(
                  opacity: 0.8,
                  child: Image.asset(item.itemAsset, fit: BoxFit.cover),
                ),
              ),
            ),
            // Only display quantity if it exists
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                _buildBottomText("",item.quantity),
                _buildBottomText("\$",item.itemCost),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildBottomText(String label, dynamic value) {
    String formattedValue = value?.toString() ?? "0";
    String displayText = label.isNotEmpty ? "$label$formattedValue" : formattedValue;
    return Expanded(
      child: Align(
        alignment: label.isNotEmpty ? Alignment.centerRight : Alignment.centerLeft,
        child: Text(
        displayText,
        style: const TextStyle(
          color: UIColors.primaryTextColor,
          fontSize: 12,
          fontWeight: FontWeight.w400,
          ),
          overflow: TextOverflow.ellipsis,
        ),
      ),
    );
  }
}
