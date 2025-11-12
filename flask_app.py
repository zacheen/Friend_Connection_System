from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
from Backend import Backend
import os

app = Flask(__name__)
CORS(app)

# Initialize backend
# You can specify a data file path here, or leave it None for empty initialization
backend = Backend(path='friendship_data.txt' if os.path.exists('friendship_data.txt') else None)

# HTML template will be served from here
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Friend Connection System</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        h1 {
            text-align: center;
            color: white;
            margin-bottom: 30px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        
        .main-content {
            display: grid;
            grid-template-columns: 400px 1fr;
            gap: 20px;
            height: calc(100vh - 120px);
        }
        
        .controls {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow-y: auto;
        }
        
        .graph-container {
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            position: relative;
            overflow: hidden;
        }
        
        .section {
            margin-bottom: 25px;
            padding-bottom: 20px;
            border-bottom: 2px solid #f0f0f0;
        }
        
        .section:last-child {
            border-bottom: none;
        }
        
        h2 {
            color: #764ba2;
            margin-bottom: 15px;
            font-size: 1.3em;
        }
        
        .input-group {
            margin-bottom: 12px;
        }
        
        label {
            display: block;
            margin-bottom: 5px;
            color: #555;
            font-weight: 500;
        }
        
        input[type="text"],
        input[type="number"] {
            width: 100%;
            padding: 10px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
            transition: border-color 0.3s;
        }
        
        input[type="text"]:focus,
        input[type="number"]:focus {
            outline: none;
            border-color: #764ba2;
        }
        
        button {
            width: 100%;
            padding: 12px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(118, 75, 162, 0.4);
        }
        
        button:active {
            transform: translateY(0);
        }
        
        .result-box {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 15px;
            margin-top: 15px;
            border: 2px solid #e0e0e0;
        }
        
        .result-title {
            font-weight: 600;
            color: #333;
            margin-bottom: 8px;
        }
        
        .path-display {
            background: white;
            padding: 10px;
            border-radius: 6px;
            margin-top: 8px;
            border: 1px solid #ddd;
        }
        
        .path-node {
            display: inline-block;
            padding: 5px 10px;
            background: #667eea;
            color: white;
            border-radius: 15px;
            margin: 2px;
        }
        
        .path-arrow {
            display: inline-block;
            margin: 0 5px;
            color: #666;
        }
        
        .score-display {
            font-size: 1.2em;
            color: #764ba2;
            font-weight: 600;
            margin-top: 10px;
        }
        
        .success-msg {
            background: #d4edda;
            color: #155724;
            padding: 10px;
            border-radius: 6px;
            margin-top: 10px;
            border: 1px solid #c3e6cb;
        }
        
        .error-msg {
            background: #f8d7da;
            color: #721c24;
            padding: 10px;
            border-radius: 6px;
            margin-top: 10px;
            border: 1px solid #f5c6cb;
        }
        
        .stats {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-top: 15px;
        }
        
        .stat-item {
            background: #f8f9fa;
            padding: 10px;
            border-radius: 6px;
            text-align: center;
        }
        
        .stat-value {
            font-size: 1.5em;
            font-weight: 600;
            color: #764ba2;
        }
        
        .stat-label {
            color: #666;
            font-size: 0.9em;
            margin-top: 3px;
        }
        
        /* Graph styling */
        .node {
            stroke: #fff;
            stroke-width: 2px;
            cursor: pointer;
            transition: r 0.3s;
        }
        
        .node:hover {
            stroke-width: 3px;
        }
        
        .link {
            stroke-opacity: 0.6;
            transition: stroke-width 0.3s;
        }
        
        .link:hover {
            stroke-width: 4px;
            stroke-opacity: 1;
        }
        
        .node-label {
            font-size: 12px;
            pointer-events: none;
            text-anchor: middle;
            fill: #333;
            font-weight: 600;
        }
        
        .link-label {
            font-size: 11px;
            fill: #333;
            text-anchor: middle;
            pointer-events: none;
            opacity: 1;
            transition: opacity 0.3s;
            font-weight: 600;
            stroke: white;
            stroke-width: 4px;
            stroke-linejoin: round;
            paint-order: stroke fill;
        }
        
        .hide-labels .link-label {
            opacity: 0;
        }
        
        .highlighted {
            stroke: #ff6b6b !important;
            stroke-width: 4px !important;
            stroke-opacity: 1 !important;
        }
        
        .path-node-highlighted {
            fill: #ff6b6b !important;
            r: 12 !important;
        }
        
        svg {
            width: 100%;
            height: 100%;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤝 Friend Connection System</h1>
        <div class="main-content">
            <div class="controls">
                <div class="section">
                    <h2>📍 Find Shortest Path</h2>
                    <div class="input-group">
                        <label for="person1">Person 1:</label>
                        <input type="text" id="person1" placeholder="Enter name">
                    </div>
                    <div class="input-group">
                        <label for="person2">Person 2:</label>
                        <input type="text" id="person2" placeholder="Enter name">
                    </div>
                    <button onclick="findPath()">Find Path</button>
                    <div id="pathResult"></div>
                </div>
                
                <div class="section">
                    <h2>➕ Add Connection</h2>
                    <div class="input-group">
                        <label for="friend1">Friend 1:</label>
                        <input type="text" id="friend1" placeholder="Enter name">
                    </div>
                    <div class="input-group">
                        <label for="friend2">Friend 2:</label>
                        <input type="text" id="friend2" placeholder="Enter name">
                    </div>
                    <div class="input-group">
                        <label for="score">Connection Score:</label>
                        <input type="number" id="score" placeholder="1-100" min="1" max="100">
                    </div>
                    <button onclick="addConnection()">Add Connection</button>
                    <div id="addResult"></div>
                </div>
                
                <div class="section">
                    <h2>📊 Network Statistics</h2>
                    <div class="stats">
                        <div class="stat-item">
                            <div class="stat-value" id="nodeCount">0</div>
                            <div class="stat-label">People</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-value" id="edgeCount">0</div>
                            <div class="stat-label">Connections</div>
                        </div>
                    </div>
                    <button onclick="toggleLabels()" style="margin-top: 10px;">👁️ Hide/Show Edge Labels</button>
                    <button onclick="refreshGraph()" style="margin-top: 10px;">🔄 Refresh Graph</button>
                </div>
            </div>
            
            <div class="graph-container" id="graphContainer">
                <svg id="graph"></svg>
            </div>
        </div>
    </div>

    <script>
        let graphData = { nodes: [], edges: [] };
        let simulation;
        let svg;
        let g;
        
        // Initialize the graph
        function initGraph() {
            const container = document.getElementById('graphContainer');
            const width = container.clientWidth;
            const height = container.clientHeight;
            
            svg = d3.select('#graph')
                .attr('width', width)
                .attr('height', height);
            
            // Add zoom behavior
            const zoom = d3.zoom()
                .scaleExtent([0.1, 4])
                .on('zoom', (event) => {
                    g.attr('transform', event.transform);
                });
            
            svg.call(zoom);
            
            g = svg.append('g');
            
            // Initialize force simulation
            simulation = d3.forceSimulation()
                .force('link', d3.forceLink().id(d => d.id).distance(d => Math.max(50, d.weight * 3)))
                .force('charge', d3.forceManyBody().strength(-400))
                .force('center', d3.forceCenter(width / 2, height / 2))
                .force('collision', d3.forceCollide().radius(40));
        }
        
        // Update graph visualization
        function updateGraph() {
            // Clear previous elements
            g.selectAll('*').remove();
            
            // Create a container for the graph elements with proper layering
            const linkGroup = g.append('g').attr('class', 'link-group');
            const labelGroup = g.append('g').attr('class', 'label-group');
            const nodeGroup = g.append('g').attr('class', 'node-group');
            const nodeLabelGroup = g.append('g').attr('class', 'node-label-group');
            
            // Add links
            const link = linkGroup.selectAll('line')
                .data(graphData.edges)
                .enter().append('line')
                .attr('class', 'link')
                .attr('stroke', '#999')
                .attr('stroke-width', 2);
            
            // Add link labels with white background stroke - always visible
            const linkLabel = labelGroup.selectAll('.link-label')
                .data(graphData.edges)
                .enter().append('text')
                .attr('class', 'link-label')
                .text(d => d.weight);
            
            // Add nodes
            const node = nodeGroup.selectAll('circle')
                .data(graphData.nodes)
                .enter().append('circle')
                .attr('class', 'node')
                .attr('r', 8)
                .attr('fill', '#667eea')
                .call(drag(simulation));
            
            // Add node labels
            const nodeLabel = nodeLabelGroup.selectAll('text')
                .data(graphData.nodes)
                .enter().append('text')
                .attr('class', 'node-label')
                .text(d => d.label)
                .attr('dy', -15);
            
            // Update positions on tick
            simulation
                .nodes(graphData.nodes)
                .on('tick', () => {
                    link
                        .attr('x1', d => d.source.x)
                        .attr('y1', d => d.source.y)
                        .attr('x2', d => d.target.x)
                        .attr('y2', d => d.target.y);
                    
                    // Position labels with slight offset to avoid overlap with the line
                    linkLabel.each(function(d) {
                        const dx = d.target.x - d.source.x;
                        const dy = d.target.y - d.source.y;
                        const length = Math.sqrt(dx * dx + dy * dy);
                        const offsetX = (dy / length) * 10;  // Perpendicular offset
                        const offsetY = -(dx / length) * 10;
                        
                        d3.select(this)
                            .attr('x', (d.source.x + d.target.x) / 2 + offsetX)
                            .attr('y', (d.source.y + d.target.y) / 2 + offsetY);
                    });
                    
                    node
                        .attr('cx', d => d.x)
                        .attr('cy', d => d.y);
                    
                    nodeLabel
                        .attr('x', d => d.x)
                        .attr('y', d => d.y);
                });
            
            simulation.force('link')
                .links(graphData.edges)
                .distance(d => Math.max(50, d.weight * 3));  // Minimum distance to prevent overlap
            
            simulation.alpha(1).restart();
            
            // Update statistics
            document.getElementById('nodeCount').textContent = graphData.nodes.length;
            document.getElementById('edgeCount').textContent = graphData.edges.length;
        }
        
        // Toggle label visibility
        function toggleLabels() {
            const container = document.getElementById('graphContainer');
            container.classList.toggle('hide-labels');
        }
        
        // Drag behavior
        function drag(simulation) {
            function dragstarted(event, d) {
                if (!event.active) simulation.alphaTarget(0.3).restart();
                d.fx = d.x;
                d.fy = d.y;
            }
            
            function dragged(event, d) {
                d.fx = event.x;
                d.fy = event.y;
            }
            
            function dragended(event, d) {
                if (!event.active) simulation.alphaTarget(0);
                d.fx = null;
                d.fy = null;
            }
            
            return d3.drag()
                .on('start', dragstarted)
                .on('drag', dragged)
                .on('end', dragended);
        }
        
        // Find shortest path
        async function findPath() {
            const person1 = document.getElementById('person1').value;
            const person2 = document.getElementById('person2').value;
            
            if (!person1 || !person2) {
                document.getElementById('pathResult').innerHTML = 
                    '<div class="error-msg">Please enter both names</div>';
                return;
            }
            
            try {
                const response = await fetch('/api/find_path', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ person1, person2 })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    let html = '<div class="result-box">';
                    html += '<div class="result-title">Shortest Path Found!</div>';
                    html += '<div class="path-display">';
                    
                    result.path.forEach((node, i) => {
                        html += `<span class="path-node">${node}</span>`;
                        if (i < result.path.length - 1) {
                            html += '<span class="path-arrow">→</span>';
                        }
                    });
                    
                    html += '</div>';
                    html += `<div class="score-display">Total Score: ${result.score}</div>`;
                    html += '</div>';
                    
                    document.getElementById('pathResult').innerHTML = html;
                    highlightPath(result.path);
                } else {
                    document.getElementById('pathResult').innerHTML = 
                        `<div class="error-msg">${result.message}</div>`;
                }
            } catch (error) {
                document.getElementById('pathResult').innerHTML = 
                    '<div class="error-msg">Error finding path</div>';
            }
        }
        
        // Highlight path on graph
        function highlightPath(path) {
            // Reset all highlights
            d3.selectAll('.link').classed('highlighted', false);
            d3.selectAll('.node').classed('path-node-highlighted', false);
            
            // Highlight path nodes
            d3.selectAll('.node')
                .classed('path-node-highlighted', d => path.includes(d.id));
            
            // Create a set of edge pairs in the path
            const pathEdges = new Set();
            for (let i = 0; i < path.length - 1; i++) {
                // Store edges in both directions for easier lookup
                pathEdges.add(`${path[i]}-${path[i + 1]}`);
                pathEdges.add(`${path[i + 1]}-${path[i]}`);
            }
            
            // Highlight all path edges at once
            d3.selectAll('.link')
                .classed('highlighted', d => {
                    const edgeKey1 = `${d.source.id}-${d.target.id}`;
                    const edgeKey2 = `${d.target.id}-${d.source.id}`;
                    return pathEdges.has(edgeKey1) || pathEdges.has(edgeKey2);
                });
        }
        
        // Add new connection
        async function addConnection() {
            const friend1 = document.getElementById('friend1').value;
            const friend2 = document.getElementById('friend2').value;
            const score = parseInt(document.getElementById('score').value);
            
            if (!friend1 || !friend2 || !score) {
                document.getElementById('addResult').innerHTML = 
                    '<div class="error-msg">Please fill all fields</div>';
                return;
            }
            
            try {
                const response = await fetch('/api/add_relation', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ friend1, friend2, score })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    document.getElementById('addResult').innerHTML = 
                        '<div class="success-msg">Connection added successfully!</div>';
                    
                    // Clear inputs
                    document.getElementById('friend1').value = '';
                    document.getElementById('friend2').value = '';
                    document.getElementById('score').value = '';
                    
                    // Refresh graph
                    await loadGraph();
                } else {
                    document.getElementById('addResult').innerHTML = 
                        `<div class="error-msg">${result.message}</div>`;
                }
            } catch (error) {
                document.getElementById('addResult').innerHTML = 
                    '<div class="error-msg">Error adding connection</div>';
            }
        }
        
        // Load graph data from server
        async function loadGraph() {
            try {
                const response = await fetch('/api/graph_data');
                const data = await response.json();
                
                graphData = {
                    nodes: data.nodes,
                    edges: data.edges.map(e => ({
                        source: e.source,
                        target: e.target,
                        weight: e.weight
                    }))
                };
                
                updateGraph();
            } catch (error) {
                console.error('Error loading graph:', error);
            }
        }
        
        // Refresh graph
        function refreshGraph() {
            loadGraph();
        }
        
        // Initialize on load
        window.addEventListener('load', () => {
            initGraph();
            loadGraph();
        });
        
        // Handle window resize
        window.addEventListener('resize', () => {
            const container = document.getElementById('graphContainer');
            const width = container.clientWidth;
            const height = container.clientHeight;
            
            svg.attr('width', width).attr('height', height);
            simulation.force('center', d3.forceCenter(width / 2, height / 2));
            simulation.alpha(0.3).restart();
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/graph_data')
def get_graph_data():
    """Get complete graph data for visualization"""
    return jsonify(backend.get_graph_data())

@app.route('/api/find_path', methods=['POST'])
def find_path():
    """Find shortest path between two people"""
    data = request.json
    person1 = data.get('person1')
    person2 = data.get('person2')
    
    if not person1 or not person2:
        return jsonify({'success': False, 'message': 'Both names are required'})
    
    score, path = backend.get_best_path(person1, person2)
    
    if path is None:
        return jsonify({
            'success': False, 
            'message': f'No connection found between {person1} and {person2}'
        })
    
    return jsonify({
        'success': True,
        'score': score,
        'path': path
    })

@app.route('/api/add_relation', methods=['POST'])
def add_relation():
    """Add a new relationship"""
    data = request.json
    friend1 = data.get('friend1')
    friend2 = data.get('friend2')
    score = data.get('score')
    
    if not all([friend1, friend2, score]):
        return jsonify({'success': False, 'message': 'All fields are required'})
    
    try:
        score = int(score)
        if score <= 0:
            return jsonify({'success': False, 'message': 'Score must be positive'})
        
        backend.add_relation(friend1, friend2, score)
        return jsonify({'success': True, 'message': 'Relationship added successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/check_relation', methods=['POST'])
def check_relation():
    """Check if two people are connected"""
    data = request.json
    person1 = data.get('person1')
    person2 = data.get('person2')
    
    if not person1 or not person2:
        return jsonify({'success': False, 'message': 'Both names are required'})
    
    connected = backend.check_relation(person1, person2)
    return jsonify({
        'success': True,
        'connected': connected
    })

@app.route('/api/components')
def get_components():
    """Get all connected components"""
    components = backend.get_connected_components()
    return jsonify({
        'success': True,
        'components': components,
        'count': len(components)
    })

if __name__ == '__main__':
    print("=" * 50)
    print("Friend Connection System Server")
    print("=" * 50)
    print("Server is starting at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    app.run(debug=True, port=5000)