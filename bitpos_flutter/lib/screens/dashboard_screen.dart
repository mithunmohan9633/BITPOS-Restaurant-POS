import 'package:flutter/material.dart';
import '../models/menu.dart';
import '../services/api_service.dart';
import 'active_orders_screen.dart';
import 'login_screen.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  final ApiService _apiService = ApiService();
  late Future<List<CategoryModel>> _menuFuture;
  final List<OrderItemCart> _cart = [];
  String _orderType = 'dine_in';
  String _paymentMethod = 'cash';
  bool _isSubmitting = false;

  @override
  void initState() {
    super.initState();
    _menuFuture = _apiService.getMenu();
  }

  void _addToCart(MenuItemModel item) {
    setState(() {
      final index = _cart.indexWhere((element) => element.item.id == item.id);
      if (index >= 0) {
        _cart[index].qty++;
      } else {
        _cart.add(OrderItemCart(item: item, qty: 1));
      }
    });
  }

  void _updateQty(int index, int delta) {
    setState(() {
      _cart[index].qty += delta;
      if (_cart[index].qty <= 0) {
        _cart.removeAt(index);
      }
    });
  }

  double get _cartTotal {
    return _cart.fold(0.0, (sum, item) => sum + item.total);
  }

  void _checkout() async {
    if (_cart.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Cart is empty')),
      );
      return;
    }

    setState(() {
      _isSubmitting = true;
    });

    try {
      final result = await _apiService.createOrder(
        items: _cart,
        paymentMethod: _paymentMethod,
        total: _cartTotal,
        orderType: _orderType,
        action: 'checkout',
      );

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Order Created: ${result['order_number']}')),
        );
        setState(() {
          _cart.clear();
        });
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error: $e')),
        );
      }
    } finally {
      if (mounted) {
        setState(() {
          _isSubmitting = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('BITPOS Restaurant Dashboard'),
        backgroundColor: Colors.deepOrange,
        foregroundColor: Colors.white,
        actions: [
          IconButton(
            icon: const Icon(Icons.list_alt),
            tooltip: 'Active Orders',
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const ActiveOrdersScreen()),
              );
            },
          ),
          IconButton(
            icon: const Icon(Icons.logout),
            tooltip: 'Logout',
            onPressed: () async {
              await _apiService.logout();
              if (mounted) {
                Navigator.pushReplacement(
                  context,
                  MaterialPageRoute(builder: (context) => const LoginScreen()),
                );
              }
            },
          ),
        ],
      ),
      body: Row(
        children: [
          // Menu Section
          Expanded(
            flex: 3,
            child: FutureBuilder<List<CategoryModel>>(
              future: _menuFuture,
              builder: (context, snapshot) {
                if (snapshot.connectionState == ConnectionState.waiting) {
                  return const Center(child: CircularProgressIndicator());
                } else if (snapshot.hasError) {
                  return Center(child: Text('Error: ${snapshot.error}'));
                } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
                  return const Center(child: Text('No menu items available'));
                }

                final categories = snapshot.data!;
                return ListView.builder(
                  itemCount: categories.length,
                  itemBuilder: (context, catIndex) {
                    final category = categories[catIndex];
                    return ExpansionTile(
                      initiallyExpanded: true,
                      title: Text(
                        category.name,
                        style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 18),
                      ),
                      children: [
                        GridView.builder(
                          shrinkWrap: true,
                          physics: const NeverScrollableScrollPhysics(),
                          gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                            crossAxisCount: 3,
                            childAspectRatio: 2.5,
                            crossAxisSpacing: 8,
                            mainAxisSpacing: 8,
                          ),
                          itemCount: category.items.length,
                          itemBuilder: (context, itemIndex) {
                            final item = category.items[itemIndex];
                            return InkWell(
                              onTap: () => _addToCart(item),
                              child: Card(
                                elevation: 2,
                                child: Padding(
                                  padding: const EdgeInsets.all(8.0),
                                  child: Column(
                                    crossAxisAlignment: CrossAxisAlignment.start,
                                    mainAxisAlignment: MainAxisAlignment.center,
                                    children: [
                                      Text(
                                        item.name,
                                        style: const TextStyle(fontWeight: FontWeight.bold),
                                        maxLines: 1,
                                        overflow: TextOverflow.ellipsis,
                                      ),
                                      const SizedBox(height: 4),
                                      Text(
                                        '₹${item.price.toStringAsFixed(2)}',
                                        style: const TextStyle(color: Colors.deepOrange),
                                      ),
                                    ],
                                  ),
                                ),
                              ),
                            );
                          },
                        ),
                      ],
                    );
                  },
                );
              },
            ),
          ),
          const VerticalDivider(width: 1),
          // Cart / Billing Section
          Expanded(
            flex: 2,
            child: Container(
              color: Colors.grey.shade50,
              padding: const EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  const Text(
                    'Current Order',
                    style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                  ),
                  const Divider(),
                  // Order Type & Payment Method Selectors
                  Row(
                    children: [
                      Expanded(
                        child: DropdownButtonFormField<String>(
                          value: _orderType,
                          decoration: const InputDecoration(labelText: 'Order Type'),
                          items: const [
                            DropdownMenuItem(value: 'dine_in', child: Text('Dine In')),
                            DropdownMenuItem(value: 'parcel', child: Text('Parcel')),
                          ],
                          onChanged: (val) => setState(() => _orderType = val!),
                        ),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: DropdownButtonFormField<String>(
                          value: _paymentMethod,
                          decoration: const InputDecoration(labelText: 'Payment'),
                          items: const [
                            DropdownMenuItem(value: 'cash', child: Text('Cash')),
                            DropdownMenuItem(value: 'upi', child: Text('UPI')),
                          ],
                          onChanged: (val) => setState(() => _paymentMethod = val!),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 12),
                  // Cart Items List
                  Expanded(
                    child: _cart.isEmpty
                        ? const Center(child: Text('Cart is empty. Tap menu items to add.'))
                        : ListView.builder(
                            itemCount: _cart.length,
                            itemBuilder: (context, index) {
                              final cartItem = _cart[index];
                              return ListTile(
                                title: Text(cartItem.item.name),
                                subtitle: Text('₹${cartItem.item.price} x ${cartItem.qty}'),
                                trailing: Row(
                                  mainAxisSize: MainAxisSize.min,
                                  children: [
                                    IconButton(
                                      icon: const Icon(Icons.remove_circle_outline),
                                      onPressed: () => _updateQty(index, -1),
                                    ),
                                    Text('${cartItem.qty}', style: const TextStyle(fontSize: 16)),
                                    IconButton(
                                      icon: const Icon(Icons.add_circle_outline),
                                      onPressed: () => _updateQty(index, 1),
                                    ),
                                  ],
                                ),
                              );
                            },
                          ),
                  ),
                  const Divider(),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      const Text('Total:', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                      Text('₹${_cartTotal.toStringAsFixed(2)}', style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.deepOrange)),
                    ],
                  ),
                  const SizedBox(height: 16),
                  ElevatedButton(
                    onPressed: _isSubmitting ? null : _checkout,
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.deepOrange,
                      foregroundColor: Colors.white,
                      padding: const EdgeInsets.symmetric(vertical: 16),
                    ),
                    child: _isSubmitting
                        ? const CircularProgressIndicator(color: Colors.white)
                        : const Text('Checkout & Pay', style: TextStyle(fontSize: 18)),
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
