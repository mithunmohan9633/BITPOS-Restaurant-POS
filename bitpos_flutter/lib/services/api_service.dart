import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import '../models/menu.dart';
import '../models/table.dart';

class ApiService {
  static const String baseUrl = 'https://bitpos-restaurant-pos.vercel.app';

  String? _cookie;

  Future<void> init() async {
    final prefs = await SharedPreferences.getInstance();
    _cookie = prefs.getString('cookie');
  }

  Future<void> _ensureInitialized() async {
    if (_cookie == null) {
      final prefs = await SharedPreferences.getInstance();
      _cookie = prefs.getString('cookie');
    }
  }

  Future<String?> login(String username, String password) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/login/'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'username': username,
          'password': password,
        }),
      );

      print('Login response status: ${response.statusCode}');
      print('Login response body: ${response.body}');

      final rawCookie = response.headers['set-cookie'];
      if (rawCookie != null) {
        _cookie = rawCookie;
        final prefs = await SharedPreferences.getInstance();
        await prefs.setString('cookie', rawCookie);
      }

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        if (data['success'] == true) {
          final prefs = await SharedPreferences.getInstance();
          await prefs.setString('role', data['role'] ?? 'user');
          await prefs.setString('username', data['username'] ?? username);
          return null;
        } else {
          return data['error'] ?? 'Login failed';
        }
      } else {
        try {
          final data = json.decode(response.body);
          if (data['error'] != null) {
            return data['error'];
          }
        } catch (_) {}
        return 'Server error: Status ${response.statusCode}';
      }
    } catch (e) {
      print('Login error: $e');
      return 'Network error: $e';
    }
  }

  Future<List<CategoryModel>> getMenu() async {
    await _ensureInitialized();
    try {
      final headers = <String, String>{};
      if (_cookie != null) {
        headers['Cookie'] = _cookie!;
      }

      final response = await http.get(
        Uri.parse('$baseUrl/api/menu/'),
        headers: headers,
      );

      if (response.statusCode == 200) {
        List data = json.decode(response.body);
        return data.map((json) => CategoryModel.fromJson(json)).toList();
      }
      throw Exception('Failed to load menu: ${response.statusCode}');
    } catch (e) {
      print('Get menu error: $e');
      rethrow;
    }
  }

  Future<List<TableModel>> getTables() async {
    await _ensureInitialized();
    try {
      final headers = <String, String>{};
      if (_cookie != null) {
        headers['Cookie'] = _cookie!;
      }

      final response = await http.get(
        Uri.parse('$baseUrl/api/tables/'),
        headers: headers,
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        List tablesList = data['tables'] ?? [];
        return tablesList.map((j) => TableModel.fromJson(j)).toList();
      }
      throw Exception('Failed to load tables');
    } catch (e) {
      print('Get tables error: $e');
      rethrow;
    }
  }

  Future<Map<String, dynamic>> createOrder({
    required List<OrderItemCart> items,
    required double total,
    int? tableId,
    String action = 'kitchen', // 'kitchen' or 'bill'
    String orderType = 'dine_in',
    String? orderNumber,
  }) async {
    await _ensureInitialized();
    try {
      final headers = <String, String>{
        'Content-Type': 'application/json',
      };
      if (_cookie != null) {
        headers['Cookie'] = _cookie!;
      }

      final body = json.encode({
        'items': items.map((i) => i.toJson()).toList(),
        'payment_method': 'cash',
        'total': total,
        'table_id': tableId,
        'action': action,
        'order_type': orderType,
        if (orderNumber != null) 'order_number': orderNumber,
      });

      final response = await http.post(
        Uri.parse('$baseUrl/api/create-order/'),
        headers: headers,
        body: body,
      );

      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('Failed to create order: ${response.body}');
      }
    } catch (e) {
      print('Create order error: $e');
      rethrow;
    }
  }

  Future<List<dynamic>> getActiveOrders() async {
    await _ensureInitialized();
    try {
      final headers = <String, String>{};
      if (_cookie != null) {
        headers['Cookie'] = _cookie!;
      }

      final response = await http.get(
        Uri.parse('$baseUrl/api/active-orders/'),
        headers: headers,
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return data['orders'] ?? [];
      }
      throw Exception('Failed to load active orders');
    } catch (e) {
      print('Active orders error: $e');
      rethrow;
    }
  }

  Future<String> getUserRole() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString('role') ?? 'user';
  }

  Future<String> getUsername() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString('username') ?? 'User';
  }

  Future<void> logout() async {
    _cookie = null;
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('cookie');
    await prefs.remove('role');
    await prefs.remove('username');
    try {
      await http.get(Uri.parse('$baseUrl/logout/'));
    } catch (_) {}
  }
}
