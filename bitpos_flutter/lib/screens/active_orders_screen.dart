import 'package:flutter/material.dart';
import '../services/api_service.dart';
import 'dashboard_screen.dart';

class ActiveOrdersScreen extends StatefulWidget {
  const ActiveOrdersScreen({super.key});

  @override
  State<ActiveOrdersScreen> createState() => _ActiveOrdersScreenState();
}

class _ActiveOrdersScreenState extends State<ActiveOrdersScreen> {
  final ApiService _apiService = ApiService();
  late Future<List<dynamic>> _ordersFuture;
  bool _isProcessing = false;

  @override
  void initState() {
    super.initState();
    _ordersFuture = _apiService.getActiveOrders();
  }

  void _refresh() {
    setState(() {
      _ordersFuture = _apiService.getActiveOrders();
    });
  }

  void _checkoutOrder(String orderNumber, double totalAmount) async {
    setState(() {
      _isProcessing = true;
    });

    try {
      await _apiService.createOrder(
        items: [],
        total: totalAmount,
        action: 'bill',
        orderNumber: orderNumber,
      );

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Order #$orderNumber checked out & bill printed successfully!')),
        );
        _refresh();
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error checking out order: $e')),
        );
      }
    } finally {
      if (mounted) {
        setState(() {
          _isProcessing = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Active Orders (Pending KOT)'),
        backgroundColor: const Color(0xFFD38C44),
        foregroundColor: Colors.white,
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _refresh,
          ),
        ],
      ),
      body: FutureBuilder<List<dynamic>>(
        future: _ordersFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return const Center(child: Text('No active pending orders.'));
          }

          final orders = snapshot.data!;
          return ListView.builder(
            padding: const EdgeInsets.all(16),
            itemCount: orders.length,
            itemBuilder: (context, index) {
              final order = orders[index];
              final items = order['items'] as List;
              final orderNumber = order['order_number'];
              final totalAmount = double.parse(order['total_amount'].toString());

              return Card(
                elevation: 3,
                margin: const EdgeInsets.only(bottom: 12),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12),
                  side: const BorderSide(color: Color(0xFFE8DCCB), width: 2),
                ),
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Text(
                            'Order #$orderNumber',
                            style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Color(0xFF4A3B32)),
                          ),
                          Text(
                            '₹$totalAmount',
                            style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Color(0xFFD38C44)),
                          ),
                        ],
                      ),
                      const SizedBox(height: 4),
                      Text('Time: ${order['created_at']}', style: TextStyle(color: Colors.grey.shade600)),
                      const Divider(),
                      ...items.map((item) => Padding(
                            padding: const EdgeInsets.symmetric(vertical: 2.0),
                            child: Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              children: [
                                Text('${item['name']} x ${item['qty']}'),
                                Text('₹${item['total']}'),
                              ],
                            ),
                          )),
                      const Divider(),
                      // Action buttons: Add Items & Checkout / Print Bill
                      Row(
                        mainAxisAlignment: MainAxisAlignment.end,
                        children: [
                          OutlinedButton.icon(
                            onPressed: _isProcessing
                                ? null
                                : () {
                                    Navigator.push(
                                      context,
                                      MaterialPageRoute(
                                        builder: (context) => DashboardScreen(
                                          tableId: null,
                                          tableName: 'Order #$orderNumber',
                                          orderType: 'dine_in',
                                          existingOrderNumber: orderNumber,
                                        ),
                                      ),
                                    ).then((_) => _refresh());
                                  },
                            icon: const Icon(Icons.add_shopping_cart, size: 18),
                            label: const Text('Add Items'),
                            style: OutlinedButton.styleFrom(
                              foregroundColor: const Color(0xFFD38C44),
                              side: const BorderSide(color: Color(0xFFD38C44)),
                            ),
                          ),
                          const SizedBox(width: 12),
                          ElevatedButton.icon(
                            onPressed: _isProcessing ? null : () => _checkoutOrder(orderNumber, totalAmount),
                            icon: const Icon(Icons.receipt_long, size: 18),
                            label: const Text('Checkout & Bill'),
                            style: ElevatedButton.styleFrom(
                              backgroundColor: Colors.green.shade700,
                              foregroundColor: Colors.white,
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              );
            },
          );
        },
      ),
    );
  }
}
