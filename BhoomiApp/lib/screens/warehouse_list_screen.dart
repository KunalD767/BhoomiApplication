import 'package:flutter/material.dart';
import 'package:bhoomi/helpers/combined_service.dart';

class WarehouseListScreen extends StatefulWidget {
  @override
  _WarehouseListScreenState createState() => _WarehouseListScreenState();
}

class _WarehouseListScreenState extends State<WarehouseListScreen> {
  @override
  void initState() {
    super.initState();
    // Fetch warehouses and generate insights
    CombinedService.fetchAndGenerateInsights(31.326, 75.576, 'warehouse'); // Example lat/lon for warehouses
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Nearby Warehouses'),
        backgroundColor: Colors.teal[100],
      ),
      body: Center(
        child: Text('Fetching nearby warehouses and generating insights...'),
      ),
    );
  }
}
