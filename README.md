# Friend Connection System

A powerful social network analysis tool that finds optimal connection paths between people using advanced graph algorithms. The system combines Union-Find data structures with Bidirectional Dijkstra algorithms to efficiently compute shortest paths in social networks, complete with an interactive web visualization.

## ✨ Features

- **Shortest Path Finding**: Discover the optimal connection path between any two people in your network (using bidirectional Dijkstra)
- **Connection Adjustmenst Available**: Add new friendships with a customizable connection score
with 1 being the strongest connection and up to 10. 
- **Path Limitations**: Limit the maximum path score to focus on close connections and reduce system loading.
- **Component Detection**: Automatically identifies separate social clusters (using Union-Find)
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
├── requirements.txt     # required Python packages 
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

### Setting Path Limitations

- Use the "Path Score Limit" field to set a maximum acceptable path score
- Set to 0 for unlimited paths
- Useful for finding only close connections (e.g., limit of 5 finds very close friend chains)

### Adding Connections

1. Enter two names in the "Add Connection" section
2. Set a connection score (1 = closest friends, up to 10)
3. Click "Add Connection"
4. The graph will automatically update with the new connection

### Interactive Graph Features

- **Drag nodes** to rearrange the graph layout
- **Click nodes** to auto-fill name fields
- **Zoom** in/out using mouse wheel
- **Toggle edge labels** to show/hide connection scores

## 🔧 Technical Details

### Algorithms

1. **Union-Find (Disjoint Set Union)**
   - Optimized with union by size
   - Tracks connected components efficiently
   - Path compression for O(α(n)) operations
   - Accept any immutable and hashable type

2. **Bidirectional Dijkstra**
   - Searches from both start and target simultaneously
   - Reduces search space compared to standard Dijkstra
   - Supports weighted graphs with customizable limitations
   - Accept any immutable and hashable type

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/graph_data` | GET | Returns complete graph structure |
| `/api/find_path` | POST | Finds shortest path between two people |
| `/api/add_relation` | POST | Adds a new friendship connection |
| `/api/check_relation` | POST | Checks if two people are connected |
| `/api/set_limitation` | POST | Sets maximum path score limit |
| `/api/get_limitation` | GET | Gets current path limitation |
| `/api/components` | GET | Returns all connected components |

## 🎨 Features Breakdown

### Backend (Algorithm.py & Backend.py)
- **Efficient Algorithms**: O(E log V) path finding complexity. When no valid connection exists, it takes O(1) because we use Union Find before running Dijkstra.
- **Scalable Design**: Handles large networks efficiently
- **Modular Architecture**: Separated concerns for easy maintenance

### Frontend (Embedded in flask_app.py)
- **Technology**: HTML5, CSS3, JavaScript, D3.js v7
- **Responsive Design**: Adapts to different screen sizes
- **Real-time Updates**: Graph refreshes automatically when data changes
- **Visual Feedback**: Color-coded paths and interactive elements


## 📝 Input Data Format (friendship_data.txt)

If you want to pre-load friendship data, create a `friendship_data.txt` file:
```
Alice, Bob, 2
Bob, Charlie, 3
Charlie, David, 4
- (needs a empty line at the end)
```
Each line represents: `Person1, Person2, ConnectionScore`
Use `-` on a line to separate data sections or mark the end.

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