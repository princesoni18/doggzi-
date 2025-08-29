import 'package:flutter/foundation.dart';

class Logger {
  final String tag;

  Logger(this.tag);

  void info(String message) {
    _log('INFO', message);
  }

  void warning(String message) {
    _log('WARNING', message);
  }

  void error(String message) {
    _log('ERROR', message);
  }

  void _log(String level, String message) {
    final logMessage = '[$level][$tag] $message';
    if (kDebugMode) {
      print(logMessage);
    }
    // Extend here for file logging, remote logging, etc.
  }
}
