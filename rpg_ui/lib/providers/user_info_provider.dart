import 'package:flutter/foundation.dart';
import '../api_calls/user_info_api.dart';
import '../models/user_model.dart';
import 'package:collection/collection.dart';

class UserStatsProvider with ChangeNotifier {
  UserInfo _userInfo = UserInfo.dummy();
  bool _isLoading = true;
  final _cache = <String, dynamic>{};

  UserStatsProvider() {
    fetchUserInfo();
  }

  UserInfo get userInfo => _userInfo;
  bool get isLoading => _isLoading;

  int get energy => _userInfo.energy;
  int get bank => _userInfo.bank;
  double get level => _userInfo.level;
  int get reputation => _userInfo.reputation;
  int get maxEnergy => _userInfo.maxEnergy;

  void fetchUserInfo() async {
     _isLoading = true;
     notifyListeners();

     try {
      var newUserInfo = await UserInfoManager.fetchUserInfo();
      if (_isDifferentFromCache(newUserInfo.toJson())) {
        _userInfo = newUserInfo;
        _cacheData(newUserInfo);
      }
      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _isLoading = false;
      notifyListeners();
    }
  }

  void _cacheData(UserInfo data) {
    _cache['userInfo'] = data.toJson();
  }

  bool _isDifferentFromCache(Map<String, dynamic> newData) {
    final cachedData = _cache['userInfo'] as Map<String, dynamic>?;
    if (cachedData == null) return true;

    return !const DeepCollectionEquality().equals(cachedData, newData);
  }
}
