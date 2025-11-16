from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
from Backend import Backend
from persona_data import PERSONAS, get_persona
import os
import atexit

app = Flask(__name__)
CORS(app)

# Initialize backend
def create_backend():
    """Load backend data from any available friendship data file."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    possible_files = [
        'friendship_data.json',
        'friendship_data.txt',
        'friendship_data_long_dis.txt',
    ]
    for data_file in possible_files:
        file_path = os.path.join(base_dir, data_file)
        if os.path.exists(file_path):
            print(f"Loading friendship data from {file_path}")
            return Backend(path=file_path)
    
    # Create empty backend if no data file exists
    print("No friendship data file found. Initializing empty backend.")
    backend_instance = Backend.__new__(Backend)
    backend_instance.init_space()
    return backend_instance

# Handle different initialization scenarios
try:
    backend = create_backend()
except Exception as e:
    # Fallback to empty initialization if file reading fails
    print(f"Warning: Could not load friendship data file: {e}")
    backend = Backend.__new__(Backend)
    backend.init_space()
atexit.register(lambda : backend.when_exit())

# HTML template will be served from here
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Friend Connection System</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">
</head>
<body>
    <div class="container">
        <h1>Friend Connection System</h1>
        <div class="main-content">
            <div class="controls">
                <div class="section">
                    <h2>Path Score Limit</h2>
                    <div class="input-group">
                        <label for="pathLimit">Maximum Path Score:</label>
                        <input type="number" id="pathLimit" placeholder="0-100" min="0" max="100" value="0">
                        <small>Maximum total score for a valid path (0 = unlimited)</small>
                    </div>
                    <button onclick="updateLimitation()">Update Limit</button>
                    <div id="limitResult"></div>
                    <div class="limitation-display" style="margin-top: 10px;">
                        <div class="limitation-value">Current Limit: <span id="currentLimit">30</span></div>
                    </div>
                </div>
                
                <div class="section">
                    <h2>Find Shortest Path</h2>
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
                    <button onclick="resetPathInterface()" style="margin-top: 10px;">Reset Path View</button>
                </div>
                
                <div class="section">
                    <h2>Find Target Profile</h2>
                    <div class="input-group">
                        <label for="startPerson">Starting Person:</label>
                        <input type="text" id="startPerson" placeholder="Enter name">
                    </div>
                    <div class="input-group">
                        <label for="targetKeyword">Target Keyword:</label>
                        <input type="text" id="targetKeyword" placeholder="Enter keyword to search in profiles">
                    </div>
                    <button onclick="findTarget()">Find Target</button>
                    <div id="targetResult"></div>
                </div>
                
                <div class="section">
                    <h2>Add Connection</h2>
                    <div class="input-group">
                        <label for="friend1">Friend 1:</label>
                        <input type="text" id="friend1" placeholder="Enter name">
                    </div>
                    <div class="input-group">
                        <label for="friend2">Friend 2:</label>
                        <input type="text" id="friend2" placeholder="Enter name">
                    </div>
                    <div class="input-group">
                        <label for="score">Connection Score (1=closest, 10=distant):</label>
                        <input type="number" id="score" placeholder="1-10" min="1" max="10" step="1">
                        <small>Lower scores = stronger friendships</small>
                    </div>
                    <button onclick="addConnection()">Add Connection</button>
                    <div id="addResult"></div>
                </div>
                
                <div class="section">
                    <h2>Network Statistics</h2>
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
                    <button onclick="toggleLabels()" style="margin-top: 10px;">Toggle Edge Labels</button>
                    <button onclick="refreshGraph()" style="margin-top: 10px;">Refresh Graph</button>
                </div>
                <div class="section">
                    <h2>Persona Spotlight</h2>
                    <div id="personaPreviewEmpty" class="persona-helper">
                        Back to HomeBack to HomeBack to HomeBack to Home||
                    </div>
                    <div id="personaPreviewError" class="error-msg hidden"></div>
                    <div id="personaPreviewCard" class="persona-preview-card hidden">
                        <div class="persona-preview-header">
                            <div>
                                <div class="persona-preview-name" id="personaName"></div>
                                <div class="persona-preview-role" id="personaTitle"></div>
                            </div>
                            <div class="persona-meta" id="personaMeta"></div>
                        </div>
                        <p id="personaSummary" class="persona-summary" style="font-size: 0.95em; color: #444; margin-top: 10px;"></p>
                        <div class="persona-tags" id="personaTraits"></div>
                        <div class="persona-lists">
                            <div>
                                <h3 style="font-size: 0.9em; color: #5b48c4; margin-bottom: 4px;">Motivations & Goals</h3>
                                <ul id="personaGoals" class="persona-list"></ul>
                            </div>
                            <div>
                                <h3 style="font-size: 0.9em; color: #5b48c4; margin-bottom: 4px;">Pain Points</h3>
                                <ul id="personaPains" class="persona-list"></ul>
                            </div>
                        </div>
                        <p id="personaTechnology" style="font-size: 0.9em; color: #555;"></p>
                        <p id="personaInsight" style="font-size: 0.9em; color: #444; font-weight: 500;"></p>
                        <div class="persona-preview-actions">
                            <span class="persona-meta" id="personaStatus">Back to HomeBack to HomeBack to Home|</span>
                            <a id="personaProfileButton" class="persona-link disabled" href="#" target="_blank" rel="noopener">Back to Home|</a>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="graph-container" id="graphContainer">
                <svg id="graph"></svg>
            </div>
        </div>
    </div>

    <div id="personaTooltip" class="persona-tooltip hidden">
        <div class="tooltip-name" id="tooltipName"></div>
        <div class="tooltip-role" id="tooltipTitle"></div>
        <div class="tooltip-meta" id="tooltipMeta"></div>
        <p class="tooltip-summary" id="tooltipSummary"></p>
    </div>

    <script>
        let graphData = { nodes: [], edges: [] };
        let simulation;
        let svg;
        let g;
        let currentLimitation = 30;
        const nameInputIds = ['person1', 'person2', 'friend1', 'friend2', 'startPerson'];
        let activeNameInput = null;
        let personaPreviewElements = {};
        let currentPersonaId = null;
        let personaCache = {};
        let personaTooltipElements = {};
        let tooltipHideTimeout = null;
        const defaultPathMessage = `
            <div class="info-msg">
                Select two friends and press "Find Path" to display the shortest route and total score.
            </div>
        `;

        function setupInputFocusTracking() {
            nameInputIds.forEach(id => {
                const input = document.getElementById(id);
                if (!input) return;

                input.addEventListener('focus', () => {
                    activeNameInput = input;
                });
            });
        }

        function initPersonaPreview() {
            personaPreviewElements = {
                empty: document.getElementById('personaPreviewEmpty'),
                error: document.getElementById('personaPreviewError'),
                card: document.getElementById('personaPreviewCard'),
                name: document.getElementById('personaName'),
                title: document.getElementById('personaTitle'),
                meta: document.getElementById('personaMeta'),
                summary: document.getElementById('personaSummary'),
                traits: document.getElementById('personaTraits'),
                goals: document.getElementById('personaGoals'),
                pains: document.getElementById('personaPains'),
                technology: document.getElementById('personaTechnology'),
                insight: document.getElementById('personaInsight'),
                link: document.getElementById('personaProfileButton'),
                status: document.getElementById('personaStatus')
            };
        }

        function showPersonaPlaceholder(message) {
            if (personaPreviewElements.empty) {
                personaPreviewElements.empty.textContent = message;
                personaPreviewElements.empty.classList.remove('hidden');
            }
            if (personaPreviewElements.error) {
                personaPreviewElements.error.classList.add('hidden');
                personaPreviewElements.error.textContent = '';
            }
            if (personaPreviewElements.card) {
                personaPreviewElements.card.classList.add('hidden');
            }
            if (personaPreviewElements.link) {
                personaPreviewElements.link.classList.add('disabled');
                personaPreviewElements.link.href = '#';
            }
        }

        async function getPersonaData(name) {
            if (!name) {
                throw new Error('Invalid name');
            }
            if (personaCache[name]) {
                return personaCache[name];
            }
            const response = await fetch(`/api/persona/${encodeURIComponent(name)}`);
            const data = await response.json();
            if (!response.ok || !data.success || !data.persona) {
                throw new Error(data.message || 'Unable to load profile');
            }
            personaCache[name] = data.persona;
            return data.persona;
        }

        function initPersonaTooltip() {
            personaTooltipElements = {
                container: document.getElementById('personaTooltip'),
                name: document.getElementById('tooltipName'),
                title: document.getElementById('tooltipTitle'),
                meta: document.getElementById('tooltipMeta'),
                summary: document.getElementById('tooltipSummary'),
            };
            if (personaTooltipElements.container) {
                personaTooltipElements.container.classList.add('hidden');
                personaTooltipElements.container.classList.remove('loading');
            }
        }

        function truncateText(text, maxLength = 120) {
            if (!text) return '';
            return text.length > maxLength ? `${text.slice(0, maxLength).trim()}...` : text;
        }

        function positionPersonaTooltip(x, y) {
            const tooltip = personaTooltipElements.container;
            if (!tooltip) return;
            const offset = 16;
            const padding = 12;
            const tooltipWidth = tooltip.offsetWidth || 260;
            const tooltipHeight = tooltip.offsetHeight || 140;
            let left = x + offset;
            let top = y + offset;
            const maxX = window.innerWidth - tooltipWidth - padding;
            const maxY = window.innerHeight - tooltipHeight - padding;
            left = Math.min(Math.max(padding, left), Math.max(padding, maxX));
            top = Math.min(Math.max(padding, top), Math.max(padding, maxY));
            tooltip.style.left = `${left}px`;
            tooltip.style.top = `${top}px`;
        }

        function showPersonaTooltipLoading(name, event) {
            const tooltip = personaTooltipElements.container;
            if (!tooltip) return;
            if (tooltipHideTimeout) {
                clearTimeout(tooltipHideTimeout);
                tooltipHideTimeout = null;
            }
            tooltip.classList.remove('hidden');
            tooltip.classList.add('loading');
            if (personaTooltipElements.name) {
                personaTooltipElements.name.textContent = name || 'Loading...';
            }
            if (personaTooltipElements.title) {
                personaTooltipElements.title.textContent = 'Loading...';
            }
            if (personaTooltipElements.meta) {
                personaTooltipElements.meta.textContent = '';
            }
            if (personaTooltipElements.summary) {
                personaTooltipElements.summary.textContent = 'Fetching profile...';
            }
            if (event) {
                positionPersonaTooltip(event.clientX, event.clientY);
            }
        }

        function renderPersonaTooltip(persona, event) {
            const tooltip = personaTooltipElements.container;
            if (!tooltip || !persona) return;
            if (tooltipHideTimeout) {
                clearTimeout(tooltipHideTimeout);
                tooltipHideTimeout = null;
            }
            tooltip.classList.remove('hidden');
            tooltip.classList.remove('loading');
            if (personaTooltipElements.name) {
                personaTooltipElements.name.textContent = persona.full_name;
            }
            if (personaTooltipElements.title) {
                personaTooltipElements.title.textContent = persona.title;
            }
            if (personaTooltipElements.meta) {
                personaTooltipElements.meta.textContent = `ID: ${persona.id} | Age ${persona.age}`;
            }
            if (personaTooltipElements.summary) {
                const summary = persona.summary || persona.system_insight || '';
                personaTooltipElements.summary.textContent = truncateText(summary, 140);
            }
            if (event) {
                positionPersonaTooltip(event.clientX, event.clientY);
            }
        }

        function showPersonaTooltipError(name, error, event) {
            const tooltip = personaTooltipElements.container;
            if (!tooltip) return;
            tooltip.classList.remove('hidden');
            tooltip.classList.add('loading');
            if (personaTooltipElements.name) {
                personaTooltipElements.name.textContent = name;
            }
            if (personaTooltipElements.title) {
                personaTooltipElements.title.textContent = 'No data available';
            }
            if (personaTooltipElements.meta) {
                personaTooltipElements.meta.textContent = '';
            }
            if (personaTooltipElements.summary) {
                personaTooltipElements.summary.textContent = error?.message || 'This friend has not shared a profile yet.';
            }
            if (event) {
                positionPersonaTooltip(event.clientX, event.clientY);
            }
        }

        function hidePersonaTooltip() {
            const tooltip = personaTooltipElements.container;
            if (!tooltip) return;
            tooltip.classList.add('hidden');
            tooltip.classList.remove('loading');
        }

        function scheduleTooltipHide() {
            if (tooltipHideTimeout) {
                clearTimeout(tooltipHideTimeout);
            }
            tooltipHideTimeout = setTimeout(() => {
                hidePersonaTooltip();
            }, 200);
        }

        function updateTooltipPosition(event) {
            const tooltip = personaTooltipElements.container;
            if (!tooltip || tooltip.classList.contains('hidden')) return;
            positionPersonaTooltip(event.clientX, event.clientY);
        }

        async function handleNodeHover(event, nodeData) {
            const name = nodeData?.id || nodeData?.label;
            if (!name) return;
            showPersonaTooltipLoading(name, event);
            try {
                const persona = await getPersonaData(name);
                renderPersonaTooltip(persona, event);
            } catch (error) {
                showPersonaTooltipError(name, error, event);
            }
        }

        function fillList(element, items) {
            if (!element) return;
            element.innerHTML = '';
            if (!items || !items.length) {
                const li = document.createElement('li');
                li.textContent = 'No data available';
                element.appendChild(li);
                return;
            }
            items.forEach(item => {
                const li = document.createElement('li');
                li.textContent = item;
                element.appendChild(li);
            });
        }

        function renderPersonaPreview(persona) {
            if (!personaPreviewElements.card || !persona) {
                showPersonaPlaceholder("Select a node to preview this friend's profile.");
                return;
            }

            if (personaPreviewElements.empty) {
                personaPreviewElements.empty.classList.add('hidden');
            }
            if (personaPreviewElements.error) {
                personaPreviewElements.error.classList.add('hidden');
                personaPreviewElements.error.textContent = '';
            }

            personaPreviewElements.name.textContent = persona.full_name;
            personaPreviewElements.title.textContent = persona.title;
            personaPreviewElements.meta.textContent = `ID: ${persona.id} | Age ${persona.age}`;
            personaPreviewElements.summary.textContent = persona.summary;
            personaPreviewElements.technology.textContent = persona.technology;
            personaPreviewElements.insight.textContent = persona.system_insight;

            if (personaPreviewElements.traits) {
                personaPreviewElements.traits.innerHTML = '';
                (persona.personality_traits || []).forEach(trait => {
                    const pill = document.createElement('span');
                    pill.className = 'persona-tag';
                    pill.textContent = trait;
                    personaPreviewElements.traits.appendChild(pill);
                });
            }

            fillList(personaPreviewElements.goals, persona.goals);
            fillList(personaPreviewElements.pains, persona.pain_points);

            if (personaPreviewElements.link) {
                personaPreviewElements.link.href = `/profile/${encodeURIComponent(persona.id)}`;
                personaPreviewElements.link.classList.remove('disabled');
            }

            if (personaPreviewElements.status) {
                personaPreviewElements.status.textContent = `Currently selected: ${persona.id} (double-click the node or use the button to open the full page)`;
            }

            personaPreviewElements.card.classList.remove('hidden');
        }

        async function loadPersonaPreview(name) {
            if (!name) {
                showPersonaPlaceholder("Select a node to preview this friend's profile.");
                return;
            }

            currentPersonaId = name;
            const requestName = name;

            if (personaPreviewElements.error) {
                personaPreviewElements.error.classList.add('hidden');
                personaPreviewElements.error.textContent = '';
            }

            showPersonaPlaceholder(`Loading ${name}'s profile...`);

            try {
                const persona = await getPersonaData(name);
                if (currentPersonaId !== requestName) {
                    return;
                }
                renderPersonaPreview(persona);
            } catch (error) {
                if (currentPersonaId !== requestName) {
                    return;
                }
                if (personaPreviewElements.error) {
                    personaPreviewElements.error.textContent = error.message || 'Unable to load profile';
                    personaPreviewElements.error.classList.remove('hidden');
                }
                showPersonaPlaceholder(`${name} does not have a profile yet.`);
            }
        }

        function openPersonaPage(name) {
            if (!name) return;
            window.open(`/profile/${encodeURIComponent(name)}`, '_blank');
        }

        function getTrackedInputs() {
            return nameInputIds
                .map(id => document.getElementById(id))
                .filter(input => input instanceof HTMLInputElement);
        }

        function handleNodeClick(nodeData) {
            const inputs = getTrackedInputs();
            const name = nodeData?.id || nodeData?.label;
            if (!name) {
                return;
            }

            loadPersonaPreview(name);

            if (!inputs.length) {
                return;
            }

            let targetInput = null;

            if (activeNameInput && inputs.includes(activeNameInput)) {
                targetInput = activeNameInput;
            } else if (inputs.includes(document.activeElement)) {
                targetInput = document.activeElement;
            }

            if (!targetInput) {
                targetInput = inputs.find(input => !input.value) || inputs[0];
            }

            if (targetInput) {
                targetInput.value = name;
                let nextInput = null;
                
                // Determine next input based on cycling within pairs
                const targetId = targetInput.id;
                
                if (targetId === 'person1') {
                    nextInput = document.getElementById('person2');
                } else if (targetId === 'person2') {
                    nextInput = document.getElementById('person1');  // Cycle back to person1
                } else if (targetId === 'friend1') {
                    nextInput = document.getElementById('friend2');
                } else if (targetId === 'friend2') {
                    nextInput = document.getElementById('friend1');  // Cycle back to friend1
                }

                if (nextInput) {
                    nextInput.focus();
                    activeNameInput = nextInput;
                } else {
                    targetInput.focus();
                    activeNameInput = targetInput;
                }
            }
        }

        // Update path limitation
        async function updateLimitation() {
            const limit = parseInt(document.getElementById('pathLimit').value);
            
            if (isNaN(limit) || limit < 0 || limit > 100) {
                document.getElementById('limitResult').innerHTML = 
                    '<div class="error-msg">Limit must be between 0 and 100</div>';
                return;
            }
            
            try {
                const response = await fetch('/api/set_limitation', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ limit })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    currentLimitation = limit;
                    document.getElementById('currentLimit').textContent = limit === 0 ? 'Unlimited' : limit;
                    document.getElementById('limitResult').innerHTML = 
                        `<div class="success-msg">Path limit updated to ${limit === 0 ? 'unlimited' : limit}</div>`;
                    
                    // Clear the message after 3 seconds
                    setTimeout(() => {
                        document.getElementById('limitResult').innerHTML = '';
                    }, 3000);
                } else {
                    document.getElementById('limitResult').innerHTML = 
                        `<div class="error-msg">${result.message}</div>`;
                }
            } catch (error) {
                document.getElementById('limitResult').innerHTML = 
                    '<div class="error-msg">Error updating limitation</div>';
            }
        }

        // Find target person with keyword
        async function findTarget() {
            const startPerson = document.getElementById('startPerson').value;
            const targetKeyword = document.getElementById('targetKeyword').value;
            
            if (!startPerson || !targetKeyword) {
                document.getElementById('targetResult').innerHTML = 
                    '<div class="error-msg">Please enter both starting person and target keyword</div>';
                return;
            }
            
            try {
                const response = await fetch('/api/find_target', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ start: startPerson, target: targetKeyword })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    let html = '<div class="result-box">';
                    html += '<div class="result-title">Target Found!</div>';
                    html += `<div class="found-person">Person: <strong>${result.found_person}</strong></div>`;
                    html += '<div class="path-display">';
                    
                    result.path.forEach((node, i) => {
                        html += `<span class="path-node">${node}</span>`;
                        if (i < result.path.length - 1) {
                            html += '<span class="path-arrow">&rarr;</span>';
                        }
                    });
                    
                    html += '</div>';
                    html += `<div class="match-info">Matched keyword "${targetKeyword}" in ${result.found_person}'s profile</div>`;
                    html += '</div>';
                    
                    document.getElementById('targetResult').innerHTML = html;
                    highlightPath(result.path);
                } else {
                    document.getElementById('targetResult').innerHTML = 
                        `<div class="error-msg">${result.message}</div>`;
                    
                    // Clear any previous path highlights
                    g.selectAll('.link').classed('highlighted', false);
                    g.selectAll('.node').classed('path-node-highlighted', false);
                    g.selectAll('.link-label').classed('path-label-highlighted', false);
                }
            } catch (error) {
                document.getElementById('targetResult').innerHTML = 
                    '<div class="error-msg">Error finding target: ' + error.message + '</div>';
                
                // Clear any previous path highlights
                g.selectAll('.link').classed('highlighted', false);
                g.selectAll('.node').classed('path-node-highlighted', false);
                g.selectAll('.link-label').classed('path-label-highlighted', false);
            }
        }

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
                .force('link', d3.forceLink().id(d => d.id).distance(d => 20 + d.weight * 5))
                .force('charge', d3.forceManyBody().strength(-200))
                .force('center', d3.forceCenter(width / 2, height / 2))
                .force('collision', d3.forceCollide().radius(25))
                .force('x', d3.forceX(width / 2).strength(0.05))
                .force('y', d3.forceY(height / 2).strength(0.05));
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
                .attr('r', 7)
                .attr('fill', '#667eea')
                .call(drag(simulation))
                .on('click', (event, d) => handleNodeClick(d))
                .on('dblclick', (event, d) => {
                    event.stopPropagation();
                    openPersonaPage(d.id || d.label);
                })
                .on('mouseenter', (event, d) => handleNodeHover(event, d))
                .on('mousemove', updateTooltipPosition)
                .on('mouseleave', () => scheduleTooltipHide());

            // Add node labels
            const nodeLabel = nodeLabelGroup.selectAll('text')
                .data(graphData.nodes)
                .enter().append('text')
                .attr('class', 'node-label')
                .text(d => d.label)
                .attr('dy', -12)
                .on('click', (event, d) => handleNodeClick(d))
                .on('dblclick', (event, d) => {
                    event.stopPropagation();
                    openPersonaPage(d.id || d.label);
                })
                .on('mouseenter', (event, d) => handleNodeHover(event, d))
                .on('mousemove', updateTooltipPosition)
                .on('mouseleave', () => scheduleTooltipHide());
            
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
                        const offsetX = (dy / length) * 8;  // Smaller perpendicular offset
                        const offsetY = -(dx / length) * 8;
                        
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
                .distance(d => 20 + d.weight * 5);  // Distance scales with score
            
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
                        html += '<span class="path-arrow">&rarr;</span>';
                        }
                    });
                    
                    html += '</div>';
                    html += `<div class="score-display">Total Score: ${result.score}</div>`;
                    html += '</div>';
                    
                    document.getElementById('pathResult').innerHTML = html;
                    highlightPath(result.path);
                } else {
                    // Handle different failure reasons
                    let errorHtml = '';
                    
                    if (result.reason === 'no_connection') {
                        // No connection at all - they're in different components
                        errorHtml = `
                            <div class="error-msg">
                                <strong>No Connection Found</strong><br>
                                ${result.message}
                            </div>
                        `;
                    } else if (result.reason === 'exceeds_limit') {
                        // Connection exists but exceeds the weight limit
                        errorHtml = `
                            <div class="warning-msg">
                                <strong>Path Exceeds Limit</strong><br>
                                ${result.message}
                            </div>
                        `;
                    } else {
                        // Generic error
                        errorHtml = `<div class="error-msg">${result.message}</div>`;
                    }
                    
                    document.getElementById('pathResult').innerHTML = errorHtml;
                    
                    // Clear any previous path highlights
                    g.selectAll('.link').classed('highlighted', false);
                    g.selectAll('.node').classed('path-node-highlighted', false);
                    g.selectAll('.link-label').classed('path-label-highlighted', false);
                }
            } catch (error) {
                document.getElementById('pathResult').innerHTML = 
                    '<div class="error-msg">Error finding path: ' + error.message + '</div>';
                
                // Clear any previous path highlights
                g.selectAll('.link').classed('highlighted', false);
                g.selectAll('.node').classed('path-node-highlighted', false);
                g.selectAll('.link-label').classed('path-label-highlighted', false);
            }
        }
        
        // Highlight path on graph
        function highlightPath(path) {
            // Reset all highlights
            g.selectAll('.link').classed('highlighted', false);
            g.selectAll('.node').classed('path-node-highlighted', false);
            g.selectAll('.link-label').classed('path-label-highlighted', false);
            
            // Highlight path nodes
            g.selectAll('.node')
                .classed('path-node-highlighted', d => path.includes(d.id));
            
            // Create a set of edge pairs in the path
            const pathEdges = new Set();
            for (let i = 0; i < path.length - 1; i++) {
                // Store edges in both directions for easier lookup
                pathEdges.add(`${path[i]}-${path[i + 1]}`);
                pathEdges.add(`${path[i + 1]}-${path[i]}`);
            }
            
            // Highlight all path edges and their labels
            g.selectAll('.link')
                .classed('highlighted', d => {
                    const edgeKey1 = `${d.source.id}-${d.target.id}`;
                    const edgeKey2 = `${d.target.id}-${d.source.id}`;
                    const isInPath = pathEdges.has(edgeKey1) || pathEdges.has(edgeKey2);
                    
                    // Also highlight the labels for path edges
                    if (isInPath) {
                        g.selectAll('.link-label')
                            .filter(labelData => labelData === d)
                            .classed('path-label-highlighted', true);
                    }
                    
                    return isInPath;
                });
        }

        function resetPathInterface() {
            const resultContainer = document.getElementById('pathResult');
            if (resultContainer) {
                resultContainer.innerHTML = defaultPathMessage;
            }
            const p1 = document.getElementById('person1');
            const p2 = document.getElementById('person2');
            if (p1) p1.value = '';
            if (p2) p2.value = '';
            if (g) {
                g.selectAll('.link').classed('highlighted', false);
                g.selectAll('.node').classed('path-node-highlighted', false);
                g.selectAll('.link-label').classed('path-label-highlighted', false);
            }
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
            
            if (score < 1 || score > 10) {
                document.getElementById('addResult').innerHTML = 
                    '<div class="error-msg">Score must be between 1 and 10</div>';
                return;
            }
            
            if (friend1 === friend2) {
                document.getElementById('addResult').innerHTML = 
                    '<div class="error-msg">Cannot connect a person to themselves</div>';
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
        
        // Get current limitation from server
        async function getCurrentLimitation() {
            try {
                const response = await fetch('/api/get_limitation');
                const data = await response.json();
                if (data.success) {
                    currentLimitation = data.limit;
                    document.getElementById('pathLimit').value = currentLimitation;
                    document.getElementById('currentLimit').textContent = 
                        currentLimitation === 0 ? 'Unlimited' : currentLimitation;
                }
            } catch (error) {
                console.error('Error getting limitation:', error);
            }
        }
        
        // Refresh graph
        function refreshGraph() {
            loadGraph();
        }
        
        // Initialize on load
        window.addEventListener('load', () => {
            initGraph();
            setupInputFocusTracking();
            initPersonaPreview();
            initPersonaTooltip();
            showPersonaPlaceholder("Select a node to preview this friend's profile.");
            const pathResult = document.getElementById('pathResult');
            if (pathResult) {
                pathResult.innerHTML = defaultPathMessage;
            }
            loadGraph();
            getCurrentLimitation();
        });
        
        // Handle window resize
        window.addEventListener('resize', () => {
            const container = document.getElementById('graphContainer');
            const width = container.clientWidth;
            const height = container.clientHeight;
            
            svg.attr('width', width).attr('height', height);
            simulation.force('center', d3.forceCenter(width / 2, height / 2));
            simulation.force('x', d3.forceX(width / 2).strength(0.05));
            simulation.force('y', d3.forceY(height / 2).strength(0.05));
            simulation.alpha(0.3).restart();
        });
    </script>
</body>
</html>
'''

PROFILE_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ persona.full_name if persona else person_id }} - Friend Profile</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/profile.css') }}">
</head>
<body>
    <div class="profile-container">
        <a class="back-link" href="/">&#8592; Back to Home</a>
        {% if persona %}
            <h1>{{ persona.full_name }}</h1>
            <p class="subtitle">{{ persona.title }}</p>
            <div class="meta">
                <span>Nickname: {{ persona.id }}</span>
                <span>Age: {{ persona.age }}</span>
            </div>
            <div class="card">
                <h2>Profile Summary</h2>
                <p>{{ persona.summary }}</p>
            </div>
            <div class="profile-grid">
                <div class="card">
                    <h2>Personality Traits</h2>
                    <ul class="pill-list">
                        {% for trait in persona.personality_traits %}
                        <li>{{ trait }}</li>
                        {% endfor %}
                    </ul>
                </div>
                <div class="card">
                    <h2>Technology & Social Behavior</h2>
                    <p>{{ persona.technology }}</p>
                </div>
                <div class="card">
                    <h2>Pain Points</h2>
                    <ul>
                        {% for pain in persona.pain_points %}
                        <li>{{ pain }}</li>
                        {% endfor %}
                    </ul>
                </div>
                <div class="card">
                    <h2>Motivations & Goals</h2>
                    <ul>
                        {% for goal in persona.goals %}
                        <li>{{ goal }}</li>
                        {% endfor %}
                    </ul>
                </div>
            </div>
            <div class="card" style="margin-top: 20px;">
                <h2>System Insight</h2>
                <p>{{ persona.system_insight }}</p>
            </div>
            <div class="profile-footer">
                <p>To explore more about {{ persona.full_name }} and their relationships, please return to the interactive network.</p>
                <a class="primary-btn" href="/">Back to Friend Connection System</a>
            </div>
        {% else %}
            <div class="empty-state">
                <h2>No profile found for {{ person_id }}</h2>
                <p>This node does not have a self-introduction yet. Please return to the main page.</p>
                <a class="primary-btn" href="/">Back to Home</a>
            </div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route('/profile/<person_id>')
def profile_page(person_id):
    """Render a standalone profile page for a given person."""
    persona = get_persona(person_id)
    return render_template_string(
        PROFILE_TEMPLATE,
        persona=persona,
        person_id=person_id
    )


@app.route('/api/persona/<person_id>')
def persona_api(person_id):
    """Return persona data for front-end previews."""
    persona = get_persona(person_id)
    if not persona:
        return jsonify({
            'success': False,
            'message': f'No persona data for {person_id}'
        }), 404
    return jsonify({
        'success': True,
        'persona': persona
    })

@app.route('/api/graph_data')
def get_graph_data():
    """Get complete graph data for visualization"""
    return jsonify(backend.get_graph_data())

@app.route('/api/set_limitation', methods=['POST'])
def set_limitation():
    """Set the path weight limitation"""
    data = request.json
    limit = data.get('limit')
    
    if limit is None:
        return jsonify({'success': False, 'message': 'Limit value is required'})
    
    try:
        limit = int(limit)
        if limit < 0 or limit > 100:
            return jsonify({'success': False, 'message': 'Limit must be between 0 and 100'})
        
        # Treat 0 as unlimited (set to a very high value)
        if limit == 0:
            backend.set_limitation(float('inf'))
        else:
            backend.set_limitation(limit)
        
        return jsonify({'success': True, 'message': f'Limitation set to {limit}'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/get_limitation')
def get_limitation():
    """Get the current path weight limitation"""
    try:
        current_limit = backend.graph.weight_limitation
        # Convert inf back to 0 for unlimited
        if current_limit == float('inf'):
            current_limit = 0
        return jsonify({'success': True, 'limit': current_limit})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/find_path', methods=['POST'])
def find_path():
    """Find shortest path between two people"""
    data = request.json
    person1 = data.get('person1')
    person2 = data.get('person2')
    
    if not person1 or not person2:
        return jsonify({'success': False, 'message': 'Both names are required'})
    
    score, path = backend.get_best_path(person1, person2)
    
    # Handle the three different return cases
    if score is None and path == []:
        # Connection exists but exceeds limitation
        current_limit = backend.graph.weight_limitation
        if current_limit == float('inf'):
            current_limit = "unlimited"
        return jsonify({
            'success': False,
            'reason': 'exceeds_limit',
            'message': f'Connection exists between {person1} and {person2}, but the shortest path exceeds the current limit of {current_limit}'
        })
    elif score is None and path is None:
        # No connection at all
        return jsonify({
            'success': False,
            'reason': 'no_connection',
            'message': f'No connection found between {person1} and {person2} - they are in different network components'
        })
    
    return jsonify({
        'success': True,
        'score': score,
        'path': path
    })

@app.route('/api/find_target', methods=['POST'])
def find_target():
    """Find a person whose profile contains a specific keyword"""
    data = request.json
    start = data.get('start')
    target = data.get('target')
    
    if not start or not target:
        return jsonify({'success': False, 'message': 'Both starting person and target keyword are required'})
    
    try:
        found_person, path = backend.find_target(start, target)
        
        if found_person is None:
            return jsonify({
                'success': False,
                'message': f'No person found with "{target}" in their profile from {start}'
            })
        
        return jsonify({
            'success': True,
            'found_person': found_person,
            'path': path,
            'message': f'Found {found_person} with matching profile'
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

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
        if score < 1 or score > 10:
            return jsonify({'success': False, 'message': 'Score must be between 1 and 10'})
        
        if friend1 == friend2:
            return jsonify({'success': False, 'message': 'Cannot connect a person to themselves'})
        
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
