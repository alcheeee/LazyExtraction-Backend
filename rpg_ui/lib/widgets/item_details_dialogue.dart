import 'package:flutter/material.dart';
import '../common_imports.dart';

class ItemDetailsDialog extends StatefulWidget {
  final Item item;
  final bool showEquipButton;
  final bool showBuyButton;
  final bool showSellButton;
  final VoidCallback? onEquip;
  final VoidCallback? onBuy;
  final VoidCallback? onSell;

  const ItemDetailsDialog({
    super.key,
    required this.item,
    this.showEquipButton = false,
    this.showBuyButton = false,
    this.showSellButton = false,
    this.onEquip,
    this.onBuy,
    this.onSell,
  });

  @override
  _ItemDetailsDialogState createState() => _ItemDetailsDialogState();
}

class _ItemDetailsDialogState extends State<ItemDetailsDialog> with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _scaleAnimation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 100),
    );
    _scaleAnimation = CurvedAnimation(parent: _controller, curve: Curves.elasticInOut);
    _controller.forward();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  // Text(item.itemName, style: TextStyle(color: item.qualityColor, fontWeight: FontWeight.bold)),
  // child: Image.asset(item.itemAsset, fit: BoxFit.cover)

  @override
  Widget build(BuildContext context) {
    return ScaleTransition(
      scale: _scaleAnimation,
      child: AlertDialog(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(2)),
        backgroundColor: UIColors.primaryBackgroundColor,
        title: Text(widget.item.itemName, style: TextStyle(
          color: widget.item.qualityColor,
          fontSize: 20,
          fontWeight: FontWeight.bold,
        )),
        content: SingleChildScrollView(
          child: ListBody(
            children: [
              _itemDetailText(widget.item.itemQuality, widget.item.qualityColor),
              _itemDetailText('Category: ${widget.item.category}', UIColors.secondaryTextColor),
              if (widget.item.slotType != null) _itemDetailText('Equip Type: ${widget.item.slotType!}', UIColors.secondaryTextColor),
              if (widget.item.stats != null) _statSection(widget.item.stats!),
            ],
          ),
        ),
        actions: <Widget>[
          if (widget.showEquipButton)
            AppTheme.customButton(
                label: widget.item.equippedSlot == null ? 'Equip' : 'Unequip',
                onPressed: widget.onEquip ?? () => Navigator.of(context).pop()),
          if (widget.showBuyButton)
            AppTheme.customButton(
                label: 'Buy', onPressed: widget.onBuy ?? () => Navigator.of(context).pop()),
          if (widget.showSellButton)
            AppTheme.customButton(
                label: 'Sell', onPressed: widget.onSell ?? () => Navigator.of(context). pop()),
          AppTheme.customButton(label: 'Close', onPressed: () => Navigator.of(context).pop()),
        ],
      ),
    );
  }

  Widget _itemDetailText(String value, Color valueColor) {
    return RichText(
      text: TextSpan(
        style: const TextStyle(
          fontSize: 16,
          color: UIColors.secondaryTextColor,
        ),
        children: <TextSpan>[
          TextSpan(text: value, style: TextStyle(color: valueColor)),
        ],
      ),
    );
  }

  Widget _statSection(Map<String, dynamic> stats) {
    return Container(
      margin: const EdgeInsets.only(top: 12),
      padding: const EdgeInsets.all(8),
      decoration: BoxDecoration(
        color: UIColors.secondaryBackgroundColor,
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: UIColors.primaryOutlineColor),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: stats.entries.map((entry) => Text(
          '+ ${_formatStatName(entry.key)}: ${entry.value}',
          style: TextStyle(color: Colors.greenAccent[700], fontSize: 16),
        )).toList(),
      ),
    );
  }

  String _formatStatName(String statName) {
    return statName.replaceAll('_', ' ').split(' ').map((str) => str.capitalize()).join(' ');
  }
}

extension on String {
  String capitalize() {
    if (isEmpty) return this;
    return "${this[0].toUpperCase()}${substring(1).toLowerCase()}";
  }
}