<template>
  <div class="adminannouncements-section">
    <h1>Announcements</h1>
    
    <div class="adminannouncements-form" v-if="auth.canPostAnnouncement">
      <h2>{{ willPublishDirectly ? 'Publish Announcement' : 'Submit for Approval' }}</h2>
      <input v-model="newTitle" placeholder="Title" class="tp-input" />
      <textarea v-model="newContent" placeholder="Content" class="tp-textarea" rows="4"></textarea>
      <select v-model="newScope" class="tp-select">
        <option value="campus_wide">Entire Campus</option>
        <option value="all_college">All College Students</option>
        <option value="basic_ed_only">Basic Education Only</option>
        <option value="department">My Department Only</option>
      </select>
      <button @click="submitAnnouncement" class="adminannouncements-btn-primary">
        {{ willPublishDirectly ? 'Publish Now' : 'Submit for Approval' }}
      </button>
      <p v-if="!willPublishDirectly" class="tp-info">
        This will be submitted to the {{ auth.user?.role === 'dean' ? 'Super Admin' : (auth.user?.role === 'program_head' ? 'Dean or Super Admin' : 'Super Admin') }} for approval before it goes live.
      </p>
    </div>

    <h2>My Announcements</h2>
    <div v-if="myAnnouncements.length === 0" class="tp-empty">No announcements yet.</div>
    <div v-for="a in myAnnouncements" :key="a.id" class="adminannouncements-card">
      <span :class="['adminannouncements-status-badge', 'adminannouncements-status-' + a.status]">{{ formatStatus(a.status) }}</span>
      <h3>{{ a.title }}</h3>
      <p>{{ a.content }}</p>
      <p v-if="a.rejection_note" class="adminannouncements-rejection-note">Rejected: {{ a.rejection_note }}</p>
      <small>{{ formatTime(a.created_at) }}</small>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '../../stores/authStore.js'
import api from '../../services/api.js'
import { showToast } from '../../services/toast.js'

const auth = useAuthStore()
const emit = defineEmits(['my-pending'])

const newTitle = ref('')
const newContent = ref('')
const newScope = ref('campus_wide')
const myAnnouncements = ref([])

const willPublishDirectly = computed(() => {
  if (auth.user?.role === 'super_admin') return true
  if (auth.user?.role === 'dean' && newScope.value === 'department') return true
  return false
})

function formatStatus(status) {
  const labels = {
    'pending_approval': 'Awaiting Approval',
    'published': 'Published',
    'rejected': 'Rejected',
    'archived': 'Archived'
  }
  return labels[status] || status
}

function formatTime(ts) {
  if (!ts) return ''
  return new Date(ts).toLocaleString()
}

async function loadMyAnnouncements() {
  try {
    const r = await api.get('/announcements/mine/')
    myAnnouncements.value = r.data
    const pending = r.data.filter(a => a.status === 'pending_approval').length
    emit('my-pending', pending)
  } catch (e) {
    console.error('Failed to load announcements:', e)
  }
}

async function submitAnnouncement() {
  if (!newTitle.value || !newContent.value) return
  try {
    await api.post('/announcements/create/', {
      title: newTitle.value,
      content: newContent.value,
      scope: newScope.value
    })
    newTitle.value = ''
    newContent.value = ''
    newScope.value = 'campus_wide'
    await loadMyAnnouncements()
  } catch (e) {
    console.error('Failed to submit:', e)
    showToast('Failed to submit announcement', 'error')
  }
}

onMounted(loadMyAnnouncements)
</script>

<style scoped>
.adminannouncements-section { padding: 20px; font-family: var(--font-primary); }
.adminannouncements-form { background: var(--color-surface); padding: 20px; border-radius: var(--radius-md); margin-bottom: 24px; }
.adminannouncements-form h2 { margin-bottom: 16px; }
.tp-input, .tp-textarea, .tp-select { 
  display: block; width: 100%; margin-bottom: 12px; padding: 10px; 
  border: 1px solid var(--color-border); border-radius: var(--radius-sm);
  font-family: var(--font-primary); font-size: var(--text-base);
}
.adminannouncements-btn-primary { 
  background: var(--color-primary); color: white; border: none; 
  padding: 12px 24px; border-radius: var(--radius-md); cursor: pointer;
  font-family: var(--font-primary); font-size: var(--text-base); min-height: 44px;
}
.adminannouncements-btn-primary:hover { background: var(--color-primary-dark); }
.tp-info { color: var(--color-text-secondary); font-size: var(--text-sm); margin-top: 8px; }
.tp-empty { color: var(--color-text-hint); padding: 20px; text-align: center; }
.adminannouncements-card { 
  background: var(--color-bg); border: 1px solid var(--color-border); 
  padding: 16px; border-radius: var(--radius-md); margin-bottom: 12px; 
}
.adminannouncements-card h3 { margin-bottom: 8px; }
.adminannouncements-status-badge { 
  display: inline-block; padding: 2px 8px; border-radius: var(--radius-full); 
  font-size: var(--text-xs); font-weight: 600; margin-bottom: 8px;
}
.adminannouncements-status-pending_approval { background: #FFF8E1; color: #E65100; }
.adminannouncements-status-published { background: #E8F5E9; color: #1B5E20; }
.adminannouncements-status-rejected { background: #FFEBEE; color: #B71C1C; }
.adminannouncements-status-archived { background: #ECEFF1; color: #263238; }
.adminannouncements-rejection-note { background: #FFEBEE; padding: 8px; border-radius: var(--radius-sm); color: #B71C1C; margin-top: 8px; }
</style>
