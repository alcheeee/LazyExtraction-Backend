class UserStats {
  final int id;
  final double level;
  final double reputation;
  final int maxEnergy;
  final double luck;
  final double knowledge;
  final double maxWeight;
  final double agility;
  final int health;
  final int damage;
  final double strength;
  final int headProtection;
  final int chestProtection;
  final int stomachProtection;
  final int armProtection;

  UserStats({
    required this.id,
    required this.level,
    required this.reputation,
    required this.maxEnergy,
    required this.luck,
    required this.knowledge,
    required this.maxWeight,
    required this.agility,
    required this.health,
    required this.damage,
    required this.strength,
    required this.headProtection,
    required this.chestProtection,
    required this.stomachProtection,
    required this.armProtection,
  });

  factory UserStats.fromJson(Map<String, dynamic> json) {
    return UserStats(
      id: json['id'],
      level: json['level'],
      reputation: json['reputation'],
      maxEnergy: json['max_energy'],
      luck: json['luck'],
      knowledge: json['knowledge'],
      maxWeight: json['max_weight'],
      agility: json['agility'],
      health: json['health'],
      damage: json['damage'],
      strength: json['strength'],
      headProtection: json['head_protection'],
      chestProtection: json['chest_protection'],
      stomachProtection: json['stomach_protection'],
      armProtection: json['arm_protection'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'level': level,
      'reputation': reputation,
      'max_energy': maxEnergy,
      'luck': luck,
      'knowledge': knowledge,
      'max_weight': maxWeight,
      'agility': agility,
      'health': health,
      'damage': damage,
      'strength': strength,
      'head_protection': headProtection,
      'chest_protection': chestProtection,
      'stomach_protection': stomachProtection,
      'arm_protection': armProtection,
    };
  }
}

final exampleUserStats = UserStats(
  id: 1,
  level: 5.0,
  reputation: 4.5,
  maxEnergy: 120,
  luck: 3.5,
  knowledge: 4.0,
  maxWeight: 150.0,
  agility: 3.0,
  health: 100,
  damage: 20,
  strength: 2.5,
  headProtection: 10,
  chestProtection: 15,
  stomachProtection: 12,
  armProtection: 8,
);
