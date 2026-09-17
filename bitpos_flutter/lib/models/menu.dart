class MenuItemModel {
  final int id;
  final String name;
  final double price;

  MenuItemModel({
    required this.id,
    required this.name,
    required this.price,
  });

  factory MenuItemModel.fromJson(Map<String, dynamic> json) {
    return MenuItemModel(
      id: json['id'],
      name: json['name'],
      price: double.parse(json['price'].toString()),
    );
  }
}

class CategoryModel {
  final int id;
  final String name;
  final List<MenuItemModel> items;

  CategoryModel({
    required this.id,
    required this.name,
    required this.items,
  });

  factory CategoryModel.fromJson(Map<String, dynamic> json) {
    var itemsList = json['items'] as List? ?? [];
    List<MenuItemModel> parsedItems =
        itemsList.map((i) => MenuItemModel.fromJson(i)).toList();

    return CategoryModel(
      id: json['id'],
      name: json['name'],
      items: parsedItems,
    );
  }
}

class OrderItemCart {
  final MenuItemModel item;
  int qty;

  OrderItemCart({
    required this.item,
    required this.qty,
  });

  double get total => item.price * qty;

  Map<String, dynamic> toJson() {
    return {
      'id': item.id,
      'qty': qty,
    };
  }
}
