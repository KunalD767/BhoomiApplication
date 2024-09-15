import 'package:flutter/material.dart';
import 'package:bhoomi/helpers/location_helper.dart';
import 'package:bhoomi/helpers/api_helper.dart';
import 'package:geolocator/geolocator.dart';

class TransportListScreen extends StatefulWidget {
  @override
  _TransportListScreenState createState() => _TransportListScreenState();
}

class _TransportListScreenState extends State<TransportListScreen> {
  late Future<List<dynamic>> _nearbyTransport;

  @override
  void initState() {
    super.initState();
    _fetchNearbyTransport();
  }

  Future<void> _fetchNearbyTransport() async {
    try {
      Position position = await LocationHelper.getCurrentLocation();
      setState(() {
        _nearbyTransport = ApiHelper.fetchNearbyData(position.latitude, position.longitude, 'transport');
      });
    } catch (e) {
      print(e);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Nearby Transport Services'),
        backgroundColor: Colors.teal[100],
      ),
      body: FutureBuilder<List<dynamic>>(
        future: _nearbyTransport,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return Center(child: Text('No transport services found nearby.'));
          } else {
            return ListView.builder(
              itemCount: snapshot.data!.length,
              itemBuilder: (context, index) {
                final transport = snapshot.data![index];
                return ListTile(
                  title: Text(transport['name']),
                  subtitle: Text('Phone: ${transport['phone']}'),
                  onTap: () {
                    Navigator.pushNamed(context, '/details', arguments: transport);
                  },
                );
              },
            );
          }
        },
      ),
    );
  }
}
