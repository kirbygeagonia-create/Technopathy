<template>
  <div class="adminfaq-section">
    <!-- Header -->
    <div class="section-header">
      <div>
        <h1>FAQ / Chatbot Management</h1>
        <p class="subtitle">Manage chatbot knowledge base and FAQ entries</p>
      </div>
      <button class="btn-primary" @click="showCreateModal = true">
        <span class="material-icons">add</span>
        Add FAQ
      </button>
    </div>

    <!-- Stats -->
    <div class="stats-row">
      <div class="stat-box">
        <span class="stat-number">{{ faqs.length }}</span>
        <span class="stat-label">Total FAQs</span>
      </div>
      <div class="stat-box">
        <span class="stat-number">{{ categories.length }}</span>
        <span class="stat-label">Categories</span>
      </div>
      <div class="stat-box">
        <span class="stat-number">{{ faqs.filter(f => f.is_active).length }}</span>
        <span class="stat-label">Active</span>
      </div>
    </div>

    <!-- Category Filter -->
    <div class="category-filter">
      <button 
        :class="['category-btn', { active: selectedCategory === '' }]"
        @click="selectedCategory = ''"
      >
        All
      </button>
      <button 
        v-for="cat in categories" 
        :key="cat"
        :class="['category-btn', { active: selectedCategory === cat }]"
        @click="selectedCategory = cat"
      >
        {{ cat }}
      </button>
    </div>

    <!-- Search -->
    <div class="search-bar">
      <span class="material-icons">search</span>
      <input v-model="searchQuery" type="text" placeholder="Search questions or answers..." />
    </div>

    <!-- FAQ List -->
    <div class="faq-list">
      <div v-for="faq in filteredFaqs" :key="faq.id" class="faq-card">
        <div class="faq-header">
          <span class="category-tag">{{ faq.category }}</span>
          <div class="faq-actions">
            <button class="btn-icon" @click="toggleActive(faq)" :title="faq.is_active ? 'Deactivate' : 'Activate'">
              <span class="material-icons">{{ faq.is_active ? 'visibility' : 'visibility_off' }}</span>
            </button>
            <button class="btn-icon" @click="editFaq(faq)" title="Edit">
              <span class="material-icons">edit</span>
            </button>
            <button class="btn-icon btn-danger" @click="confirmDelete(faq)" title="Delete">
              <span class="material-icons">delete</span>
            </button>
          </div>
        </div>
        <div class="faq-content">
          <h3 class="faq-question">{{ faq.question }}</h3>
          <p class="faq-answer">{{ faq.answer }}</p>
        </div>
        <div class="faq-footer">
          <span :class="['status-badge', faq.is_active ? 'status-active' : 'status-inactive']">
            {{ faq.is_active ? 'Active' : 'Inactive' }}
          </span>
          <span class="updated-at">Updated {{ formatDate(faq.updated_at) }}</span>
        </div>
      </div>
    </div>

    <div v-if="filteredFaqs.length === 0" class="empty-state">
      <span class="material-icons">help_outline</span>
      <p>No FAQs found</p>
    </div>

    <!-- Create/Edit Modal -->
    <div v-if="showCreateModal || showEditModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-dialog">
        <div class="modal-header">
          <h2>{{ showEditModal ? 'Edit FAQ' : 'Add New FAQ' }}</h2>
          <button class="btn-close" @click="closeModal">
            <span class="material-icons">close</span>
          </button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>Category</label>
            <select v-model="form.category">
              <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
              <option value="_new">+ Add New Category</option>
            </select>
            <input v-if="form.category === '_new'" v-model="newCategory" type="text" placeholder="Enter new category name" class="new-category-input" />
          </div>
          <div class="form-group">
            <label>Question</label>
            <input v-model="form.question" type="text" placeholder="Enter the question" />
          </div>
          <div class="form-group">
            <label>Answer</label>
            <textarea v-model="form.answer" rows="5" placeholder="Enter the answer"></textarea>
          </div>
          <div class="form-group checkbox-group">
            <label class="checkbox-label">
              <input v-model="form.is_active" type="checkbox" />
              <span>Active (visible to users)</span>
            </label>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-secondary" @click="closeModal">Cancel</button>
          <button class="btn-primary" @click="saveFaq">
            {{ showEditModal ? 'Save Changes' : 'Create FAQ' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation -->
    <div v-if="showDeleteModal" class="modal-overlay" @click.self="showDeleteModal = false">
      <div class="modal-dialog modal-sm">
        <div class="modal-header">
          <span class="material-icons modal-icon">warning</span>
          <h2>Delete FAQ</h2>
        </div>
        <div class="modal-body">
          <p>Are you sure you want to delete this FAQ?</p>
          <p class="text-muted">"{{ faqToDelete?.question }}"</p>
        </div>
        <div class="modal-footer">
          <button class="btn-secondary" @click="showDeleteModal = false">Cancel</button>
          <button class="btn-danger" @click="deleteFaq">Delete</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../../services/api.js'
import { showToast } from '../../services/toast.js'

const faqs = ref([])
const searchQuery = ref('')
const selectedCategory = ref('')
const showCreateModal = ref(false)
const showEditModal = ref(false)
const showDeleteModal = ref(false)
const faqToDelete = ref(null)
const newCategory = ref('')

const form = ref({
  id: null,
  category: '',
  question: '',
  answer: '',
  is_active: true
})

const categories = computed(() => {
  const cats = [...new Set(faqs.value.map(f => f.category))]
  return cats.sort()
})

const filteredFaqs = computed(() => {
  return faqs.value.filter(faq => {
    const matchesCategory = !selectedCategory.value || faq.category === selectedCategory.value
    const matchesSearch = !searchQuery.value ||
      faq.question.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      faq.answer.toLowerCase().includes(searchQuery.value.toLowerCase())
    return matchesCategory && matchesSearch
  })
})

function formatDate(date) {
  return new Date(date).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

function editFaq(faq) {
  form.value = { ...faq }
  showEditModal.value = true
}

function closeModal() {
  showCreateModal.value = false
  showEditModal.value = false
  newCategory.value = ''
  form.value = { id: null, category: categories.value[0] || '', question: '', answer: '', is_active: true }
}

function confirmDelete(faq) {
  faqToDelete.value = faq
  showDeleteModal.value = true
}

async function loadFaqs() {
  try {
    const response = await api.get('/faq/')
    faqs.value = response.data
  } catch (e) {
    console.error('Failed to load FAQs:', e)
    // Mock data
    faqs.value = [
      { id: 1, category: 'General', question: 'What are the campus operating hours?', answer: 'The campus is open from 6:00 AM to 9:00 PM on weekdays, and 7:00 AM to 6:00 PM on weekends.', is_active: true, updated_at: new Date().toISOString() },
      { id: 2, category: 'General', question: 'Where can I find the registrar\'s office?', answer: 'The registrar\'s office is located on the 2nd floor of the Administration Building, Room 201.', is_active: true, updated_at: new Date(Date.now() - 86400000).toISOString() },
      { id: 3, category: 'Facilities', question: 'How do I book a meeting room?', answer: 'You can book meeting rooms through the student portal or by visiting the facilities office in the Main Building.', is_active: true, updated_at: new Date(Date.now() - 172800000).toISOString() },
      { id: 4, category: 'Navigation', question: 'Where is the library?', answer: 'The University Library is located in Building C, accessible from the main campus entrance.', is_active: true, updated_at: new Date(Date.now() - 259200000).toISOString() },
      { id: 5, category: 'IT Support', question: 'How do I connect to campus WiFi?', answer: 'Connect to "CampusNet" network using your student ID as username and your password.', is_active: false, updated_at: new Date(Date.now() - 345600000).toISOString() }
    ]
  }
}

async function saveFaq() {
  try {
    const category = form.value.category === '_new' ? newCategory.value : form.value.category
    const data = { ...form.value, category }
    
    if (showEditModal.value) {
      await api.put(`/faq/${form.value.id}/`, data)
    } else {
      await api.post('/faq/', data)
    }
    closeModal()
    loadFaqs()
  } catch (e) {
    console.error('Failed to save FAQ:', e)
    showToast('Failed to save FAQ', 'error')
  }
}

async function toggleActive(faq) {
  try {
    await api.patch(`/faq/${faq.id}/`, { is_active: !faq.is_active })
    faq.is_active = !faq.is_active
  } catch (e) {
    console.error('Failed to toggle status:', e)
  }
}

async function deleteFaq() {
  try {
    await api.delete(`/faq/${faqToDelete.value.id}/`)
    showDeleteModal.value = false
    loadFaqs()
  } catch (e) {
    console.error('Failed to delete FAQ:', e)
  }
}

onMounted(loadFaqs)
</script>

<style scoped>
.adminfaq-section { padding: 0; font-family: var(--font-primary); max-width: 1400px; }

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

.category-filter {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
}

.category-btn {
  padding: 8px 16px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-full);
  color: var(--color-text-secondary);
  font-family: var(--font-primary);
  font-size: var(--text-sm);
  cursor: pointer;
  transition: all 0.2s ease;
}

.category-btn:hover {
  background: var(--color-primary-light);
  border-color: var(--color-primary);
  color: var(--color-primary);
}

.category-btn.active {
  background: var(--color-primary);
  border-color: var(--color-primary);
  color: white;
}

.search-bar {
  display: flex;
  align-items: center;
  gap: 10px;
  max-width: 500px;
  padding: 12px 16px;
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  margin-bottom: 20px;
}

.search-bar .material-icons {
  font-size: 20px;
  color: var(--color-text-hint);
}

.search-bar input {
  flex: 1;
  border: none;
  background: transparent;
  font-family: var(--font-primary);
  font-size: var(--text-base);
  color: var(--color-text-primary);
  outline: none;
}

.faq-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.faq-card {
  background: var(--color-bg);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border);
  padding: 20px;
  transition: all 0.2s ease;
}

.faq-card:hover {
  box-shadow: var(--shadow-sm);
}

.faq-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.category-tag {
  padding: 4px 12px;
  background: var(--color-primary-light);
  border-radius: var(--radius-full);
  font-size: var(--text-xs);
  font-weight: 600;
  color: var(--color-primary);
}

.faq-actions {
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

.faq-question {
  font-size: var(--text-base);
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 8px 0;
}

.faq-answer {
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  line-height: 1.5;
  margin: 0;
}

.faq-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 16px;
  padding-top: 12px;
  border-top: 1px solid var(--color-border);
}

.status-badge {
  padding: 4px 10px;
  border-radius: var(--radius-full);
  font-size: var(--text-xs);
  font-weight: 600;
}

.status-active { background: var(--color-success-bg); color: var(--color-success); }
.status-inactive { background: var(--color-surface-2); color: var(--color-text-hint); }

.updated-at {
  font-size: var(--text-xs);
  color: var(--color-text-hint);
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 60px 20px;
  color: var(--color-text-hint);
}

.empty-state .material-icons {
  font-size: 48px;
  margin-bottom: 12px;
  opacity: 0.5;
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
  max-width: 560px;
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
.form-group select,
.form-group textarea {
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
.form-group select:focus,
.form-group textarea:focus {
  border-color: var(--color-primary);
}

.new-category-input {
  margin-top: 8px;
}

.checkbox-group {
  display: flex;
  align-items: center;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
}

.checkbox-label input[type="checkbox"] {
  width: 18px;
  height: 18px;
  accent-color: var(--color-primary);
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
  font-size: var(--text-base);
  color: var(--color-text-secondary);
  margin-top: 8px;
}
</style>
