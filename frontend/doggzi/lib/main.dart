import 'package:doggzi/modules/auth/controllers/auth_controller.dart';
import 'package:doggzi/modules/auth/presentation/login_screen.dart';
import 'package:doggzi/modules/pets/presentation/pets_list_screen.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'services/auth_service.dart';
import 'services/api_service.dart';


void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Initialize services
  await Get.putAsync(() => AuthService().init());
  Get.put(ApiService());
  Get.put(AuthController());
  
  runApp(const PetApp());
}

class PetApp extends StatelessWidget {
  const PetApp({super.key});
  @override
  Widget build(BuildContext context) {
    return GetMaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Pet Manager',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: GetX<AuthController>(
        builder: (controller) {
          return controller.isLoggedIn.value 
            ? PetListScreen() 
            : LoginScreen();
        },
      ),
      getPages: [
        GetPage(name: '/login', page: () => LoginScreen()),
        GetPage(name: '/pets', page: () => PetListScreen()),
      ],
    );
  }
}