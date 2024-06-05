import 'package:flutter/material.dart';

final ThemeData darkTheme = ThemeData(
  brightness: Brightness.dark,
  primaryColor: Colors.blue,
  scaffoldBackgroundColor: Colors.grey[900],
  appBarTheme: const AppBarTheme(
    color: Colors.black,
    iconTheme: IconThemeData(color: Colors.white),
    titleTextStyle: TextStyle(color: Colors.white, fontSize: 20),
  ),
  textTheme: const TextTheme(
    bodyLarge: TextStyle(color: Colors.white),
    bodyMedium: TextStyle(color: Colors.white),
  ),
  buttonTheme: const ButtonThemeData(
    buttonColor: Colors.blue,
    textTheme: ButtonTextTheme.primary,
  ),
  elevatedButtonTheme: ElevatedButtonThemeData(
    style: ElevatedButton.styleFrom(
      foregroundColor: Colors.white, backgroundColor: Colors.blue,
    ),
  ),
);


Color getTierColor(String tier) {
  switch (tier) {
    case 'ItemTier.Tier1':
      return Colors.grey;
    case 'ItemTier.Tier2':
      return Colors.green;
    case 'ItemTier.Tier3':
      return Colors.blue;
    case 'ItemTier.Tier4':
      return Colors.purple;
    case 'ItemTier.Tier5':
      return Colors.yellow;
    default:
      return Colors.grey;
  }
}
