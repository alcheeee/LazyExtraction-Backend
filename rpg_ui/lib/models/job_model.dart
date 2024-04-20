import 'dart:convert';

class Job {
  final String jobName;
  final String jobType;
  final int income;
  final int energyRequired;
  final String description;
  final Map<String, dynamic> requiredStats;
  final Map<String, dynamic> statChanges;

  Job({
    required this.jobName,
    required this.jobType,
    required this.income,
    required this.energyRequired,
    required this.description,
    required this.requiredStats,
    required this.statChanges,
  });

  factory Job.fromJson(Map<String, dynamic> json) {
    return Job(
      jobName: json['job_name'],
      jobType: json['job_type'],
      income: json['income'],
      energyRequired: json['energy_required'],
      description: json['description'],
      requiredStats: jsonDecode(json['required_stats']),
      statChanges: jsonDecode(json['stat_changes']),
    );
  }
}
