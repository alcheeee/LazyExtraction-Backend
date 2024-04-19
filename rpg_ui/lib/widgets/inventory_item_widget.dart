import 'package:flutter/material.dart';
import '../common_imports.dart';

class ItemTile extends StatelessWidget {
  final Map<String, dynamic> item;
  final List<String> bottomInfoKeys;  // Keys for information to display at the bottom
  final VoidCallback onTap;

  const ItemTile({super.key, required this.item, required this.bottomInfoKeys, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.all(6),
        decoration: BoxDecoration(
          color: UIColors.secondaryBackgroundColor,
          border: Border.all(color: UIColors.primaryOutlineColor),
          borderRadius: BorderRadius.circular(2),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.1),
              spreadRadius: 1,
              blurRadius: 2,
              offset: const Offset(0, 1),
            ),
          ],
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(item['item_name'], style: TextStyle(color: _getColorForQuality(item['item_quality']), fontWeight: FontWeight.bold)),
            Expanded(
              child: Center(
                child: Opacity(
                  opacity: 0.5,
                  child: Image.asset('assets/placeholder_item.png', fit: BoxFit.cover),
                ),
              ),
            ),
            ...bottomInfoKeys.map((key) => Align(
              alignment: Alignment.bottomRight,
              child: Text('${key.capitalize()}: ${item[key].toString()}', style: const TextStyle(color: UIColors.primaryTextColor)),
            )),
          ],
        ),
      ),
    );
  }

  Color _getColorForQuality(String quality) {
    switch (quality) {
      case 'Unique':
        return Colors.purple;
      case 'Special':
        return Colors.blue;
      case 'Rare':
        return Colors.green;
      case 'Uncommon':
        return Colors.orange;
      case 'Common':
        return Colors.grey;
      case 'Junk':
      default:
        return Colors.brown;
    }
  }
}

extension StringExtension on String {
  String capitalize() {
    return "${this[0].toUpperCase()}${substring(1)}";
  }
}

class ItemDetailsDialog extends StatefulWidget {
  final BuildContext context;
  final Map<String, dynamic> item;
  final bool showEquipButton;
  final bool showBuyButton;
  final bool showSellButton;
  final VoidCallback? onEquip;
  final VoidCallback? onBuy;
  final VoidCallback? onSell;

  const ItemDetailsDialog({
    super.key,
    required this.context,
    required this.item,
    this.showEquipButton = false,
    this.showBuyButton = false,
    this.showSellButton = false,
    this.onEquip,
    this.onBuy,
    this.onSell,
  });

  @override
  State<ItemDetailsDialog> createState() => _ItemDetailsDialogState();
}

class _ItemDetailsDialogState extends State<ItemDetailsDialog> with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _scaleAnimation;

    @override
    void initState() {
      super.initState();
      _controller = AnimationController(
        vsync: this,
        duration: const Duration(milliseconds: 300),
      );
      _scaleAnimation = CurvedAnimation(parent: _controller, curve: Curves.elasticInOut);
      _controller.forward();
    }

    @override
    void dispose() {
      _controller.dispose();
      super.dispose();
    }

    @override
    Widget build(BuildContext context) {
      return ScaleTransition(
        scale: _scaleAnimation,
        child: AlertDialog(
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(4)),
          backgroundColor: UIColors.primaryBackgroundColor,
          title: Text(widget.item['item_name'], style: const TextStyle(
            color: UIColors.primaryTextColor,
            fontSize: 20,
            fontWeight: FontWeight.bold,
          )),
          content: SingleChildScrollView(
            child: ListBody(
              children: [
                _itemDetailText('Quality: ${widget.item['item_quality']}'),
                _itemDetailText('Category: ${widget.item['category']}'),
                widget.item['item_slot'] != null ? _itemDetailText('Equipped in: ${widget.item['item_slot']}') : const SizedBox.shrink(),
                const Divider(color: Colors.grey),
                const Text(
                  'Some placeholder stats: Strength, Intelligence, etc.',
                  style: TextStyle(color: UIColors.secondaryTextColor),
                ),
              ],
            ),
          ),
          actions: <Widget>[
            if (widget.showEquipButton)
              AppTheme.customButton(
                  label: 'Equip',
                  onPressed: widget.onEquip ?? () => Navigator.of(context).pop()),
            if (widget.showBuyButton)
              AppTheme.customButton(
                  label: 'Buy',
                  onPressed: widget.onBuy ?? () => Navigator.of(context).pop()),
            if (widget.showSellButton)
              AppTheme.customButton(
                  label: 'Sell',
                  onPressed: widget.onSell ?? () => Navigator.of(context).pop()),
            AppTheme.customButton(
              label: 'Close',
              onPressed: () => Navigator.of(context).pop(),
            ),
          ],
        ),
      );
    }

  Widget _itemDetailText(String text) => Text(
    text,
    style: const TextStyle(
      color: UIColors.secondaryTextColor,
      fontSize: 16,
    ),
  );
}