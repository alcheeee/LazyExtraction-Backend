import 'attachments.dart';
import 'weapons.dart';
import 'armor.dart';
import 'bullets.dart';
import 'medical.dart';

class ItemType {
  static const Weapon = 'Weapon';
  static const Armor = 'Armor';
  static const Clothing = 'Clothing';
  static const Medical = 'Medical';
  static const Bullets = 'Bullets';
  static const Attachments = 'Attachments';
  static const Valuable = 'Valuable';
}

Map<String, Map<String, dynamic>> getItemCatalogByType(String type) {
  switch (type) {
    case ItemType.Attachments:
      return attachmentsCatalog;
    case ItemType.Weapon:
      return weaponsCatalog;
    case ItemType.Armor:
      return armorCatalog;
    case ItemType.Bullets:
      return bulletsCatalog;
    case ItemType.Medical:
      return medicalCatalog;
    default:
      return {};
  }
}

Map<String, dynamic>? getItemByName(String itemName) {
  for (var catalog in [
    attachmentsCatalog,
    weaponsCatalog,
    armorCatalog,
    bulletsCatalog,
    medicalCatalog
  ]) {
    if (catalog.containsKey(itemName)) {
      return catalog[itemName];
    }
  }
  return null;
}

List<Map<String, dynamic>> getItemsSortedByName(String type) {
  Map<String, Map<String, dynamic>> catalog = getItemCatalogByType(type);
  List<Map<String, dynamic>> items = catalog.values.toList();
  items.sort((a, b) => a['item_name'].compareTo(b['item_name']));
  return items;
}
