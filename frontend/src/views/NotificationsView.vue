<template>
  <div class="notifications-view">
    <header class="notifications-top-bar">
      <button class="notifications-back-btn" @click="goBack">
        <span class="material-icons">arrow_back</span>
      </button>
      <div class="notifications-header-title">
        <h1>Notifications</h1>
      </div>
      <button class="notifications-read-btn" @click="markAllAsRead" v-if="notifications.length > 0" title="Mark all as read">
        <span class="material-icons">done_all</span>
      </button>
      <div v-else class="notifications-spacer"></div>
    </header>

    <div class="notifications-main-content">
      <div class="notifications-list">
        <div v-if="notifications.length === 0" class="notifications-empty-state">
          <div class="notifications-empty-icon">
            <span class="material-icons">notifications_off</span>
          </div>
          <h2>All caught up!</h2>
          <p>You have no new notifications.</p>
        </div>
        
        <div v-for="notif in notifications" :key="notif.id" 
             :class="['notifications-card', notif.type, { 'notifications-unread': !notif.is_read }]">
          <div class="notifications-card-header">
            <span v-if="notif.source_label"
                  :class="['source-chip', 'chip-' + (notif.source_color || 'orange')]">
              {{ notif.source_label }}
            </span>
            <span class="notifications-badge" :class="notif.type">{{ notif.type }}</span>
            <span class="notifications-time">{{ formatTime(notif.created_at) }}</span>
          </div>
          <h3>{{ notif.title }}</h3>
          <p>{{ notif.message }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import db from '../services/db.js'
import api from '../services/api.js'
import { isOnline } from '../services/sync.js'
import { showToast } from '../services/toast.js'

const router = useRouter()
const notifications = ref([])

const goBack = () => router.back()

onMounted(async () => {
  try {
    // If online, sync from API first to get latest notifications
    if (isOnline()) {
      try {
        const res = await api.get('/notifications/')
        notifications.value = res.data
        // Save to IndexedDB for offline use
        await db.notifications.clear()
        await db.notifications.bulkPut(res.data)
      } catch (apiError) {
        console.warn('Failed to sync notifications from API:', apiError)
        // Fall back to IndexedDB
        notifications.value = await db.notifications
          .orderBy('created_at')
          .reverse()
          .toArray()
      }
    } else {
      // Offline: load from IndexedDB only
      notifications.value = await db.notifications
        .orderBy('created_at')
        .reverse()
        .toArray()
    }
  } catch (dbError) {
    console.error('Failed to load notifications:', dbError)
    showToast('Unable to load notifications', 'error')
  }
})

function formatTime(timestamp) {
  if (!timestamp) return ''
  const date = new Date(timestamp)
  return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

async function markAllAsRead() {
  let hasUnread = false
  for (const notif of notifications.value) {
    if (!notif.is_read) {
      notif.is_read = true
      hasUnread = true
      await db.notifications.update(notif.id, { is_read: true })
    }
  }

  if (hasUnread) {
    if (isOnline()) {
      try {
        await api.post('/notifications/read-all/')
      } catch (e) {
        console.warn('Failed to sync read status:', e)
      }
    } else {
      showToast('Offline: Read status saved locally', 'info')
    }
  }
}
</script>

<style>
/* Styles moved to external file: src/assets/notifications.css */
@import '../assets/notifications.css';

.source-chip {
  display: inline-block;
  font-size: var(--text-xs);
  font-family: var(--font-primary);
  font-weight: 600;
  padding: 2px 8px;
  border-radius: var(--radius-full);
  margin-bottom: 4px;
}
.chip-red        { background: #FFEBEE; color: #B71C1C; }
.chip-dark_blue  { background: #E8EAF6; color: #1A237E; }
.chip-green      { background: #E8F5E9; color: #1B5E20; }
.chip-charcoal   { background: #ECEFF1; color: #263238; }
.chip-purple     { background: #F3E5F5; color: #4A148C; }
.chip-teal       { background: #E0F2F1; color: #004D40; }
.chip-amber      { background: #FFF8E1; color: #E65100; }
.chip-blue       { background: #E3F2FD; color: #0D47A1; }
.chip-dark_green { background: #E8F5E9; color: #33691E; }
.chip-indigo     { background: #E8EAF6; color: #283593; }
.chip-brown      { background: #EFEBE9; color: #4E342E; }
.chip-orange     { background: #FFF3E0; color: #E65100; }
</style>
