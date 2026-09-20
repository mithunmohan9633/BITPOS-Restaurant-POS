import 'package:flutter/material.dart';
import 'screens/login_screen.dart';

void main() {
  runApp(const BitposApp());
}

class BitposApp extends StatelessWidget {
  const BitposApp({super.key});

  @override
  Widget build(BuildContext context) {
    const primaryColor = Color(0xFFD38C44);
    const bgColor = Color(0xFFFDF8F5);
    const textColor = Color(0xFF4A3B32);
    const borderColor = Color(0xFFE8DCCB);

    return MaterialApp(
      title: 'BITPOS',
      theme: ThemeData(
        useMaterial3: true,
        scaffoldBackgroundColor: bgColor,
        colorScheme: ColorScheme.fromSeed(
          seedColor: primaryColor,
          primary: primaryColor,
          surface: Colors.white,
          onSurface: textColor,
        ),
        appBarTheme: const AppBarTheme(
          backgroundColor: Colors.white,
          foregroundColor: textColor,
          elevation: 0,
          surfaceTintColor: Colors.transparent,
        ),
        cardTheme: CardThemeData(
          color: Colors.white,
          elevation: 2,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(14),
            side: const BorderSide(color: borderColor, width: 2),
          ),
        ),
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            backgroundColor: primaryColor,
            foregroundColor: Colors.white,
            elevation: 0,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(10),
            ),
          ),
        ),
      ),
      home: const LoginScreen(),
      debugShowCheckedModeBanner: false,
    );
  }
}
