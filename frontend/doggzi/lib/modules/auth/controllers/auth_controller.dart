import 'package:doggzi/modules/auth/data/user_model.dart';
import 'package:doggzi/services/api_service.dart';
import 'package:doggzi/services/auth_service.dart';
import 'package:get/get.dart';

class AuthController extends GetxController {
  final AuthService _authService = Get.find();
  final ApiService _apiService = Get.find();

  final RxBool isLoading = false.obs;
  final RxBool isLoggedIn = false.obs;
  final Rx<User?> currentUser = Rx<User?>(null);

  @override
  void onInit() {
    super.onInit();
    checkAuthStatus();
  }

  void checkAuthStatus() {
    isLoggedIn.value = _authService.hasToken;
  }

  Future<void> login(String email, String password) async {
    try {
      isLoading.value = true;
      final response = await _apiService.login(email, password);
      
      await _authService.saveToken(response['access_token']);
      currentUser.value = User.fromJson(response['user']);
      isLoggedIn.value = true;
      
      Get.offAllNamed('/pets');
      Get.snackbar('Success', 'Logged in successfully!');
    } catch (e) {
      Get.snackbar('Error', _getErrorMessage(e));
    } finally {
      isLoading.value = false;
    }
  }

  Future<void> register(String name, String email, String password) async {
    try {
      isLoading.value = true;
      final response = await _apiService.register(name, email, password);

      await _authService.saveToken(response['access_token']);
      currentUser.value = User.fromJson(response['user']);
      isLoggedIn.value = true;
      
      Get.offAllNamed('/pets');
      Get.snackbar('Success', 'Account created successfully!');
    } catch (e) {
      Get.snackbar('Error', _getErrorMessage(e));
    } finally {
      isLoading.value = false;
    }
  }
  String _getErrorMessage(dynamic e) {
    if (e is String) {
      return e;
    }
    if (e is Exception) {
      final msg = e.toString();
      if (msg.contains('Timeout')) return 'Request timed out. Please try again.';
      if (msg.contains('Network')) return 'Network error. Please check your connection.';
      if (msg.contains('Unauthorized')) return 'Invalid credentials or unauthorized.';
      if (msg.contains('email')) return 'Please check your email address.';
      return 'Something went wrong. Please try again.';
    }
    return 'An unexpected error occurred.';
  }

  Future<void> logout() async {
    await _authService.removeToken();
    currentUser.value = null;
    isLoggedIn.value = false;
    Get.offAllNamed('/login');
  }
}