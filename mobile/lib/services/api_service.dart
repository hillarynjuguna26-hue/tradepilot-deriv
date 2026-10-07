import 'dart:convert';
import 'package:http/http.dart' as http;

class MarketSignal {
  final String symbol;
  final String action;
  final double confidence;
  final double? pivotLevel;

  MarketSignal({
    required this.symbol,
    required this.action,
    required this.confidence,
    this.pivotLevel,
  });

  factory MarketSignal.fromJson(Map<String, dynamic> json) {
    return MarketSignal(
      symbol: json['symbol'] ?? 'UNKNOWN',
      action: json['action'] ?? 'HOLD',
      confidence: (json['confidence'] ?? 0.0).toDouble(),
      pivotLevel: (json['levels'] != null && json['levels']['pivot'] != null)
          ? (json['levels']['pivot'] as num).toDouble()
          : null,
    );
  }
}

class ApiService {
  static const String baseUrl = 'http://10.0.2.2:8000/api';

  static Future<List<String>> fetchSymbols() async {
    final response = await http.get(Uri.parse('$baseUrl/symbols'));
    if (response.statusCode != 200) {
      throw Exception('Failed to load symbols');
    }

    final jsonBody = json.decode(response.body);
    return List<String>.from(jsonBody['symbols'] ?? []);
  }

  static Future<MarketSignal> scanDemo(String symbol) async {
    final response = await http.post(
      Uri.parse('$baseUrl/demo-scan'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'symbol': symbol}),
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to scan symbol');
    }

    final jsonBody = json.decode(response.body);
    return MarketSignal.fromJson(jsonBody);
  }
}
