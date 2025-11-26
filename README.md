# Friend Connection System

A powerful social network analysis tool that finds optimal connection paths between people using advanced graph algorithms. The system combines Union-Find data structures with Bidirectional Dijkstra algorithms to efficiently compute shortest paths in social networks, complete with an interactive web visualization.

## ✨ Features

- **Shortest Path Finding**: Discover the optimal connection path between any two people in your network (using bidirectional Dijkstra)
- **Profile-Based Search**: Find people whose profiles match specific keywords, with the shortest path from your starting point
- **Connection Adjustments Available**: Add new friendships with a customizable connection score with 1 being the strongest connection and up to 10
- **Path Limitations**: Limit the maximum path score to focus on close connections and reduce system loading
- **Component Detection**: Automatically identifies separate social clusters (using Union-Find)
- **Persona Profiles**: View detailed profile information for each person including personality traits, goals, and more
- **Click-to-Fill Interface**: Click on nodes in the graph to auto-fill names in input fields
- **Interactive Graph Visualization**: Real-time visualization with drag-and-drop capabilities
- **Network Statistics**: View real-time statistics about network size and connectivity

## 📋 Prerequisites

- Python 3.7+
- pip (Python package installer)

## 🚀 Installation

1. **Clone the repository** (or download the files):
```bash
git clone https://github.com/zacheen/Friend_Connection_System.git
cd friend-connection-system
```

2. **Install required Python packages**:
```bash
pip install -r requirements.txt
```

## 📁 Project Structure

```
friend-connection-system/
│
├── Algorithm.py         # Core graph algorithms (Union-Find & Bidirectional Dijkstra)
├── Backend.py           # Backend logic and data management
├── flask_app.py         # Flask web server and API endpoints
├── persona_data.py      # Persona profile data and utilities
├── requirements.txt     # Required Python packages 
├── friendship_data.json # Friendship data in JSON format
├── friendship_data_long_dis.txt # Sample dataset used for experimentation
└── README.md
```

## 🏃‍♂️ Running the Application

1. **Start the Flask server**:
```bash
python flask_app.py
```

2. The server will display:
```
==================================================
Friend Connection System Server
==================================================
Server is starting at: http://localhost:5000
Press Ctrl+C to stop the server
==================================================
```

3. **Open your browser** and navigate to:
```
http://localhost:5000
```

## 💻 Usage Guide

### Finding Shortest Path

1. Enter two names in the "Find Shortest Path" section
2. Click "Find Path"
3. The system will:
   - Display the optimal path with total score
   - Highlight the path in red on the graph
   - Show each person in the connection chain

### Finding People by Profile Keywords

1. Enter a starting person's name in the "Find Target Profile" section
2. Enter a keyword to search for in people's profiles (e.g., "engineer", "music", "travel")
3. Click "Find Target"
4. The system will:
   - Search through connected profiles for the keyword match
   - Display the shortest path from your starting person to someone with that characteristic
   - Highlight the discovered path on the graph

This feature is useful for finding friends-of-friends who share specific interests or professions.

### Setting Path Limitations

- Use the "Path Score Limit" field to set a maximum acceptable path score
- Set to 0 for unlimited paths
- Useful for finding only close connections (e.g., limit of 5 finds very close friend chains)

### Adding Connections

1. Enter two names in the "Add Connection" section
2. Set a connection score (1 = closest friends, up to 10)
3. Click "Add Connection"
4. The graph will automatically update with the new connection

### Viewing Persona Profiles

- **Quick Preview**: Click on any node to see a profile preview in the sidebar
- **Hover Tooltip**: Hover over nodes to see a brief tooltip with key profile info
- **Full Profile Page**: Double-click a node or use the profile button to open a detailed profile page

### Interactive Graph Features

- **Drag nodes** to rearrange the graph layout
- **Click nodes** to auto-fill name fields and preview profiles
- **Double-click nodes** to open full profile pages
- **Zoom** in/out using mouse wheel
- **Toggle edge labels** to show/hide connection scores

## 🔧 Technical Details

### Algorithms

1. **Union-Find (Disjoint Set Union)**
   - Optimized with union by size
   - Tracks connected components efficiently
   - Path compression for O(α(n)) operations
   - Accepts any immutable and hashable type

2. **Bidirectional Dijkstra**
   - Searches from both start and target simultaneously
   - Reduces search space compared to standard Dijkstra
   - Supports weighted graphs with customizable limitations
   - Accepts any immutable and hashable type

3. **Profile-Based Search**
   - Uses modified Dijkstra to find nearest person matching a keyword
   - Searches through persona summaries and attributes
   - Returns shortest path to the matching profile

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/graph_data` | GET | Returns complete graph structure |
| `/api/find_path` | POST | Finds shortest path between two people |
| `/api/find_target` | POST | Finds nearest person matching a profile keyword |
| `/api/add_relation` | POST | Adds a new friendship connection |
| `/api/check_relation` | POST | Checks if two people are connected |
| `/api/set_limitation` | POST | Sets maximum path score limit |
| `/api/get_limitation` | GET | Gets current path limitation |
| `/api/components` | GET | Returns all connected components |
| `/api/personas` | GET | Returns all persona profiles |
| `/api/persona/<id>` | GET | Returns a specific persona profile |
| `/profile/<id>` | GET | Renders full profile page for a person |

## 🎨 Features Breakdown

### Backend (Algorithm.py & Backend.py)
- **Efficient Algorithms**: O(E log V) path finding complexity. When no valid connection exists, it takes O(1) because we use Union Find before running Dijkstra.
- **Scalable Design**: Handles large networks efficiently
- **Modular Architecture**: Separated concerns for easy maintenance
- **Persona Integration**: Profile data integrated with graph search

### Frontend (Embedded in flask_app.py)
- **Technology**: HTML5, CSS3, JavaScript, D3.js v7
- **Responsive Design**: Adapts to different screen sizes
- **Real-time Updates**: Graph refreshes automatically when data changes
- **Visual Feedback**: Color-coded paths and interactive elements
- **Profile Previews**: Hover tooltips and sidebar previews for persona data


## 📝 Input Data Format (friendship_data.txt)

If you want to pre-load friendship data, create a `friendship_data.txt` file:
```
Alice, Bob, 2
Bob, Charlie, 3
Charlie, David, 4
- (needs an empty line at the end)
```
Each line represents: `Person1, Person2, ConnectionScore`
Use `-` on a line to separate data sections or mark the end.

Alternatively, use JSON format (`friendship_data.json`):
```json
{
  "relations": [
    ["Alice", "Bob", 2],
    ["Bob", "Charlie", 3],
    ["Charlie", "David", 4]
  ]
}
```

## 🐛 Troubleshooting

**Issue**: "Port 5000 is already in use"
- **Solution**: Change the port in `flask_app.py` last line: `app.run(debug=True, port=5001)`

**Issue**: Graph doesn't update after adding connections
- **Solution**: Click "Refresh Graph" button or reload the page

**Issue**: Can't find path between two people
- **Possible causes**:
  - They're in different network components (not connected at all)
  - The path exceeds the set limitation
  - Names are misspelled (case-sensitive)
  
<!--
## Roadmap
- [x] Adapt the algorithm to fit our needs
- [x] Optimize algorithm
- [x] Add a path limit to improve performance when working with larger datasets
- [x] Build and connect to front end

<!--
## 🎯 Future Enhancements
- [ ] Adding custom bias settings for each additional leve (The cost for an extra connection)
- [ ] Multiple shortest paths display
- [ ] Batch import from CSV files
-->