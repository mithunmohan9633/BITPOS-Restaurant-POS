import 'package:flutter/material.dart';
import '../models/table.dart';
import '../services/api_service.dart';
import '../widgets/app_drawer.dart';
import 'dashboard_screen.dart';
import 'active_orders_screen.dart';
import 'login_screen.dart';

class TableSelectionScreen extends StatefulWidget {
  const TableSelectionScreen({super.key});

  @override
  State<TableSelectionScreen> createState() => _TableSelectionScreenState();
}

class _TableSelectionScreenState extends State<TableSelectionScreen> {
  final ApiService _apiService = ApiService();
  late Future<List<TableModel>> _tablesFuture;
  String _staffName = '';

  @override
  void initState() {
    super.initState();
    _apiService.init();
    _tablesFuture = _apiService.getTables();
    _loadStaffName();
  }

  void _loadStaffName() async {
    final name = await _apiService.getUsername();
    setState(() {
      _staffName = name;
    });
  }

  void _refresh() {
    setState(() {
      _tablesFuture = _apiService.getTables();
    });
  }

  @override
  Widget build(BuildContext context) {
    const primaryColor = Color(0xFFD38C44);
    const textColor = Color(0xFF4A3B32);
    const bgColor = Color(0xFFFDF8F5);

    return Scaffold(
      backgroundColor: bgColor,
      appBar: AppBar(
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Select Table or Order Type', style: TextStyle(color: textColor, fontWeight: FontWeight.bold)),
            Text('Staff: $_staffName', style: const TextStyle(fontSize: 12, color: Colors.grey)),
          ],
        ),
        backgroundColor: Colors.white,
        foregroundColor: textColor,
        elevation: 0,
        iconTheme: const IconThemeData(color: textColor),
        actions: [
          IconButton(
            icon: const Icon(Icons.list_alt, color: primaryColor),
            tooltip: 'Active Orders',
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const ActiveOrdersScreen()),
              );
            },
          ),
          IconButton(
            icon: const Icon(Icons.refresh, color: primaryColor),
            onPressed: _refresh,
          ),
        ],
      ),
      drawer: const AppDrawer(),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Parcel / Takeaway Quick Action Button
            ElevatedButton.icon(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => const DashboardScreen(
                      tableId: null,
                      tableName: 'Parcel / Takeaway',
                      orderType: 'parcel',
                    ),
                  ),
                );
              },
              icon: const Icon(Icons.shopping_bag, size: 28),
              label: const Text('New Parcel / Takeaway Order', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              style: ElevatedButton.styleFrom(
                backgroundColor: primaryColor,
                foregroundColor: Colors.white,
                padding: const EdgeInsets.symmetric(vertical: 16),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
              ),
            ),
            const SizedBox(height: 24),
            const Text(
              'Dine-In Tables',
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: textColor),
            ),
            const SizedBox(height: 12),
            Expanded(
              child: FutureBuilder<List<TableModel>>(
                future: _tablesFuture,
                builder: (context, snapshot) {
                  if (snapshot.connectionState == ConnectionState.waiting) {
                    return const Center(child: CircularProgressIndicator());
                  } else if (snapshot.hasError) {
                    return Center(child: Text('Error loading tables: ${snapshot.error}'));
                  } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
                    return const Center(
                      child: Text(
                        'No tables configured for this store.\nPlease add tables via Web Admin.',
                        textAlign: TextAlign.center,
                        style: TextStyle(fontSize: 16, color: Colors.grey),
                      ),
                    );
                  }

                  final tables = snapshot.data!;
                  return GridView.builder(
                    gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                      crossAxisCount: 3,
                      childAspectRatio: 1.2,
                      crossAxisSpacing: 12,
                      mainAxisSpacing: 12,
                    ),
                    itemCount: tables.length,
                    itemBuilder: (context, index) {
                      final table = tables[index];
                      return InkWell(
                        onTap: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (context) => DashboardScreen(
                                tableId: table.id,
                                tableName: 'Table ${table.tableNumber}',
                                orderType: 'dine_in',
                              ),
                            ),
                          );
                        },
                        child: Card(
                          elevation: 2,
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(12),
                            side: const BorderSide(
                              color: Color(0xFFE8DCCB),
                              width: 2,
                            ),
                          ),
                          child: Padding(
                            padding: const EdgeInsets.all(12.0),
                            child: Column(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                Icon(
                                  Icons.table_restaurant,
                                  size: 36,
                                  color: table.isOccupied ? Colors.orange.shade700 : primaryColor,
                                ),
                                const SizedBox(height: 8),
                                Text(
                                  'Table ${table.tableNumber}',
                                  style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: textColor),
                                  textAlign: TextAlign.center,
                                ),
                                const SizedBox(height: 4),
                                Text(
                                  table.isOccupied ? 'Occupied' : 'Available',
                                  style: TextStyle(
                                    fontSize: 12,
                                    color: table.isOccupied ? Colors.orange.shade800 : Colors.green.shade700,
                                    fontWeight: FontWeight.w600,
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ),
                      );
                    },
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}
