import 'package:flutter/material.dart';
import 'package:tradepilot_deriv/services/api_service.dart';

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
        scaffoldBackgroundColor: const Color(0xFF0F172A),
        appBarTheme: const AppBarTheme(
          backgroundColor: Color(0xFF111827),
          foregroundColor: Colors.white,
        ),
      ),
      home: const DashboardScreen(),
    );
  }
}

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  List<String> symbols = [];
  String selectedSymbol = 'frxEURUSD';
  bool isLoading = true;
  String statusText = 'Ready';
  MarketSignal? latestSignal;

  @override
  void initState() {
    super.initState();
    _loadSymbols();
  }

  Future<void> _loadSymbols() async {
    try {
      final loadedSymbols = await ApiService.fetchSymbols();
      setState(() {
        symbols = loadedSymbols;
        selectedSymbol = symbols.isNotEmpty ? symbols.first : selectedSymbol;
        isLoading = false;
      });
    } catch (e) {
      setState(() {
        isLoading = false;
        statusText = 'API unavailable';
      });
    }
  }

  Future<void> _scanSymbol() async {
    setState(() {
      statusText = 'Scanning...';
      isLoading = true;
    });

    try {
      final signal = await ApiService.scanDemo(selectedSymbol);
      setState(() {
        latestSignal = signal;
        statusText = 'Signal received';
        isLoading = false;
      });
    } catch (e) {
      setState(() {
        statusText = 'Scan failed';
        isLoading = false;
      });
    }
  }

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
            _infoCard('Balance', '\$12,450.00'),
            _infoCard('Open Positions', '3'),
            _infoCard('Daily P&L', '+\$340.00'),
            const SizedBox(height: 18),
            const Text(
              '15m LuxAlgo Pivot Strategy',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 12),
            if (symbols.isNotEmpty)
              DropdownButtonFormField<String>(
                value: selectedSymbol,
                decoration: const InputDecoration(
                  filled: true,
                  fillColor: Color(0xFF111827),
                  border: OutlineInputBorder(),
                ),
                items: symbols
                    .map((symbol) => DropdownMenuItem(value: symbol, child: Text(symbol)))
                    .toList(),
                onChanged: (value) {
                  if (value != null) {
                    setState(() {
                      selectedSymbol = value;
                    });
                  }
                },
              ),
            const SizedBox(height: 14),
            Row(
              children: [
                ElevatedButton.icon(
                  onPressed: isLoading ? null : _scanSymbol,
                  icon: const Icon(Icons.search),
                  label: const Text('Scan'),
                ),
                const SizedBox(width: 12),
                OutlinedButton.icon(
                  onPressed: () {},
                  icon: const Icon(Icons.pause),
                  label: const Text('Pause'),
                ),
              ],
            ),
            const SizedBox(height: 18),
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: const Color(0xFF111827),
                borderRadius: BorderRadius.circular(12),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('Status', style: TextStyle(color: Colors.grey)),
                  const SizedBox(height: 8),
                  Text(statusText, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                  const SizedBox(height: 12),
                  if (latestSignal != null) ...[
                    Text('Symbol: ${latestSignal!.symbol}'),
                    Text('Action: ${latestSignal!.action}'),
                    Text('Confidence: ${(latestSignal!.confidence * 100).toStringAsFixed(0)}%'),
                    if (latestSignal!.pivotLevel != null)
                      Text('Pivot: ${latestSignal!.pivotLevel!.toStringAsFixed(5)}'),
                  ],
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _infoCard(String title, String value) {
    return Container(
      width: double.infinity,
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: const Color(0xFF111827),
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
}
