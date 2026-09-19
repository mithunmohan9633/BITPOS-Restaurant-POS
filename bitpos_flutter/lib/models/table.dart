class TableModel {
  final int id;
  final String tableNumber;
  final int seatingCapacity;
  final bool isOccupied;

  TableModel({
    required this.id,
    required this.tableNumber,
    required this.seatingCapacity,
    required this.isOccupied,
  });

  factory TableModel.fromJson(Map<String, dynamic> json) {
    return TableModel(
      id: json['id'],
      tableNumber: json['table_number'].toString(),
      seatingCapacity: json['seating_capacity'] ?? 4,
      isOccupied: json['is_occupied'] ?? false,
    );
  }
}
