<template>
  <div v-if="show" class="offline-banner" :class="{ 'offline': !isOnline, 'stale': isOnline && isStale }">
    <span class="material-icons offline-icon">
      {{ !isOnline ? 'wifi_off' : 'update' }}
    </span>
    <span class="offline-text">
      {{ message }}
    </span>
    <button v-if="!isOnline" class="offline-dismiss" @click="dismiss">
      <span class="material-icons">close</span>
    </button>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { isOnline, registerConnectivityListener } from '../services/sync.js'
import { getOfflineStatus } from '../services/offlineData.js'

const show = ref(true)
const onlineStatus = ref(isOnline())
const statusDetails = ref(null)
let unsubscribe = null

const isStale = computed(() => statusDetails.value?.stale || false)

const message = computed(() => {
  if (!onlineStatus.value) {
    if (statusDetails.value?.lastSync) {
      const time = new Date(statusDetails.value.lastSync).toLocaleTimeString()
      return `Offline mode • Last synced at ${time}`
    }
    return 'Offline mode • Using cached data'
  }
  if (isStale.value) {
    return 'Using cached data • Will sync when available'
  }
  return ''
})

async function updateStatus() {
  onlineStatus.value = isOnline()
  if (!onlineStatus.value || show.value) {
    statusDetails.value = await getOfflineStatus()
  }
  // Auto-hide if online and not stale
  if (onlineStatus.value && !isStale.value) {
    show.value = false
  }
}

function dismiss() {
  show.value = false
}

onMounted(() => {
  updateStatus()
  // Listen for connectivity changes
  window.addEventListener('online', updateStatus)
  window.addEventListener('offline', () => {
    onlineStatus.value = false
    show.value = true
  })
  // Register for sync events
  unsubscribe = registerConnectivityListener((result) => {
    if (result.success) {
      updateStatus()
    }
  })
})

onUnmounted(() => {
  window.removeEventListener('online', updateStatus)
  window.removeEventListener('offline', updateStatus)
  if (unsubscribe) unsubscribe()
})
</script>

<style scoped>
.offline-banner {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 10000;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 8px 16px;
  font-size: 13px;
  font-weight: 500;
  transition: all 0.3s ease;
  min-height: 36px;
}

.offline-banner.offline {
  background: #D32F2F;
  color: white;
}

.offline-banner.stale {
  background: #FF9800;
  color: white;
}

.offline-banner:not(.offline):not(.stale) {
  display: none;
}

.offline-icon {
  font-size: 18px;
}

.offline-text {
  flex: 1;
  text-align: center;
}

.offline-dismiss {
  background: none;
  border: none;
  color: inherit;
  cursor: pointer;
  padding: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0.8;
  transition: opacity 0.2s;
}

.offline-dismiss:hover {
  opacity: 1;
}

.offline-dismiss .material-icons {
  font-size: 18px;
}

/* Adjust for safe areas on mobile */
@supports (padding-top: env(safe-area-inset-top)) {
  .offline-banner {
    padding-top: calc(8px + env(safe-area-inset-top));
    min-height: calc(36px + env(safe-area-inset-top));
  }
}
</style>
