import 'package:doggzi/modules/pets/data/pets_model.dart';
import 'package:doggzi/services/api_service.dart';
import 'package:get/get.dart';


class PetController extends GetxController {
  final ApiService _apiService = Get.find();

  final RxList<Pet> pets = <Pet>[].obs;
  final RxBool isLoading = false.obs;
  final RxBool isAddingPet = false.obs;

  @override
  void onInit() {
    super.onInit();
    loadPets();
  }

  Future<void> loadPets() async {
    try {
      isLoading.value = true;
      pets.value = await _apiService.getPets();
    } catch (e) {
      Get.snackbar('Error', _getErrorMessage(e));
    } finally {
      isLoading.value = false;
    }
  }

  Future<void> addPet(Pet pet) async {
    try {
      isAddingPet.value = true;
      final newPet = await _apiService.addPet(pet);
      pets.add(newPet);
      Get.back();
      Get.snackbar('Success', 'Pet added successfully!');
    } catch (e) {
      Get.snackbar('Error', _getErrorMessage(e));
    } finally {
      isAddingPet.value = false;
    }
  }
  String _getErrorMessage(dynamic e) {
    // Customize for different error types if needed
    if (e is String) {
      return e;
    }
    if (e is Exception) {
      final msg = e.toString();
      if (msg.contains('Timeout')) return 'Request timed out. Please try again.';
      if (msg.contains('Network')) return 'Network error. Please check your connection.';
      if (msg.contains('Unauthorized')) return 'You are not authorized.';
      return 'Something went wrong. Please try again.';
    }
    return 'An unexpected error occurred.';
  }

  Future<void> refreshPets() async {
    await loadPets();
  }
}