<template>
  <div class="adminaccounts-section">
    <!-- Header -->
    <div class="section-header">
      <div>
        <h1>Admin Accounts</h1>
        <p class="subtitle">Manage administrator accounts, roles, and permissions</p>
      </div>
      <button class="btn-primary" @click="showCreateModal = true">
        <span class="material-icons">person_add</span>
        Add Admin
      </button>
    </div>

    <!-- Stats Row -->
    <div class="stats-row">
      <div class="stat-box">
        <span class="stat-number">{{ admins.length }}</span>
        <span class="stat-label">Total Admins</span>
      </div>
      <div class="stat-box">
        <span class="stat-number">{{ admins.filter(a => a.is_active).length }}</span>
        <span class="stat-label">Active</span>
      </div>
      <div class="stat-box">
        <span class="stat-number">{{ admins.filter(a => !a.is_active).length }}</span>
        <span class="stat-label">Inactive</span>
      </div>
    </div>

    <!-- Filters -->
    <div class="filters-bar">
      <div class="search-box">
        <span class="material-icons">search</span>
        <input v-model="searchQuery" type="text" placeholder="Search by name, email, or role..." />
      </div>
      <select v-model="filterRole" class="filter-select">
        <option value="">All Roles</option>
        <option value="super_admin">Super Admin</option>
        <option value="dean">Dean</option>
        <option value="program_head">Program Head</option>
        <option value="basic_ed_head">Basic Ed Head</option>
      </select>
      <select v-model="filterStatus" class="filter-select">
        <option value="">All Status</option>
        <option value="active">Active</option>
        <option value="inactive">Inactive</option>
      </select>
    </div>

    <!-- Data Table -->
    <div class="table-container">
      <table class="data-table">
        <thead>
          <tr>
            <th>Admin</th>
            <th>Role</th>
            <th>Department</th>
            <th>Status</th>
            <th>Last Login</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="admin in filteredAdmins" :key="admin.id">
            <td>
              <div class="admin-info">
                <div class="admin-avatar">
                  <span class="material-icons">account_circle</span>
                </div>
                <div class="admin-details">
                  <div class="admin-name">{{ admin.display_name || admin.username }}</div>
                  <div class="admin-email">{{ admin.email }}</div>
                </div>
              </div>
            </td>
            <td>
              <span :class="['role-badge', 'role-' + admin.role]">{{ formatRole(admin.role) }}</span>
            </td>
            <td>{{ admin.department_label || 'N/A' }}</td>
            <td>
              <span :class="['status-indicator', admin.is_active ? 'status-active' : 'status-inactive']">
                <span class="status-dot"></span>
                {{ admin.is_active ? 'Active' : 'Inactive' }}
              </span>
            </td>
            <td>{{ admin.last_login ? formatDate(admin.last_login) : 'Never' }}</td>
            <td>
              <div class="action-buttons">
                <button class="btn-icon" @click="editAdmin(admin)" title="Edit">
                  <span class="material-icons">edit</span>
                </button>
                <button class="btn-icon" @click="toggleStatus(admin)" :title="admin.is_active ? 'Deactivate' : 'Activate'">
                  <span class="material-icons">{{ admin.is_active ? 'block' : 'check_circle' }}</span>
                </button>
                <button class="btn-icon btn-danger" @click="confirmDelete(admin)" title="Delete">
                  <span class="material-icons">delete</span>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-if="filteredAdmins.length === 0" class="empty-table">
        <span class="material-icons">search_off</span>
        <p>No admin accounts found matching your filters</p>
      </div>
    </div>

    <!-- Pagination -->
    <div class="pagination" v-if="filteredAdmins.length > 0">
      <span class="pagination-info">Showing {{ filteredAdmins.length }} of {{ admins.length }} admins</span>
    </div>

    <!-- Create/Edit Modal -->
    <div v-if="showCreateModal || showEditModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-dialog">
        <div class="modal-header">
          <h2>{{ showEditModal ? 'Edit Admin' : 'Create New Admin' }}</h2>
          <button class="btn-close" @click="closeModal">
            <span class="material-icons">close</span>
          </button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>Username</label>
            <input v-model="form.username" type="text" placeholder="Enter username" />
          </div>
          <div class="form-group">
            <label>Display Name</label>
            <input v-model="form.display_name" type="text" placeholder="Enter display name" />
          </div>
          <div class="form-group">
            <label>Email</label>
            <input v-model="form.email" type="email" placeholder="Enter email address" />
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Role</label>
              <select v-model="form.role">
                <option value="super_admin">Super Admin</option>
                <option value="dean">Dean</option>
                <option value="program_head">Program Head</option>
                <option value="basic_ed_head">Basic Ed Head</option>
              </select>
            </div>
            <div class="form-group">
              <label>Department</label>
              <select v-model="form.department">
                <option value="">Select Department</option>
                <option value="safety_security">Safety and Security Office</option>
                <option value="office_of_the_dean">Office of the Dean</option>
                <option value="college_agriculture">College of Agriculture and Fisheries</option>
                <option value="college_criminology">College of Criminal Justice Education</option>
                <option value="college_business">College of Business and Good Governance</option>
                <option value="college_ict">College of Information and Communication Technology</option>
                <option value="dept_civil_engineering">Department of Civil Engineering</option>
                <option value="college_teacher_education">College of Teacher Education</option>
                <option value="tesda">Technical Education and Skills Development Authority (TESDA)</option>
                <option value="general_education">General Education Department</option>
                <option value="basic_education">Basic Education Department</option>
              </select>
            </div>
          </div>
          <div class="form-group" v-if="!showEditModal">
            <label>Password</label>
            <input v-model="form.password" type="password" placeholder="Enter password" />
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-secondary" @click="closeModal">Cancel</button>
          <button class="btn-primary" @click="saveAdmin">
            {{ showEditModal ? 'Save Changes' : 'Create Admin' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="modal-overlay" @click.self="showDeleteModal = false">
      <div class="modal-dialog modal-sm">
        <div class="modal-header">
          <span class="material-icons modal-icon">warning</span>
          <h2>Delete Admin Account</h2>
        </div>
        <div class="modal-body">
          <p>Are you sure you want to delete <strong>{{ adminToDelete?.display_name || adminToDelete?.username }}</strong>?</p>
          <p class="text-muted">This action cannot be undone.</p>
        </div>
        <div class="modal-footer">
          <button class="btn-secondary" @click="showDeleteModal = false">Cancel</button>
          <button class="btn-danger" @click="deleteAdmin">Delete</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../../services/api.js'
import { showToast } from '../../services/toast.js'

const admins = ref([])
const searchQuery = ref('')
const filterRole = ref('')
const filterStatus = ref('')
const showCreateModal = ref(false)
const showEditModal = ref(false)
const showDeleteModal = ref(false)
const adminToDelete = ref(null)

const form = ref({
  id: null,
  username: '',
  display_name: '',
  email: '',
  role: 'program_head',
  department: '',
  password: ''
})

const filteredAdmins = computed(() => {
  return admins.value.filter(admin => {
    const matchesSearch = !searchQuery.value || 
      (admin.username?.toLowerCase().includes(searchQuery.value.toLowerCase())) ||
      (admin.display_name?.toLowerCase().includes(searchQuery.value.toLowerCase())) ||
      (admin.email?.toLowerCase().includes(searchQuery.value.toLowerCase()))
    
    const matchesRole = !filterRole.value || admin.role === filterRole.value
    const matchesStatus = !filterStatus.value || 
      (filterStatus.value === 'active' ? admin.is_active : !admin.is_active)
    
    return matchesSearch && matchesRole && matchesStatus
  })
})

function formatRole(role) {
  const labels = {
    'super_admin': 'Super Admin',
    'dean': 'Dean',
    'program_head': 'Program Head',
    'basic_ed_head': 'Basic Ed Head'
  }
  return labels[role] || role
}

function formatDate(date) {
  return new Date(date).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

function editAdmin(admin) {
  form.value = { ...admin, password: '' }
  showEditModal.value = true
}

function closeModal() {
  showCreateModal.value = false
  showEditModal.value = false
  form.value = { id: null, username: '', display_name: '', email: '', role: 'program_head', department: '', password: '' }
}

function confirmDelete(admin) {
  adminToDelete.value = admin
  showDeleteModal.value = true
}

async function loadAdmins() {
  try {
    const response = await api.get('/users/admins/')
    admins.value = response.data
  } catch (e) {
    console.error('Failed to load admins:', e)
    // Mock data for demonstration
    admins.value = [
      { id: 1, username: 'superadmin', display_name: 'Super Administrator', email: 'super@technopath.edu', role: 'super_admin', department: '', department_label: 'All Departments', is_active: true, last_login: new Date().toISOString() },
      { id: 2, username: 'dean_cs', display_name: 'Dr. Maria Santos', email: 'dean.cs@technopath.edu', role: 'dean', department: 'cs', department_label: 'Computer Science', is_active: true, last_login: new Date(Date.now() - 86400000).toISOString() },
      { id: 3, username: 'ph_it', display_name: 'Prof. Juan Cruz', email: 'ph.it@technopath.edu', role: 'program_head', department: 'it', department_label: 'Information Technology', is_active: true, last_login: new Date(Date.now() - 172800000).toISOString() },
      { id: 4, username: 'be_head', display_name: 'Mrs. Ana Reyes', email: 'be.head@technopath.edu', role: 'basic_ed_head', department: 'basic_ed', department_label: 'Basic Education', is_active: false, last_login: null }
    ]
  }
}

async function saveAdmin() {
  try {
    if (showEditModal.value) {
      await api.put(`/users/admins/${form.value.id}/`, form.value)
    } else {
      await api.post('/users/admins/', form.value)
    }
    closeModal()
    loadAdmins()
    showToast('Admin account saved successfully', 'success')
  } catch (e) {
    console.error('Failed to save admin:', e)
    const msg = e.response?.data?.error || 'Failed to save admin account'
    showToast(msg, 'error')
  }
}

async function toggleStatus(admin) {
  if (admin.is_active) {
    // Deactivate via DELETE (soft-delete)
    try {
      await api.delete(`/users/admins/${admin.id}/`)
      admin.is_active = false
      showToast(`${admin.display_name || admin.username} deactivated`, 'success')
    } catch (e) {
      const msg = e.response?.data?.error || 'Failed to deactivate'
      showToast(msg, 'error')
    }
  } else {
    // Reactivate via PUT
    try {
      await api.put(`/users/admins/${admin.id}/`, { ...admin, is_active: true })
      admin.is_active = true
      showToast(`${admin.display_name || admin.username} reactivated`, 'success')
    } catch (e) {
      const msg = e.response?.data?.error || 'Failed to reactivate'
      showToast(msg, 'error')
    }
  }
}

async function deleteAdmin() {
  try {
    await api.delete(`/users/admins/${adminToDelete.value.id}/`)
    showDeleteModal.value = false
    loadAdmins()
  } catch (e) {
    console.error('Failed to delete admin:', e)
  }
}

onMounted(loadAdmins)
</script>

<style scoped>
.adminaccounts-section { padding: 0; font-family: var(--font-primary); max-width: 1400px; }

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

.btn-primary {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: var(--color-primary);
  color: white;
  border: none;
  border-radius: var(--radius-md);
  font-family: var(--font-primary);
  font-size: var(--text-sm);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary:hover {
  background: var(--color-primary-dark);
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(255, 152, 0, 0.3);
}

.btn-primary .material-icons {
  font-size: 20px;
}

.stats-row {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
}

.stat-box {
  display: flex;
  flex-direction: column;
  padding: 16px 24px;
  background: var(--color-bg);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border);
  min-width: 120px;
}

.stat-number {
  font-size: 28px;
  font-weight: 700;
  color: var(--color-primary);
}

.stat-label {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
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

.filter-select {
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
  padding: 16px;
  border-bottom: 1px solid var(--color-border);
  font-size: var(--text-sm);
}

.data-table tr:last-child td {
  border-bottom: none;
}

.data-table tr:hover {
  background: var(--color-surface);
}

.admin-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.admin-avatar {
  width: 40px;
  height: 40px;
  background: var(--color-primary-light);
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
}

.admin-avatar .material-icons {
  font-size: 24px;
  color: var(--color-primary);
}

.admin-details {
  display: flex;
  flex-direction: column;
}

.admin-name {
  font-weight: 600;
  color: var(--color-text-primary);
}

.admin-email {
  font-size: var(--text-xs);
  color: var(--color-text-secondary);
}

.role-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: var(--radius-full);
  font-size: var(--text-xs);
  font-weight: 600;
}

.role-super_admin { background: #FFEBEE; color: #B71C1C; }
.role-dean { background: #E3F2FD; color: #1565C0; }
.role-program_head { background: #E8F5E9; color: #2E7D32; }
.role-basic_ed_head { background: #FFF3E0; color: #E65100; }

.status-indicator {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: var(--text-sm);
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: var(--radius-full);
}

.status-active .status-dot { background: var(--color-success); }
.status-active { color: var(--color-success); }
.status-inactive .status-dot { background: var(--color-text-hint); }
.status-inactive { color: var(--color-text-hint); }

.action-buttons {
  display: flex;
  gap: 8px;
}

.btn-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
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
  font-size: 18px;
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
  justify-content: flex-end;
  padding: 16px;
  border-top: 1px solid var(--color-border);
}

.pagination-info {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
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

.modal-dialog.modal-sm {
  max-width: 400px;
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

.modal-icon {
  font-size: 32px;
  color: var(--color-warning);
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
  padding: 12px 14px;
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  font-family: var(--font-primary);
  font-size: var(--text-sm);
  color: var(--color-text-primary);
  outline: none;
  transition: border-color 0.2s ease;
}

.form-group input:focus,
.form-group select:focus {
  border-color: var(--color-primary);
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

.btn-secondary {
  padding: 10px 20px;
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  color: var(--color-text-primary);
  font-family: var(--font-primary);
  font-size: var(--text-sm);
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-secondary:hover {
  background: var(--color-surface);
}

.btn-danger {
  padding: 10px 20px;
  background: var(--color-danger);
  border: none;
  border-radius: var(--radius-md);
  color: white;
  font-family: var(--font-primary);
  font-size: var(--text-sm);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-danger:hover {
  background: #B71C1C;
}

.text-muted {
  font-size: var(--text-sm);
  color: var(--color-text-hint);
  margin-top: 8px;
}
</style>
