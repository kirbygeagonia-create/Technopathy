<template>
  <div class="adminauditlog-section">
    <!-- Header -->
    <div class="section-header">
      <div>
        <h1>Audit Log</h1>
        <p class="subtitle">Track system activities and administrative actions</p>
      </div>
      <button class="btn-export" @click="exportLogs">
        <span class="material-icons">download</span>
        Export
      </button>
    </div>

    <!-- Filters -->
    <div class="filters-bar">
      <div class="search-box">
        <span class="material-icons">search</span>
        <input v-model="searchQuery" type="text" placeholder="Search actions, users, or details..." />
      </div>
      <select v-model="filterAction" class="filter-select">
        <option value="">All Actions</option>
        <option value="create">Create</option>
        <option value="update">Update</option>
        <option value="delete">Delete</option>
        <option value="login">Login</option>
        <option value="logout">Logout</option>
        <option value="approve">Approve</option>
        <option value="reject">Reject</option>
      </select>
      <select v-model="filterUser" class="filter-select">
        <option value="">All Users</option>
        <option v-for="user in uniqueUsers" :key="user" :value="user">{{ user }}</option>
      </select>
      <input v-model="filterDate" type="date" class="filter-date" />
    </div>

    <!-- Stats -->
    <div class="stats-row">
      <div class="stat-box">
        <span class="stat-number">{{ filteredLogs.length }}</span>
        <span class="stat-label">Total Entries</span>
      </div>
      <div class="stat-box">
        <span class="stat-number">{{ todayLogs.length }}</span>
        <span class="stat-label">Today</span>
      </div>
      <div class="stat-box">
        <span class="stat-number">{{ uniqueUsers.length }}</span>
        <span class="stat-label">Active Users</span>
      </div>
    </div>

    <!-- Audit Log Table -->
    <div class="table-container">
      <table class="data-table">
        <thead>
          <tr>
            <th>Timestamp</th>
            <th>User</th>
            <th>Action</th>
            <th>Target</th>
            <th>Details</th>
            <th>IP Address</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="log in filteredLogs" :key="log.id">
            <td>
              <div class="timestamp">
                <span class="date">{{ formatDate(log.timestamp) }}</span>
                <span class="time">{{ formatTime(log.timestamp) }}</span>
              </div>
            </td>
            <td>
              <div class="user-cell">
                <span class="material-icons user-icon">account_circle</span>
                <span>{{ log.user }}</span>
              </div>
            </td>
            <td>
              <span :class="['action-badge', 'action-' + log.action_type]">
                <span class="material-icons">{{ getActionIcon(log.action_type) }}</span>
                {{ formatAction(log.action_type) }}
              </span>
            </td>
            <td>{{ log.target_type }}</td>
            <td class="details-cell">{{ log.details }}</td>
            <td class="ip-cell">{{ log.ip_address }}</td>
          </tr>
        </tbody>
      </table>
      <div v-if="filteredLogs.length === 0" class="empty-table">
        <span class="material-icons">search_off</span>
        <p>No audit logs found matching your filters</p>
      </div>
    </div>

    <!-- Pagination -->
    <div class="pagination">
      <button class="btn-page" :disabled="currentPage === 1" @click="currentPage--">
        <span class="material-icons">chevron_left</span>
      </button>
      <span class="page-info">Page {{ currentPage }} of {{ totalPages }}</span>
      <button class="btn-page" :disabled="currentPage >= totalPages" @click="currentPage++">
        <span class="material-icons">chevron_right</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../../services/api.js'

const logs = ref([])
const searchQuery = ref('')
const filterAction = ref('')
const filterUser = ref('')
const filterDate = ref('')
const currentPage = ref(1)
const itemsPerPage = 20

const uniqueUsers = computed(() => {
  const users = [...new Set(logs.value.map(l => l.user))]
  return users.sort()
})

const todayLogs = computed(() => {
  const today = new Date().toDateString()
  return logs.value.filter(l => new Date(l.timestamp).toDateString() === today)
})

const filteredLogs = computed(() => {
  let filtered = logs.value

  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    filtered = filtered.filter(l => 
      l.user.toLowerCase().includes(q) ||
      l.details.toLowerCase().includes(q) ||
      l.target_type.toLowerCase().includes(q)
    )
  }

  if (filterAction.value) {
    filtered = filtered.filter(l => l.action_type === filterAction.value)
  }

  if (filterUser.value) {
    filtered = filtered.filter(l => l.user === filterUser.value)
  }

  if (filterDate.value) {
    const date = new Date(filterDate.value).toDateString()
    filtered = filtered.filter(l => new Date(l.timestamp).toDateString() === date)
  }

  // Pagination
  const start = (currentPage.value - 1) * itemsPerPage
  return filtered.slice(start, start + itemsPerPage)
})

const totalPages = computed(() => {
  return Math.ceil(logs.value.length / itemsPerPage)
})

function formatDate(timestamp) {
  return new Date(timestamp).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

function formatTime(timestamp) {
  return new Date(timestamp).toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

function formatAction(action) {
  const labels = {
    'create': 'Created',
    'update': 'Updated',
    'delete': 'Deleted',
    'login': 'Logged In',
    'logout': 'Logged Out',
    'approve': 'Approved',
    'reject': 'Rejected'
  }
  return labels[action] || action
}

function getActionIcon(action) {
  const icons = {
    'create': 'add_circle',
    'update': 'edit',
    'delete': 'delete',
    'login': 'login',
    'logout': 'logout',
    'approve': 'check_circle',
    'reject': 'cancel'
  }
  return icons[action] || 'info'
}

function exportLogs() {
  const csv = [
    ['Timestamp', 'User', 'Action', 'Target', 'Details', 'IP Address'],
    ...filteredLogs.value.map(l => [
      new Date(l.timestamp).toISOString(),
      l.user,
      l.action_type,
      l.target_type,
      l.details,
      l.ip_address
    ])
  ].map(row => row.join(',')).join('\n')

  const blob = new Blob([csv], { type: 'text/csv' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `audit-log-${new Date().toISOString().split('T')[0]}.csv`
  a.click()
  URL.revokeObjectURL(url)
}

async function loadLogs() {
  try {
    const response = await api.get('/audit-log/')
    logs.value = response.data
  } catch (e) {
    console.error('Failed to load audit logs:', e)
    // Mock data for demonstration
    logs.value = [
      { id: 1, timestamp: new Date().toISOString(), user: 'superadmin', action_type: 'login', target_type: 'System', details: 'User logged in successfully', ip_address: '192.168.1.100' },
      { id: 2, timestamp: new Date(Date.now() - 3600000).toISOString(), user: 'dean_cs', action_type: 'approve', target_type: 'Announcement', details: 'Approved announcement: "Campus Orientation 2024"', ip_address: '192.168.1.101' },
      { id: 3, timestamp: new Date(Date.now() - 7200000).toISOString(), user: 'ph_it', action_type: 'create', target_type: 'Room', details: 'Created room: "IT Lab 3"', ip_address: '192.168.1.102' },
      { id: 4, timestamp: new Date(Date.now() - 10800000).toISOString(), user: 'superadmin', action_type: 'update', target_type: 'Admin Account', details: 'Updated permissions for: dean_cs', ip_address: '192.168.1.100' },
      { id: 5, timestamp: new Date(Date.now() - 14400000).toISOString(), user: 'be_head', action_type: 'logout', target_type: 'System', details: 'User logged out', ip_address: '192.168.1.103' },
    ]
  }
}

onMounted(loadLogs)
</script>

<style scoped>
.adminauditlog-section { padding: 0; font-family: var(--font-primary); max-width: 1400px; }

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

.btn-export {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  color: var(--color-text-primary);
  font-family: var(--font-primary);
  font-size: var(--text-sm);
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-export:hover {
  background: var(--color-primary-light);
  border-color: var(--color-primary);
  color: var(--color-primary);
}

.filters-bar {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.search-box {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1;
  min-width: 280px;
  padding: 10px 14px;
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
}

.search-box .material-icons {
  font-size: 20px;
  color: var(--color-text-hint);
}

.search-box input {
  flex: 1;
  border: none;
  background: transparent;
  font-family: var(--font-primary);
  font-size: var(--text-sm);
  color: var(--color-text-primary);
  outline: none;
}

.filter-select, .filter-date {
  padding: 10px 14px;
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  font-family: var(--font-primary);
  font-size: var(--text-sm);
  color: var(--color-text-primary);
  min-width: 140px;
  cursor: pointer;
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

.timestamp {
  display: flex;
  flex-direction: column;
}

.timestamp .date {
  font-weight: 500;
  color: var(--color-text-primary);
}

.timestamp .time {
  font-size: var(--text-xs);
  color: var(--color-text-hint);
}

.user-cell {
  display: flex;
  align-items: center;
  gap: 8px;
}

.user-icon {
  font-size: 20px;
  color: var(--color-text-hint);
}

.action-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: var(--radius-full);
  font-size: var(--text-xs);
  font-weight: 600;
}

.action-badge .material-icons {
  font-size: 14px;
}

.action-create { background: var(--color-success-bg); color: var(--color-success); }
.action-update { background: var(--color-info-bg); color: var(--color-info); }
.action-delete { background: var(--color-danger-bg); color: var(--color-danger); }
.action-login { background: var(--color-success-bg); color: var(--color-success); }
.action-logout { background: var(--color-surface-2); color: var(--color-text-secondary); }
.action-approve { background: var(--color-success-bg); color: var(--color-success); }
.action-reject { background: var(--color-danger-bg); color: var(--color-danger); }

.details-cell {
  max-width: 300px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.ip-cell {
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  color: var(--color-text-hint);
}

.empty-table {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 60px 20px;
  color: var(--color-text-hint);
}

.empty-table .material-icons {
  font-size: 48px;
  margin-bottom: 12px;
  opacity: 0.5;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  padding: 20px;
  border-top: 1px solid var(--color-border);
}

.btn-page {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  color: var(--color-text-primary);
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-page:hover:not(:disabled) {
  background: var(--color-primary-light);
  border-color: var(--color-primary);
  color: var(--color-primary);
}

.btn-page:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
}
</style>
