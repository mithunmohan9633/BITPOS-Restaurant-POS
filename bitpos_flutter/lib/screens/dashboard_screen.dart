import 'package:flutter/material.dart';
import '../models/menu.dart';
import '../services/api_service.dart';
import 'active_orders_screen.dart';
import 'login_screen.dart';

class DashboardScreen extends StatefulWidget {
  final int? tableId;
  final String tableName;
  final String orderType;
  final String? existingOrderNumber;

  const DashboardScreen({
    super.key,
    required this.tableId,
    required this.tableName,
    required this.orderType,
    this.existingOrderNumber,
  });

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  final ApiService _apiService = ApiService();
  late Future<List<CategoryModel>> _menuFuture;
  final List<OrderItemCart> _cart = [];
  bool _isSubmitting = false;
  String _userRole = 'user';
  String _userName = '';

  @override
  void initState() {
    super.initState();
    _menuFuture = _apiService.getMenu();
    _loadUserInfo();
  }

  void _loadUserInfo() async {
    final role = await _apiService.getUserRole();
    final name = await _apiService.getUsername();
    setState(() {
      _userRole = role;
      _userName = name;
    });
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

  int get _cartItemCount {
    return _cart.fold(0, (sum, item) => sum + item.qty);
  }

  void _submitOrder(String action) async {
    if (_cart.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Cart is empty. Please select menu items.')),
      );
      return;
    }

    setState(() {
      _isSubmitting = true;
    });

    try {
      final result = await _apiService.createOrder(
        items: _cart,
        total: _cartTotal,
        tableId: widget.tableId,
        action: action, // 'kitchen' or 'bill'
        orderType: widget.orderType,
        orderNumber: widget.existingOrderNumber,
      );

      if (mounted) {
        final actionName = action == 'kitchen' ? 'Sent to Kitchen (KOT)' : 'Bill Printed';
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('$actionName successfully! Order #${result['order_number']}')),
        );
        setState(() {
          _cart.clear();
        });
        if (Navigator.canPop(context)) {
          Navigator.pop(context);
        }
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

  void _showCartBottomSheet() {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (context) {
        return DraggableScrollableSheet(
          initialChildSize: 0.7,
          minChildSize: 0.4,
          maxChildSize: 0.95,
          expand: false,
          builder: (context, scrollController) {
            return Padding(
              padding: const EdgeInsets.all(16.0),
              child: _buildCartContent(scrollController),
            );
          },
        );
      },
    );
  }

  Widget _buildCartContent(ScrollController? scrollController) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(
              'Order: ${widget.tableName}',
              style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            IconButton(
              icon: const Icon(Icons.close),
              onPressed: () => Navigator.pop(context),
            ),
          ],
        ),
        const Divider(),
        Expanded(
          child: _cart.isEmpty
              ? const Center(child: Text('Cart is empty. Tap menu items to add.'))
              : ListView.builder(
                  controller: scrollController,
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
        const SizedBox(height: 12),
        // Action Buttons for Staff: Proceed to Kitchen & Print Bill
        Row(
          children: [
            Expanded(
              child: ElevatedButton.icon(
                onPressed: _isSubmitting ? null : () => _submitOrder('kitchen'),
                icon: const Icon(Icons.kitchen),
                label: const Text('Proceed to Kitchen'),
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.orange.shade800,
                  foregroundColor: Colors.white,
                  padding: const EdgeInsets.symmetric(vertical: 14),
                ),
              ),
            ),
            const SizedBox(width: 8),
            Expanded(
              child: ElevatedButton.icon(
                onPressed: _isSubmitting ? null : () => _submitOrder('bill'),
                icon: const Icon(Icons.receipt),
                label: const Text('Print Bill'),
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.green.shade700,
                  foregroundColor: Colors.white,
                  padding: const EdgeInsets.symmetric(vertical: 14),
                ),
              ),
            ),
          ],
        ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    final screenWidth = MediaQuery.of(context).size.width;
    final isWideScreen = screenWidth >= 800;
    final crossAxisCount = screenWidth >= 1200 ? 4 : (screenWidth >= 800 ? 3 : 2);

    return Scaffold(
      appBar: AppBar(
        title: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(widget.tableName, style: const TextStyle(fontSize: 18)),
            Text('Staff: $_userName', style: const TextStyle(fontSize: 12, color: Colors.white70)),
          ],
        ),
        backgroundColor: const Color(0xFFD38C44),
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
            flex: isWideScreen ? 3 : 1,
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
                  padding: const EdgeInsets.all(8),
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
                          gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                            crossAxisCount: crossAxisCount,
                            childAspectRatio: 2.2,
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
          // Cart Section for Wide Screens (Tablets / Desktops)
          if (isWideScreen) ...[
            const VerticalDivider(width: 1),
            Expanded(
              flex: 2,
              child: Container(
                color: Colors.grey.shade50,
                padding: const EdgeInsets.all(16.0),
                child: _buildCartContent(null),
              ),
            ),
          ],
        ],
      ),
      // Floating Cart Bar for Mobile Phones (< 800px width)
      bottomNavigationBar: !isWideScreen && _cart.isNotEmpty
          ? Container(
              color: Colors.deepOrange,
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    '$_cartItemCount items | ₹${_cartTotal.toStringAsFixed(2)}',
                    style: const TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold),
                  ),
                  ElevatedButton(
                    onPressed: _showCartBottomSheet,
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.white,
                      foregroundColor: Colors.deepOrange,
                    ),
                    child: const Text('View Cart'),
                  ),
                ],
              ),
            )
          : null,
    );
  }
}
