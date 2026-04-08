<template>
  <div class="settings-view">
    <!-- Header -->
    <div class="settings-header">
      <div class="settings-header-content">
        <div class="settings-header-icon">
          <span class="material-icons">settings</span>
        </div>
        <div class="settings-header-text">
          <h1>App Settings</h1>
          <p>Customize your experience</p>
        </div>
      </div>
    </div>

    <!-- Settings List -->
    <div class="settings-content">
      <!-- Account Section -->
      <div class="settings-section">
        <h3 class="settings-section-title">Account</h3>
        <div class="settings-card">
          <div class="settings-item" @click="goToProfile">
            <div class="settings-item-icon" style="background: #E3F2FD; color: #2196F3;">
              <span class="material-icons">person</span>
            </div>
            <div class="settings-item-text">
              <div class="settings-item-title">Profile</div>
              <div class="settings-item-subtitle">View and edit your profile</div>
            </div>
            <span class="material-icons settings-chevron">chevron_right</span>
          </div>
          <div class="settings-divider"></div>
          <div class="settings-item" @click="goToAdminLogin">
            <div class="settings-item-icon" style="background: #FFF3E0; color: #FF9800;">
              <span class="material-icons">admin_panel_settings</span>
            </div>
            <div class="settings-item-text">
              <div class="settings-item-title">Login Admin</div>
              <div class="settings-item-subtitle">Access admin dashboard</div>
            </div>
            <span class="material-icons settings-chevron">chevron_right</span>
          </div>
        </div>
      </div>

      <!-- Appearance Section -->
      <div class="settings-section">
        <h3 class="settings-section-title">Appearance</h3>
        <div class="settings-card">
          <div class="settings-item">
            <div class="settings-item-icon" style="background: #F3E5F5; color: #9C27B0;">
              <span class="material-icons">dark_mode</span>
            </div>
            <div class="settings-item-text">
              <div class="settings-item-title">Dark Mode</div>
              <div class="settings-item-subtitle">Toggle dark theme</div>
            </div>
            <label class="settings-switch">
              <input type="checkbox" v-model="isDarkMode" @change="toggleTheme">
              <span class="settings-slider"></span>
            </label>
          </div>
        </div>
      </div>

      <!-- Info Section -->
      <div class="settings-section">
        <h3 class="settings-section-title">Info</h3>
        <div class="settings-card">
          <div class="settings-item" @click="showFacilitiesRoomsPanel = true">
            <div class="settings-item-icon" style="background: #FFF3E0; color: #FF9800;">
              <span class="material-icons">business</span>
            </div>
            <div class="settings-item-text">
              <div class="settings-item-title">Facilities & Rooms</div>
              <div class="settings-item-subtitle">Browse campus facilities and rooms</div>
            </div>
            <span class="material-icons settings-chevron">chevron_right</span>
          </div>
        </div>
      </div>

      <!-- About Section -->
      <div class="settings-section">
        <h3 class="settings-section-title">About</h3>
        <div class="settings-card">
          <div class="settings-item">
            <div class="settings-item-icon" style="background: #E3F2FD; color: #2196F3;">
              <span class="material-icons">info_outline</span>
            </div>
            <div class="settings-item-text">
              <div class="settings-item-title">About Us</div>
              <div class="settings-item-subtitle">Guide Map Navigation app for campus routing</div>
            </div>
          </div>
          <div class="settings-divider"></div>
          <div class="settings-item">
            <div class="settings-item-icon" style="background: #E8F5E9; color: #4CAF50;">
              <span class="material-icons">verified</span>
            </div>
            <div class="settings-item-text">
              <div class="settings-item-title">Version</div>
              <div class="settings-item-subtitle">1.0.0</div>
            </div>
          </div>
          <div class="settings-divider"></div>
          <div class="settings-item" @click="checkForUpdates">
            <div class="settings-item-icon" style="background: #FFF3E0; color: #FF5722;">
              <span class="material-icons">system_update</span>
            </div>
            <div class="settings-item-text">
              <div class="settings-item-title">Check for Updates</div>
              <div class="settings-item-subtitle">Verify you have the latest version</div>
            </div>
          </div>
        </div>
      </div>

      <div class="bottom-spacer"></div>
    </div>

    <!-- Facilities & Rooms Panel Modal -->
    <Transition name="fade">
      <div v-if="showFacilitiesRoomsPanel" class="modal-overlay" @click="showFacilitiesRoomsPanel = false">
        <div class="dialog fr-dialog" @click.stop style="padding: 0; width: 95vw; max-width: 600px; overflow: hidden; border-radius: 16px;">
          <FacilitiesRoomsPanel @close="showFacilitiesRoomsPanel = false" />
        </div>
      </div>
    </Transition>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useThemeStore } from '../stores/themeStore.js'
import { showToast } from '../services/toast.js'
import FacilitiesRoomsPanel from '../components/FacilitiesRoomsPanel.vue'

const router = useRouter()
const themeStore = useThemeStore()

// State - use computed for dark mode to sync with store
const isDarkMode = computed({
  get: () => themeStore.isDarkMode,
  set: (val) => themeStore.setTheme(val)
})
const showFacilitiesRoomsPanel = ref(false)

// Methods
const goToAdminLogin = () => {
  router.push('/admin/login')
}

const goToProfile = () => {
  router.push('/profile')
}

const toggleTheme = () => {
  themeStore.toggleTheme()
  showToast(themeStore.isDarkMode ? 'Dark mode enabled' : 'Light mode enabled')
}

const isCheckingUpdate = ref(false)
const updateAvailable = ref(false)
const currentVersion = ref('1.0.0')

const checkForUpdates = async () => {
  isCheckingUpdate.value = true
  try {
    // Check for service worker updates
    const registration = await navigator.serviceWorker?.getRegistration()
    if (registration) {
      await registration.update()
      
      // Check if new service worker is waiting
      if (registration.waiting) {
        updateAvailable.value = true
        showToast('Update available! Restart app to apply.', 'info')
      } else {
        showToast('You are using the latest version.', 'success')
      }
    } else {
      showToast('App is up to date', 'success')
    }
  } catch (error) {
    showToast('Could not check for updates', 'error')
  } finally {
    isCheckingUpdate.value = false
  }
}

// Using global showToast from toast.js service

onMounted(() => {
  // Initialize theme store if not already done
  themeStore.initTheme()
})
</script>

<style>
/* Styles moved to external file: src/assets/settings.css */
@import '../assets/settings.css';
</style>
