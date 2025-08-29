class Pet {
  final String id;
  final String name;
  final String type;
  final String? breed;
  final int? age;
  final String? notes;

  Pet({
    required this.id,
    required this.name,
    required this.type,
    this.breed,
    this.age,
    this.notes,
  });

  factory Pet.fromJson(Map<String, dynamic> json) {
    return Pet(
      id: json['id'].toString(),
      name: json['name'] ?? '',
      type: json['type'] ?? '',
      breed: json['breed'] ?? '',
      age: json['age'],
      notes: json['notes'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'name': name,
      'type': type,
      'breed': breed,
      'age': age,
      'notes': notes,
    };
  }
}
