import 'package:get/get.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../utils/logger.dart';

class AuthService extends GetxService {
  SharedPreferences? _prefs;
  static const String _tokenKey = 'auth_token';
  final Logger _logger = Logger('AuthService');

  Future<AuthService> init() async {
    try {
      _prefs = await SharedPreferences.getInstance();
      _logger.info('SharedPreferences initialized');
    } catch (e) {
      _logger.error('Failed to initialize SharedPreferences: $e');
    }
    return this;
  }

  String? get token {
    final t = _prefs?.getString(_tokenKey);
    if (t != null && t.isNotEmpty) {
      _logger.info('Token retrieved');
    } else {
      _logger.warning('No token found');
    }
    return t;
  }

  Future<void> saveToken(String token) async {
    try {
      await _prefs?.setString(_tokenKey, token);
      _logger.info('Token saved');
    } catch (e) {
      _logger.error('Failed to save token: $e');
    }
  }

  Future<void> removeToken() async {
    try {
      await _prefs?.remove(_tokenKey);
      _logger.info('Token removed');
    } catch (e) {
      _logger.error('Failed to remove token: $e');
    }
  }

  bool get hasToken {
    final has = token != null && token!.isNotEmpty;
    _logger.info('Has token: $has');
    return has;
  }
}