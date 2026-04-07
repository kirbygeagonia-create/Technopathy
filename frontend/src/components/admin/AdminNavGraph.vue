<template>
  <div class="adminnavgraph-section">
    <div class="section-header">
      <div>
        <h1>Navigation Graph</h1>
        <p class="subtitle">Manage navigation nodes and connections</p>
      </div>
      <div class="header-actions">
        <button class="btn-secondary" @click="resetView">
          <span class="material-icons">refresh</span>
          Reset
        </button>
        <button class="btn-primary" @click="showAddNodeModal = true">
          <span class="material-icons">add_location</span>
          Add Node
        </button>
      </div>
    </div>

    <!-- Stats -->
    <div class="stats-row">
      <div class="stat-box">
        <span class="stat-number">{{ nodes.length }}</span>
        <span class="stat-label">Total Nodes</span>
      </div>
      <div class="stat-box">
        <span class="stat-number">{{ edges.length }}</span>
        <span class="stat-label">Connections</span>
      </div>
      <div class="stat-box">
        <span class="stat-number">{{ nodes.filter(n => n.type === 'room').length }}</span>
        <span class="stat-label">Rooms</span>
      </div>
      <div class="stat-box">
        <span class="stat-number">{{ nodes.filter(n => n.type === 'junction').length }}</span>
        <span class="stat-label">Junctions</span>
      </div>
    </div>

    <!-- Graph Visualization Placeholder -->
    <div class="graph-container">
      <div class="graph-placeholder">
        <span class="material-icons">account_tree</span>
        <p>Interactive Navigation Graph</p>
        <p class="sub-text">Visual graph editor would be implemented here with a library like Cytoscape.js or D3.js</p>
        <div class="mock-graph">
          <div class="mock-node entrance">Entrance</div>
          <div class="mock-edge"></div>
          <div class="mock-node junction">J1</div>
          <div class="mock-edge"></div>
          <div class="mock-node room">Room 101</div>
        </div>
      </div>
    </div>

    <!-- Nodes Table -->
    <div class="section-title">
      <h2>Navigation Nodes</h2>
    </div>
    <div class="table-container">
      <table class="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Type</th>
            <th>Floor</th>
            <th>Building</th>
            <th>Connections</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="node in nodes" :key="node.id">
            <td><code>{{ node.node_id }}</code></td>
            <td>{{ node.name }}</td>
            <td>
              <span :class="['type-badge', 'type-' + node.type]">{{ node.type }}</span>
            </td>
            <td>{{ node.floor }}</td>
            <td>{{ node.building }}</td>
            <td>{{ getConnectionCount(node.node_id) }}</td>
            <td>
              <div class="action-buttons">
                <button class="btn-icon" @click="editNode(node)" title="Edit">
                  <span class="material-icons">edit</span>
                </button>
                <button class="btn-icon" @click="connectNode(node)" title="Connect">
                  <span class="material-icons">timeline</span>
                </button>
                <button class="btn-icon btn-danger" @click="confirmDeleteNode(node)" title="Delete">
                  <span class="material-icons">delete</span>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Add/Edit Node Modal -->
    <div v-if="showAddNodeModal || showEditNodeModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-dialog">
        <div class="modal-header">
          <h2>{{ showEditNodeModal ? 'Edit Node' : 'Add Navigation Node' }}</h2>
          <button class="btn-close" @click="closeModal">
            <span class="material-icons">close</span>
          </button>
        </div>
        <div class="modal-body">
          <div class="form-row">
            <div class="form-group">
              <label>Node ID</label>
              <input v-model="nodeForm.node_id" type="text" placeholder="e.g., ROOM_101" />
            </div>
            <div class="form-group">
              <label>Type</label>
              <select v-model="nodeForm.type">
                <option value="room">Room</option>
                <option value="junction">Junction</option>
                <option value="entrance">Entrance</option>
                <option value="exit">Exit</option>
                <option value="stairs">Stairs</option>
                <option value="elevator">Elevator</option>
              </select>
            </div>
          </div>
          <div class="form-group">
            <label>Name</label>
            <input v-model="nodeForm.name" type="text" placeholder="Display name" />
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Building</label>
              <select v-model="nodeForm.building">
                <option v-for="b in buildings" :key="b.id" :value="b.code">{{ b.name }}</option>
              </select>
            </div>
            <div class="form-group">
              <label>Floor</label>
              <input v-model="nodeForm.floor" type="number" min="1" />
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>X Coordinate</label>
              <input v-model="nodeForm.x" type="number" step="0.1" />
            </div>
            <div class="form-group">
              <label>Y Coordinate</label>
              <input v-model="nodeForm.y" type="number" step="0.1" />
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-secondary" @click="closeModal">Cancel</button>
          <button class="btn-primary" @click="saveNode">{{ showEditNodeModal ? 'Save' : 'Add Node' }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../services/api.js'
import { showToast } from '../../services/toast.js'

const nodes = ref([])
const edges = ref([])
const buildings = ref([])
const showAddNodeModal = ref(false)
const showEditNodeModal = ref(false)

const nodeForm = ref({
  id: null,
  node_id: '',
  name: '',
  type: 'room',
  building: '',
  floor: 1,
  x: 0,
  y: 0
})

function getConnectionCount(nodeId) {
  return edges.value.filter(e => e.from === nodeId || e.to === nodeId).length
}

function editNode(node) {
  nodeForm.value = { ...node }
  showEditNodeModal.value = true
}

function connectNode(node) {
  showToast(`Connect node ${node.name} - Feature would open connection editor`, 'info')
}

function confirmDeleteNode(node) {
  if (confirm(`Delete node ${node.name}?`)) {
    deleteNode(node)
  }
}

function closeModal() {
  showAddNodeModal.value = false
  showEditNodeModal.value = false
  nodeForm.value = { id: null, node_id: '', name: '', type: 'room', building: '', floor: 1, x: 0, y: 0 }
}

function resetView() {
  loadData()
}

async function loadData() {
  try {
    const [nodesRes, edgesRes, buildingsRes] = await Promise.all([
      api.get('/navigation/nodes/'),
      api.get('/navigation/edges/'),
      api.get('/facilities/')
    ])
    nodes.value = nodesRes.data
    edges.value = edgesRes.data
    buildings.value = buildingsRes.data
  } catch (e) {
    console.error('Failed to load navigation data:', e)
    // Mock data
    nodes.value = [
      { id: 1, node_id: 'ENTRANCE_MAIN', name: 'Main Entrance', type: 'entrance', building: 'MAIN-ACAD', floor: 1, x: 0, y: 0 },
      { id: 2, node_id: 'J1_F1', name: 'Junction 1', type: 'junction', building: 'MAIN-ACAD', floor: 1, x: 10, y: 0 },
      { id: 3, node_id: 'ROOM_101', name: 'Room 101', type: 'room', building: 'MAIN-ACAD', floor: 1, x: 20, y: 5 },
      { id: 4, node_id: 'ROOM_102', name: 'Room 102', type: 'room', building: 'MAIN-ACAD', floor: 1, x: 20, y: -5 },
      { id: 5, node_id: 'STAIR_A', name: 'Stairwell A', type: 'stairs', building: 'MAIN-ACAD', floor: 1, x: 15, y: 0 }
    ]
    edges.value = [
      { id: 1, from: 'ENTRANCE_MAIN', to: 'J1_F1', weight: 10 },
      { id: 2, from: 'J1_F1', to: 'ROOM_101', weight: 15 },
      { id: 3, from: 'J1_F1', to: 'ROOM_102', weight: 15 },
      { id: 4, from: 'J1_F1', to: 'STAIR_A', weight: 5 }
    ]
    buildings.value = [
      { id: 1, code: 'MAIN-ACAD', name: 'Main Academic Building' }
    ]
  }
}

async function saveNode() {
  try {
    if (showEditNodeModal.value) {
      await api.put(`/navigation/nodes/${nodeForm.value.id}/`, nodeForm.value)
    } else {
      await api.post('/navigation/nodes/', nodeForm.value)
    }
    closeModal()
    loadData()
  } catch (e) {
    console.error('Failed to save node:', e)
  }
}

async function deleteNode(node) {
  try {
    await api.delete(`/navigation/nodes/${node.id}/`)
    loadData()
  } catch (e) {
    console.error('Failed to delete node:', e)
  }
}

onMounted(loadData)
</script>

<style scoped>
.adminnavgraph-section { padding: 0; font-family: var(--font-primary); max-width: 1400px; }

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.section-header h1 {
  font-size: var(--text-2xl);
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0 0 4px 0;
}

.subtitle {
  font-size: var(--text-base);
  color: var(--color-text-secondary);
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.btn-primary, .btn-secondary {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  border-radius: var(--radius-md);
  font-family: var(--font-primary);
  font-size: var(--text-sm);
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary {
  background: var(--color-primary);
  color: white;
  border: none;
}

.btn-primary:hover {
  background: var(--color-primary-dark);
}

.btn-secondary {
  background: var(--color-surface);
  color: var(--color-text-primary);
  border: 1px solid var(--color-border);
}

.btn-secondary:hover {
  background: var(--color-surface-2);
}

.stats-row {
  display: flex;
  gap: 16px;
  margin-bottom: 20px;
}

.stat-box {
  display: flex;
  flex-direction: column;
  padding: 14px 20px;
  background: var(--color-bg);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border);
  min-width: 100px;
}

.stat-number {
  font-size: 24px;
  font-weight: 700;
  color: var(--color-primary);
}

.stat-label {
  font-size: var(--text-xs);
  color: var(--color-text-secondary);
}

.graph-container {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border);
  padding: 40px;
  margin-bottom: 24px;
}

.graph-placeholder {
  text-align: center;
  color: var(--color-text-secondary);
}

.graph-placeholder .material-icons {
  font-size: 64px;
  color: var(--color-primary);
  margin-bottom: 16px;
}

.graph-placeholder p {
  font-size: var(--text-lg);
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 8px 0;
}

.sub-text {
  font-size: var(--text-sm);
  color: var(--color-text-hint);
  margin-bottom: 24px;
}

.mock-graph {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
}

.mock-node {
  padding: 12px 20px;
  border-radius: var(--radius-md);
  font-size: var(--text-sm);
  font-weight: 500;
}

.mock-node.entrance { background: var(--color-success-bg); color: var(--color-success); }
.mock-node.junction { background: var(--color-info-bg); color: var(--color-info); }
.mock-node.room { background: var(--color-primary-light); color: var(--color-primary); }

.mock-edge {
  width: 40px;
  height: 2px;
  background: var(--color-border);
}

.section-title {
  margin-bottom: 16px;
}

.section-title h2 {
  font-size: var(--text-lg);
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0;
}

.table-container {
  background: var(--color-bg);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border);
  overflow: hidden;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th {
  padding: 14px 16px;
  text-align: left;
  font-size: var(--text-xs);
  font-weight: 600;
  color: var(--color-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
}

.data-table td {
  padding: 14px 16px;
  border-bottom: 1px solid var(--color-border);
  font-size: var(--text-sm);
}

.data-table tr:last-child td {
  border-bottom: none;
}

.data-table tr:hover {
  background: var(--color-surface);
}

.data-table code {
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  background: var(--color-surface);
  padding: 4px 8px;
  border-radius: var(--radius-sm);
}

.type-badge {
  padding: 4px 10px;
  border-radius: var(--radius-full);
  font-size: var(--text-xs);
  font-weight: 600;
  text-transform: capitalize;
}

.type-room { background: var(--color-primary-light); color: var(--color-primary); }
.type-junction { background: var(--color-info-bg); color: var(--color-info); }
.type-entrance { background: var(--color-success-bg); color: var(--color-success); }
.type-exit { background: var(--color-danger-bg); color: var(--color-danger); }
.type-stairs { background: #FFF3E0; color: #E65100; }
.type-elevator { background: #E8EAF6; color: #3F51B5; }

.action-buttons {
  display: flex;
  gap: 8px;
}

.btn-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-icon:hover {
  background: var(--color-primary-light);
  color: var(--color-primary);
  border-color: var(--color-primary);
}

.btn-icon.btn-danger:hover {
  background: var(--color-danger-bg);
  color: var(--color-danger);
  border-color: var(--color-danger);
}

.btn-icon .material-icons {
  font-size: 16px;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-dialog {
  background: var(--color-bg);
  border-radius: var(--radius-lg);
  width: 100%;
  max-width: 480px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: var(--shadow-lg);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid var(--color-border);
}

.modal-header h2 {
  font-size: var(--text-lg);
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0;
}

.btn-close {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: transparent;
  border: none;
  border-radius: var(--radius-full);
  color: var(--color-text-hint);
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-close:hover {
  background: var(--color-surface);
  color: var(--color-text-primary);
}

.modal-body {
  padding: 24px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--color-text-secondary);
  margin-bottom: 6px;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 10px 12px;
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  font-family: var(--font-primary);
  font-size: var(--text-sm);
  color: var(--color-text-primary);
  outline: none;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 16px 24px;
  border-top: 1px solid var(--color-border);
  background: var(--color-surface);
  border-radius: 0 0 var(--radius-lg) var(--radius-lg);
}
</style>
