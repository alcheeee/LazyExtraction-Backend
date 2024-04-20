import '../common_imports.dart';
import '../api_calls/jobs_api.dart';
import '../models/job_model.dart';
import 'package:flutter/material.dart';

class JobsScreen extends StatefulWidget {
  const JobsScreen({super.key});

  @override
  _JobsScreenState createState() => _JobsScreenState();
}

class _JobsScreenState extends State<JobsScreen> {
  final GlobalKey<ScaffoldState> _scaffoldKey = GlobalKey<ScaffoldState>();
  late Future<List<Job>> _jobsFuture;
  String? currentJob;

  @override
  void initState() {
    super.initState();
    _jobsFuture = JobManager.fetchAllJobs();
    currentJob = "Store Bagger"; // Placeholder, need to add route
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      key: _scaffoldKey,
      appBar: commonAppBar('Jobs', _scaffoldKey, context),
      drawer: commonDrawer(context, 'JobsScreen'),
      body: Column(
        children: [
          Container(
            padding: const EdgeInsets.all(10),
            margin: const EdgeInsets.all(10),
            decoration: BoxDecoration(
              color: UIColors.secondaryBackgroundColor,
              borderRadius: BorderRadius.circular(10),
              border: Border.all(color: UIColors.primaryOutlineColor),
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withOpacity(0.1),
                  spreadRadius: 1,
                  blurRadius: 2,
                  offset: const Offset(0, 2),
                ),
              ],
            ),
            child: Center(
              child: Text(
                currentJob != null ? "Currently Employed as: $currentJob" : "You're unemployed",
                style: const TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: UIColors.primaryTextColor,
                ),
              ),
            ),
          ),
          Expanded(
            child: FutureBuilder<List<Job>>(
              future: _jobsFuture,
              builder: (context, snapshot) {
                if (snapshot.connectionState == ConnectionState.waiting) {
                  return const Center(child: CircularProgressIndicator());
                } else if (snapshot.hasError) {
                  return Center(child: Text('Error: ${snapshot.error}'));
                }
                return ListView.builder(
                  itemCount: snapshot.data?.length ?? 0,
                  itemBuilder: (context, index) {
                    Job job = snapshot.data![index];
                    return Card(
                      color: UIColors.secondaryBackgroundColor,
                      child: ListTile(
                        onTap: () => _showJobDetails(context, job),
                        title: Text(job.jobName, style: const TextStyle(color: UIColors.primaryTextColor)),
                        subtitle: Text('\$${job.income} per task - Tap for more', style: const TextStyle(color: UIColors.secondaryTextColor)),
                        isThreeLine: true,
                        leading: const Icon(Icons.work, color: UIColors.primaryTextColor),
                        trailing: Text(job.jobType, style: const TextStyle(color: UIColors.primaryTextColor)),
                      ),
                    );
                  },
                );
              },
            ),
          ),
        ],
      ),
    );
  }

  void _showJobDetails(BuildContext context, Job job) {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          backgroundColor: UIColors.primaryBackgroundColor,
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(4)),
          title: Text(
              job.jobName,
              style: const TextStyle(
                color: UIColors.primaryTextColor,
                fontWeight: FontWeight.bold,
                fontSize: 20
              ),
          ),
          content: SingleChildScrollView(
            child: ListBody(
              children: [
                Text(job.description,
                    style: const TextStyle(
                      color: UIColors.primaryTextColor,
                      fontWeight: FontWeight.w400,
                      fontSize: 16
                    )
                ),
                Text('Income: \$${job.income}',
                    style: const TextStyle(color: Colors.green)
                ),
                Text('Energy cost: ${job.energyRequired}',
                    style: const TextStyle(color: Colors.yellow)
                ),
                _buildStatDetails('Required Stats', job.requiredStats),
                _buildStatDetails('Stat Changes', job.statChanges),
              ],
            ),
          ),
          actions: <Widget>[
            AppTheme.customButton(
              label: 'Apply',
              onPressed: () async {
                Navigator.of(context).pop();
                String resultMessage = await JobManager.applyToJob(job.jobName);
                ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(resultMessage)));
              },
              backgroundColor: UIColors.secondaryBackgroundColor,
              textStyle: const TextStyle(color: UIColors.primaryTextColor),
            ),
            AppTheme.customButton(
              label: 'Close',
              onPressed: () => Navigator.of(context).pop(),
              backgroundColor: UIColors.secondaryBackgroundColor,
              textStyle: const TextStyle(color: UIColors.primaryTextColor),
            ),
          ],
        );
      },
    );
  }

  Widget _buildStatDetails(String title, Map<String, dynamic> stats) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.only(top: 10.0),
          child:
          Text(title,
              style: const TextStyle(
                  color: UIColors.primaryTextColor,
                  fontWeight: FontWeight.bold
              )
          ),
        ),
        ...stats.entries.map((entry) => Text(
            '${entry.key.capitalize()}: ${entry.value}',
            style: const TextStyle(
                color: UIColors.secondaryTextColor,
                fontWeight: FontWeight.w400
            )
        )),
      ],
    );
  }
}

extension on String {
  String capitalize() {
    if (isEmpty) return this;
    return "${this[0].toUpperCase()}${substring(1).toLowerCase()}";
  }
}
