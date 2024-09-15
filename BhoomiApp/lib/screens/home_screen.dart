import 'package:flutter/material.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'account_screen.dart';

class HomeScreen extends StatefulWidget {
  final String name;
  final String email;
  final String phoneNumber;
  final String state;

  HomeScreen({
    required this.name,
    required this.email,
    required this.phoneNumber,
    required this.state,
  });

  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int _selectedIndex = 0;

  void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index;
    });

    switch (index) {
      case 0:
        Navigator.pushReplacementNamed(context, '/home');
        break;
      case 1:
        Navigator.pushReplacementNamed(context, '/chatbot');
        break;
      case 2:
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (context) => AccountScreen(
              name: widget.name,
              email: widget.email,
              phoneNumber: widget.phoneNumber,
              state: widget.state,
            ),
          ),
        );
        break;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.teal[100],
        elevation: 0,
        leading: Builder(
          builder: (context) => IconButton(
            icon: const Icon(Icons.menu, color: Colors.black),
            onPressed: () {
              Scaffold.of(context).openDrawer();
            },
          ),
        ),
        title: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Image.asset('assets/images/logo3.png', height: 40),
            const SizedBox(width: 10),
            const Text(
              'BHOOMI',
              style: TextStyle(color: Colors.black, fontSize: 24, fontWeight: FontWeight.bold),
            ),
          ],
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.notifications, color: Colors.black),
            onPressed: () {
            },
          ),
          const SizedBox(width: 10),
        ],
      ),
      drawer: Drawer(
        child: Column(
          children: [
            Container(
              color: Colors.teal[100],
              child: Column(
                children: [
                  UserAccountsDrawerHeader(
                    accountName: Text(widget.name, style: const TextStyle(color: Colors.black)),
                    accountEmail: Text(widget.email, style: const TextStyle(color: Colors.black)),
                    currentAccountPicture: CircleAvatar(
                      backgroundColor: Colors.white,
                      child: Text(
                        widget.name[0],
                        style: const TextStyle(fontSize: 40.0, color: Colors.black),
                      ),
                    ),
                    decoration: BoxDecoration(
                      color: Colors.teal[300], 
                    ),
                  ),
                ],
              ),
            ),
            Expanded(
              child: Container(
                color: Colors.white,
                child: ListView(
                  padding: EdgeInsets.zero,
                  children: <Widget>[
                    _buildDrawerItem(FontAwesomeIcons.solidFolder, 'Categories'),
                    _buildDrawerItem(FontAwesomeIcons.save, 'Saved Products'),
                    _buildDrawerItem(FontAwesomeIcons.productHunt, 'Your Products'),
                    _buildDrawerItem(FontAwesomeIcons.podcast, 'Government Policies'),
                    _buildDrawerItem(FontAwesomeIcons.chartLine, 'Market Rate'),
                    _buildDrawerItem(FontAwesomeIcons.bullhorn, 'Promote'),
                    _buildDrawerItem(FontAwesomeIcons.whatsapp, 'WhatsApp'),
                    _buildDrawerItem(FontAwesomeIcons.youtube, 'Learn from YouTube'),
                    _buildDrawerItem(FontAwesomeIcons.seedling, 'Crop Health'),
                    _buildDrawerItem(FontAwesomeIcons.sun, 'Weather'),
                    _buildDrawerItem(FontAwesomeIcons.phone, 'Contact Us'),
                    _buildDrawerItem(FontAwesomeIcons.fileContract, 'T&C'),
                    _buildDrawerItem(FontAwesomeIcons.infoCircle, 'Know About Us'),
                    _buildDrawerItem(FontAwesomeIcons.signOutAlt, 'Logout'),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(
              decoration: InputDecoration(
                prefixIcon: const Icon(Icons.search),
                hintText: 'Search any categories',
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(30),
                  borderSide: BorderSide.none,
                ),
                filled: true,
                fillColor: Colors.teal[100],
              ),
            ),
            const SizedBox(height: 20),
            Expanded(
              child: ListView(
                children: [
                  _buildCategoryCard('Disease Detection', 'assets/images/crop_disease_icon.png'),
                  _buildCategoryCard('Community', 'assets/images/community_icon.png'),
                  _buildCategoryCard('Soil Analysis', 'assets/images/soil_analysis_icon.png'),
                  _buildCategoryCard('Mandis and Transport', 'assets/images/mandis_transport_icon.png'),
                ],
              ),
            ),
          ],
        ),
      ),
      bottomNavigationBar: Container(
        decoration: BoxDecoration(
          color: Colors.teal[100],
          borderRadius: const BorderRadius.only(
            topLeft: Radius.circular(30.0),
            topRight: Radius.circular(30.0),
          ),
          boxShadow: [
            BoxShadow(
              color: Colors.grey.withOpacity(0.5),
              spreadRadius: 1,
              blurRadius: 10,
              offset: const Offset(0, 2),
            ),
          ],
        ),
        child: BottomNavigationBar(
          currentIndex: _selectedIndex,
          onTap: _onItemTapped,
          backgroundColor: Colors.transparent,
          elevation: 0,
          iconSize: 36.0,
          items: [
            BottomNavigationBarItem(
              icon: Icon(Icons.home, color: _selectedIndex == 0 ? Colors.teal : Colors.black),
              label: 'Home',
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.chat, color: _selectedIndex == 1 ? Colors.teal : Colors.black),
              label: 'Chatbot',
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.account_circle, color: _selectedIndex == 2 ? Colors.teal : Colors.black),
              label: 'Account',
            ),
          ],
          selectedItemColor: Colors.teal,
          unselectedItemColor: Colors.black,
          showSelectedLabels: true,
          type: BottomNavigationBarType.fixed,
        ),
      ),
    );
  }

  Widget _buildDrawerItem(IconData icon, String title) {
    return ListTile(
      leading: Icon(icon, color: Colors.black), 
      title: Text(
        title,
        style: const TextStyle(color: Colors.black),
      ),
      onTap: () {
      },
    );
  }

  Widget _buildCategoryCard(String title, String iconPath) {
    return Card(
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(10.0),
      ),
      color: Colors.teal[300],
      child: ListTile(
        leading: Image.asset(iconPath, width: 50),
        title: Text(
          title,
          style: const TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold),
        ),
        onTap: () {
          if (title == 'Disease Detection') {
            Navigator.pushNamed(context, '/crop-disease');
          } else if (title == 'Soil Analysis') {
            Navigator.pushNamed(context, '/soil-analysis');
          } else if (title == 'Mandis and Transport') {
            Navigator.pushNamed(context, '/mandis-transport');
          }
        },
      ),
    );
  }
}
