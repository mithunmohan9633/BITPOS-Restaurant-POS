import 'package:flutter/material.dart';
import 'screens/login_screen.dart';

void main() {
  runApp(const BitposApp());
}

class BitposApp extends StatelessWidget {
  const BitposApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'BITPOS Restaurant POS',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepOrange),
        useMaterial3: true,
      ),
      home: const LoginScreen(),
      debugShowCheckedModeBanner: false,
    );
  }
}
