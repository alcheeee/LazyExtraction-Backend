class UserInfo {
  final String username;
  final int bank;
  final int energy;
  final double level;
  final int reputation;
  final int maxEnergy;
  final double evasiveness;
  final int health;
  final double strength;
  final double knowledge;
  final double luck;
  final int damage;
  final String? education;
  final String? currentJob;

  UserInfo({
    this.username = '',
    this.bank = 0,
    this.energy = 0,
    this.level = 0.0,
    this.reputation = 0,
    this.maxEnergy = 0,
    this.evasiveness = 0.0,
    this.health = 0,
    this.strength = 0.0,
    this.knowledge = 0.0,
    this.luck = 0.0,
    this.damage = 0,
    this.education,
    this.currentJob,
  });

  factory UserInfo.dummy() {
    return UserInfo(
      username: "Guest",
      bank: 0,
      energy: 0,
      level: 0.0,
      reputation: 0,
      maxEnergy: 0,
      evasiveness: 0.0,
      health: 0,
      strength: 0.0,
      knowledge: 0.0,
      luck: 0.0,
      damage: 0,
      education: null,
      currentJob: null,
    );
  }

  factory UserInfo.fromJson(Map<String, dynamic> json) {
    return UserInfo(
      username: json['username'] as String? ?? '',
      bank: json['bank'] as int? ?? 0,
      energy: json['energy'] as int? ?? 0,
      level: (json['level'] as num? ?? 0).toDouble(),
      reputation: json['reputation'] as int? ?? 0,
      maxEnergy: json['max_energy'] as int? ?? 0,
      evasiveness: (json['evasiveness'] as num? ?? 0.0).toDouble(),
      health: json['health'] as int? ?? 0,
      strength: (json['strength'] as num? ?? 0.0).toDouble(),
      knowledge: (json['knowledge'] as num? ?? 0.0).toDouble(),
      luck: (json['luck'] as num? ?? 0.0).toDouble(),
      damage: json['damage'] as int? ?? 0,
      education: json['education'],
      currentJob: json['current_job'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'username': username,
      'bank': bank,
      'energy': energy,
      'level': level,
      'reputation': reputation,
      'max_energy': maxEnergy,
      'evasiveness': evasiveness,
      'health': health,
      'strength': strength,
      'knowledge': knowledge,
      'luck': luck,
      'damage': damage,
      'education': education,
      'current_job': currentJob,
    };
  }
}
