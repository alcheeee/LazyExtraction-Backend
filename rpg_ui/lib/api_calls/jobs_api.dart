import 'package:http/http.dart' as http;
import 'dart:convert';
import '../config.dart';
import '../models/job_model.dart';


class JobManager {

  static Future<List<Job>> fetchAllJobs() async {
    var response = await http.post(Uri.parse('${APIUrl.apiURL}/game/get-all-jobs'),
      headers: {
        'Accept': 'application/json',
        'Authorization': 'Bearer ${SessionManager.accessToken}',
      },
    );
    if (response.statusCode == 200) {
      List<dynamic> jsonData = jsonDecode(response.body);
      return jsonData.map((jobJson) => Job.fromJson(jobJson)).toList();
    } else {
      throw Exception('Failed to load jobs');
    }
  }

  static Future<String> applyToJob(String jobName) async {
    var response = await http.post(Uri.parse('${APIUrl.apiURL}/game/apply-to-job'),
      headers: {
        'Accept': 'application/json',
        'Authorization': 'Bearer ${SessionManager.accessToken}',
        'Content-Type': 'application/json',
      },
      body: jsonEncode({'job_name': jobName}),
    );
    if (response.statusCode == 200) {
      return 'Application successful';
    } else {
      Map<String, dynamic> responseBody = jsonDecode(response.body);
      return 'Failed to apply: ${responseBody['message']}';
    }
  }
}
