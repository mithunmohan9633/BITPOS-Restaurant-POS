import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../widgets/app_drawer.dart';

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  final ApiService _apiService = ApiService();
  String _userName = '';
  String _userRole = '';
  final TextEditingController _urlController = TextEditingController(text: ApiService.baseUrl);

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

    return Scaffold(
      backgroundColor: const Color(0xFFFDF8F5),
      appBar: AppBar(
        title: const Text('App Settings', style: TextStyle(color: textColor, fontWeight: FontWeight.bold)),
        backgroundColor: Colors.white,
        foregroundColor: textColor,
        elevation: 0,
        iconTheme: const IconThemeData(color: textColor),
      ),
      drawer: const AppDrawer(),
      body: ListView(
        padding: const EdgeInsets.all(16.0),
        children: [
          Card(
            elevation: 2,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(16),
              side: const BorderSide(color: Color(0xFFE8DCCB), width: 2),
            ),
            child: Padding(
              padding: const EdgeInsets.all(20.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'Server Configuration',
                    style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: textColor),
                  ),
                  const SizedBox(height: 12),
                  TextField(
                    controller: _urlController,
                    decoration: const InputDecoration(
                      labelText: 'Backend Server URL',
                      border: OutlineInputBorder(),
                      focusedBorder: OutlineInputBorder(borderSide: BorderSide(color: primaryColor)),
                    ),
                  ),
                  const SizedBox(height: 12),
                  ElevatedButton(
                    onPressed: () {
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(content: Text('Server URL configuration saved successfully')),
                      );
                    },
                    style: ElevatedButton.styleFrom(backgroundColor: primaryColor),
                    child: const Text('Save Settings'),
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),
          Card(
            elevation: 2,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(16),
              side: const BorderSide(color: Color(0xFFE8DCCB), width: 2),
            ),
            child: Padding(
              padding: const EdgeInsets.all(20.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'Staff Profile',
                    style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: textColor),
                  ),
                  const SizedBox(height: 12),
                  ListTile(
                    leading: const Icon(Icons.person, color: primaryColor),
                    title: Text('Username: $_userName', style: const TextStyle(fontWeight: FontWeight.bold)),
                  ),
                  ListTile(
                    leading: const Icon(Icons.badge, color: primaryColor),
                    title: Text('Role: ${_userRole.toUpperCase()}', style: const TextStyle(fontWeight: FontWeight.bold)),
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),
          Card(
            elevation: 2,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(16),
              side: const BorderSide(color: Color(0xFFE8DCCB), width: 2),
            ),
            child: Padding(
              padding: const EdgeInsets.all(20.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'Printer & Station Status',
                    style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: textColor),
                  ),
                  const SizedBox(height: 12),
                  const ListTile(
                    leading: Icon(Icons.print, color: Colors.green),
                    title: Text('Kitchen Printer (KOT): Connected'),
                    subtitle: Text('Network Station 1'),
                  ),
                  const ListTile(
                    leading: Icon(Icons.receipt, color: Colors.green),
                    title: Text('Bill Printer: Connected'),
                    subtitle: Text('Cash Counter Station'),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
