import 'package:flutter/material.dart';
import '../common_imports.dart';
import '../api_calls/user_info_api.dart';
import '../models/user_model.dart';


class UserProfileScreen extends StatefulWidget {
  const UserProfileScreen({super.key});

  @override
  _UserProfileScreenState createState() => _UserProfileScreenState();
}

class _UserProfileScreenState extends State<UserProfileScreen> {
  final GlobalKey<ScaffoldState> _scaffoldKey = GlobalKey<ScaffoldState>();
  late Future<UserInfo> _userInfoFuture;

  @override
  void initState() {
    super.initState();
    _userInfoFuture = UserInfoManager.fetchUserInfo();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      key: _scaffoldKey,
      appBar: commonAppBar('User Profile', _scaffoldKey, context),
      drawer: commonDrawer(context, 'UserProfileScreen'),
      body: FutureBuilder<UserInfo>(
        future: _userInfoFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error.toString()}'));
          }

          UserInfo userInfo = snapshot.data!;
          return ListView(
            padding: const EdgeInsets.all(16),
            children: [
              _buildProfileHeader(userInfo),
              const SizedBox(height: 20),
              _buildStatCard('Energy', userInfo.energy.toString(), Icons.flash_on),
              _buildStatCard('Bank', '\$${userInfo.bank}', Icons.account_balance_wallet),
              _buildStatCard('Level', userInfo.level.toString(), Icons.trending_up),
              _buildStatCard('Reputation', userInfo.reputation.toString(), Icons.star),
              _buildDetailedStatSection(userInfo),
              if (userInfo.currentJob != null)
                _buildJobInfo(userInfo.currentJob!),
            ],
          );
        },
      ),
    );
  }

  Widget _buildProfileHeader(UserInfo userInfo) {
    return Column(
      children: [
        const CircleAvatar(
          radius: 50,
          // backgroundImage: AssetImage('assets/profile_picture.png'), // Placeholder image
        ),
        const SizedBox(height: 8),
        Text(
          userInfo.username,
          style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: UIColors.primaryTextColor),
        ),
      ],
    );
  }

  Widget _buildStatCard(String title, String value, IconData icon) {
    return Card(
      color: UIColors.secondaryBackgroundColor,
      child: ListTile(
        leading: Icon(icon, color: UIColors.primaryTextColor),
        title: Text(title, style: const TextStyle(color: UIColors.primaryTextColor)),
        trailing: Text(value, style: const TextStyle(color: UIColors.primaryTextColor, fontWeight: FontWeight.bold)),
      ),
    );
  }

  Widget _buildDetailedStatSection(UserInfo userInfo) {
    return ExpansionTile(
      title: const Text('Detailed Stats', style: TextStyle(color: UIColors.primaryTextColor)),
      children: [
        _buildStatLine('Max Energy', userInfo.maxEnergy.toString()),
        _buildStatLine('Health', userInfo.health.toString()),
        _buildStatLine('Strength', userInfo.strength.toStringAsFixed(1)),
        _buildStatLine('Evasiveness', userInfo.evasiveness.toStringAsFixed(1)),
        _buildStatLine('Knowledge', userInfo.knowledge.toStringAsFixed(1)),
        _buildStatLine('Luck', userInfo.luck.toStringAsFixed(1)),
        _buildStatLine('Damage', userInfo.damage.toString()),
      ],
    );
  }

  Widget _buildStatLine(String statName, String value) {
    return ListTile(
      title: Text(statName, style: const TextStyle(color: UIColors.secondaryTextColor)),
      trailing: Text(value, style: const TextStyle(color: UIColors.primaryTextColor)),
    );
  }

  Widget _buildJobInfo(String job) {
    return ListTile(
      title: const Text('Current Job', style: TextStyle(color: UIColors.primaryTextColor)),
      subtitle: Text(job, style: const TextStyle(color: UIColors.secondaryTextColor)),
    );
  }
}