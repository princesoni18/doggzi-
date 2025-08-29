import 'dart:convert';
import 'package:doggzi/core/constants.dart';
import 'package:doggzi/modules/pets/data/pets_model.dart';
import 'package:doggzi/utils/logger.dart';
import 'package:get/get.dart';
import 'package:http/http.dart' as http;

import 'auth_service.dart';

class ApiService extends GetxService {
  final String baseUrl = base_url; // Replace with your API URL
  final AuthService _authService = Get.find();

  Map<String, String> get _headers {
    final headers = {'Content-Type': 'application/json'};
    if (_authService.hasToken) {
      headers['Authorization'] = 'Bearer ${_authService.token}';
    }
    return headers;
  }

  // Auth endpoints
  Future<Map<String, dynamic>> login(String email, String password) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/auth/login'),
        headers: _headers,
        body: jsonEncode({'email': email, 'password': password}),
      );

      if (response.statusCode == 200) {
        Logger("API service").info(response.body);
        return jsonDecode(response.body);
      } else {
        throw Exception(_getErrorMessage(response));
      }
    } catch (e) {
      throw Exception('Login failed: $e');
    }
  }

  Future<Map<String, dynamic>> register(String name, String email, String password) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/auth/register'),
        headers: _headers,
      
        body: jsonEncode({
           'email': email,
          'user_name': name,
         
          'password': password,
        }),
      );
      
      if (response.statusCode == 201||response.statusCode==200) {
        return jsonDecode(response.body);
      } else {
        throw Exception(_getErrorMessage(response));
      }
    } catch (e) {
      throw Exception('Registration failed: $e');
    }
  }

  // Pet endpoints
  Future<List<Pet>> getPets() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/pets'),
        headers: _headers,
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body);
        return data.map((json) => Pet.fromJson(json)).toList();
      } else {
        throw Exception(_getErrorMessage(response));
      }
    } catch (e) {
      throw Exception('Failed to load pets: $e');
    }
  }

  Future<Pet> addPet(Pet pet) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/pets/'),
        headers: _headers,
        body: jsonEncode(pet.toJson()),
      );

      if (response.statusCode == 201||response.statusCode == 200 ) {
        return Pet.fromJson(jsonDecode(response.body));
      } else {
        throw Exception(_getErrorMessage(response));
      }
    } catch (e) {
      throw Exception('Failed to add pet: $e');
    }
  }

  String _getErrorMessage(http.Response response) {
    try {
      final error = jsonDecode(response.body);
      return error['message'] ?? 'Unknown error occurred';
    } catch (e) {
      return 'HTTP ${response.statusCode}: ${response.reasonPhrase}';
    }
  }
}