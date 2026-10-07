import 'package:flutter/material.dart';

void main() {
  runApp(const TradePilotApp());
}

class TradePilotApp extends StatelessWidget {
  const TradePilotApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'TradePilot Deriv',
      theme: ThemeData(
        useMaterial3: true,
        brightness: Brightness.dark,
        scaffoldBackgroundColor: const Color(0xFF0E1117),
        appBarTheme: const AppBarTheme(
          backgroundColor: Color(0xFF121A2A),
        ),
      ),
      home: const DashboardScreen(),
    );
  }
}

class DashboardScreen extends StatelessWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('TradePilot Deriv'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _metricCard('Balance', '\$12,450.00'),
            _metricCard('Open Positions', '3'),
            _metricCard('Daily P&L', '+\$340.00'),
            const SizedBox(height: 16),
            const Text(
              '15m LuxAlgo Pivot Strategy',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 12),
            Row(
              children: [
                ElevatedButton(
                  onPressed: () {},
                  child: const Text('Start'),
                ),
                const SizedBox(width: 12),
                OutlinedButton(
                  onPressed: () {},
                  child: const Text('Pause'),
                ),
              ],
            ),
            const SizedBox(height: 22),
            _symbolTile('frxEURUSD', 'BUY', 'Confidence 82%'),
            _symbolTile('R_100', 'SELL', 'Confidence 79%'),
          ],
        ),
      ),
    );
  }

  Widget _metricCard(String title, String value) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(16),
      margin: const EdgeInsets.only(bottom: 12),
      decoration: BoxDecoration(
        color: const Color(0xFF1B2431),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(title, style: const TextStyle(color: Colors.grey)),
          const SizedBox(height: 8),
          Text(value, style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
        ],
      ),
    );
  }

  Widget _symbolTile(String symbol, String action, String label) {
    final color = action == 'BUY' ? Colors.green : Colors.red;
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(14),
      margin: const EdgeInsets.only(bottom: 12),
      decoration: BoxDecoration(
        color: const Color(0xFF111827),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(symbol, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          Text(action, style: TextStyle(color: color, fontWeight: FontWeight.bold)),
          Text(label, style: const TextStyle(color: Colors.grey)),
        ],
      ),
    );
  }
}
