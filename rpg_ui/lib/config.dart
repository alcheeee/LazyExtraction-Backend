class SessionManager {
  static String accessToken = '';
  static bool get isAuthenticated => accessToken.isNotEmpty;
  static void logout() {
    accessToken = '';
  }
}

class APIUrl {
  static const String apiURL = 'http://10.0.2.2:8001';
}