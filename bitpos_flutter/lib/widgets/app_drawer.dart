import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../screens/table_selection_screen.dart';
import '../screens/active_orders_screen.dart';
import '../screens/settings_screen.dart';
import '../screens/login_screen.dart';

class AppDrawer extends StatefulWidget {
  const AppDrawer({super.key});

  @override
  State<AppDrawer> createState() => _AppDrawerState();
}

class _AppDrawerState extends State<AppDrawer> {
  final ApiService _apiService = ApiService();
  String _userName = '';
  String _userRole = '';

  @override
  void initState() {
    super.initState();
    _loadInfo();
  }

  void _loadInfo() async {
    final name = await _apiService.getUsername();
    final role = await _apiService.getUserRole();
    setState(() {
      _userName = name;
      _userRole = role;
    });
  }

  @override
  Widget build(BuildContext context) {
    const primaryColor = Color(0xFFD38C44);
    const textColor = Color(0xFF4A3B32);

    return Drawer(
      backgroundColor: const Color(0xFFFDF8F5),
      child: ListView(
        padding: EdgeInsets.zero,
        children: [
          UserAccountsDrawerHeader(
            decoration: const BoxDecoration(
              color: primaryColor,
            ),
            currentAccountPicture: CircleAvatar(
              backgroundColor: Colors.white,
              child: Text(
                _userName.isNotEmpty ? _userName[0].toUpperCase() : 'B',
                style: const TextStyle(fontSize: 28, fontWeight: FontWeight.bold, color: primaryColor),
              ),
            ),
            accountName: Text(
              _userName,
              style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            accountEmail: Text(
              'Role: ${_userRole.toUpperCase()}',
              style: const TextStyle(fontSize: 13, color: Colors.white70),
            ),
          ),
          ListTile(
            leading: const Icon(Icons.table_restaurant, color: primaryColor),
            title: const Text('Table Selection', style: TextStyle(fontWeight: FontWeight.bold, color: textColor)),
            onTap: () {
              Navigator.pushReplacement(
                context,
                MaterialPageRoute(builder: (context) => const TableSelectionScreen()),
              );
            },
          ),
          ListTile(
            leading: const Icon(Icons.list_alt, color: primaryColor),
            title: const Text('Active Orders (KOT)', style: TextStyle(fontWeight: FontWeight.bold, color: textColor)),
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const ActiveOrdersScreen()),
              );
            },
          ),
          const Divider(color: Color(0xFFE8DCCB)),
          ListTile(
            leading: const Icon(Icons.settings, color: primaryColor),
            title: const Text('Settings', style: TextStyle(fontWeight: FontWeight.bold, color: textColor)),
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const SettingsScreen()),
              );
            },
          ),
          const Divider(color: Color(0xFFE8DCCB)),
          ListTile(
            leading: const Icon(Icons.logout, color: Colors.red),
            title: const Text('Logout', style: TextStyle(fontWeight: FontWeight.bold, color: Colors.red)),
            onTap: () async {
              await _apiService.logout();
              if (mounted) {
                Navigator.pushAndRemoveUntil(
                  context,
                  MaterialPageRoute(builder: (context) => const LoginScreen()),
                  (route) => false,
                );
              }
            },
          ),
        ],
      ),
    );
  }
}
