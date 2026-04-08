<template>
  <div class="profile-view">
    <!-- Header -->
    <div class="profile-header">
      <button class="profile-back-btn" @click="goBack">
        <span class="material-icons">arrow_back</span>
      </button>
      <h1>Profile</h1>
      <div class="profile-spacer"></div>
    </div>

    <!-- Profile Content -->
    <div class="profile-content">
      <!-- Avatar Section -->
      <div class="profile-avatar-section">
        <div class="profile-avatar">
          <span class="material-icons">person</span>
        </div>
        <button class="profile-change-avatar" @click="changeAvatar">
          <span class="material-icons">photo_camera</span>
          Change Photo
        </button>
      </div>

      <!-- User Info Section -->
      <div class="profile-section">
        <h3 class="profile-section-title">User Information</h3>
        <div class="profile-card">
          <div class="profile-item">
            <div class="profile-item-icon" style="background: #E3F2FD; color: #2196F3;">
              <span class="material-icons">person</span>
            </div>
            <div class="profile-item-text">
              <div class="profile-item-title">Display Name</div>
              <div class="profile-item-subtitle">{{ userProfile.displayName || 'Guest User' }}</div>
            </div>
            <button class="profile-edit-btn" @click="editName">
              <span class="material-icons">edit</span>
            </button>
          </div>

          <div class="profile-item">
            <div class="profile-item-icon" style="background: #FFF3E0; color: #FF9800;">
              <span class="material-icons">email</span>
            </div>
            <div class="profile-item-text">
              <div class="profile-item-title">Email</div>
              <div class="profile-item-subtitle">{{ userProfile.email || 'Not provided' }}</div>
            </div>
          </div>

          <div class="profile-item">
            <div class="profile-item-icon" style="background: #F3E5F5; color: #9C27B0;">
              <span class="material-icons">phone</span>
            </div>
            <div class="profile-item-text">
              <div class="profile-item-title">Phone</div>
              <div class="profile-item-subtitle">{{ userProfile.phone || 'Not provided' }}</div>
            </div>
            <button class="profile-edit-btn" @click="editPhone">
              <span class="material-icons">edit</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Preferences Section -->
      <div class="profile-section">
        <h3 class="profile-section-title">Preferences</h3>
        <div class="profile-card">
          <div class="profile-item">
            <div class="profile-item-icon" style="background: #E8F5E9; color: #4CAF50;">
              <span class="material-icons">language</span>
            </div>
            <div class="profile-item-text">
              <div class="profile-item-title">Language</div>
              <div class="profile-item-subtitle">{{ selectedLanguage }}</div>
            </div>
            <select v-model="selectedLanguage" class="profile-select" @change="saveLanguage">
              <option value="English">English</option>
              <option value="Filipino">Filipino</option>
              <option value="Cebuano">Cebuano</option>
            </select>
          </div>

          <div class="profile-item">
            <div class="profile-item-icon" style="background: #FFF8E1; color: #FFC107;">
              <span class="material-icons">text_fields</span>
            </div>
            <div class="profile-item-text">
              <div class="profile-item-title">Font Size</div>
              <div class="profile-item-subtitle">{{ fontSizeLabels[fontScale] }}</div>
            </div>
            <div class="profile-slider-container">
              <input
                type="range"
                min="0.8"
                max="1.3"
                step="0.1"
                v-model="fontScale"
                class="profile-slider"
                @change="saveFontScale"
              />
            </div>
          </div>

          <div class="profile-item">
            <div class="profile-item-icon" style="background: #ECEFF1; color: #607D8B;">
              <span class="material-icons">contrast</span>
            </div>
            <div class="profile-item-text">
              <div class="profile-item-title">High Contrast</div>
              <div class="profile-item-subtitle">Better visibility</div>
            </div>
            <label class="profile-switch">
              <input type="checkbox" v-model="highContrast" @change="saveHighContrast">
              <span class="profile-slider-switch"></span>
            </label>
          </div>

          <div class="profile-item">
            <div class="profile-item-icon" style="background: #FCE4EC; color: #E91E63;">
              <span class="material-icons">animation</span>
            </div>
            <div class="profile-item-text">
              <div class="profile-item-title">Reduce Animations</div>
              <div class="profile-item-subtitle">Minimize motion effects</div>
            </div>
            <label class="profile-switch">
              <input type="checkbox" v-model="reduceAnimations" @change="saveReduceAnimations">
              <span class="profile-slider-switch"></span>
            </label>
          </div>
        </div>
      </div>

      <!-- Quick Links Section -->
      <div class="profile-section">
        <h3 class="profile-section-title">Quick Links</h3>
        <div class="profile-card">
          <div class="profile-item" @click="goToFavorites">
            <div class="profile-item-icon" style="background: #FFEBEE; color: #F44336;">
              <span class="material-icons">favorite</span>
            </div>
            <div class="profile-item-text">
              <div class="profile-item-title">My Favorites</div>
              <div class="profile-item-subtitle">{{ favoritesCount }} saved locations</div>
            </div>
            <span class="material-icons profile-chevron">chevron_right</span>
          </div>

          <div class="profile-item" @click="goToSettings">
            <div class="profile-item-icon" style="background: #E0F7FA; color: #00BCD4;">
              <span class="material-icons">settings</span>
            </div>
            <div class="profile-item-text">
              <div class="profile-item-title">Settings</div>
              <div class="profile-item-subtitle">App configuration</div>
            </div>
            <span class="material-icons profile-chevron">chevron_right</span>
          </div>
        </div>
      </div>

      <!-- Account Actions -->
      <div class="profile-section">
        <h3 class="profile-section-title">Account</h3>
        <div class="profile-card">
          <div class="profile-item profile-item-danger" @click="logout" v-if="isLoggedIn">
            <div class="profile-item-icon" style="background: #FFEBEE; color: #F44336;">
              <span class="material-icons">logout</span>
            </div>
            <div class="profile-item-text">
              <div class="profile-item-title">Logout</div>
              <div class="profile-item-subtitle">Sign out of your account</div>
            </div>
            <span class="material-icons profile-chevron">chevron_right</span>
          </div>

          <div class="profile-item" @click="goToAdminLogin" v-else>
            <div class="profile-item-icon" style="background: #FFF3E0; color: #FF9800;">
              <span class="material-icons">login</span>
            </div>
            <div class="profile-item-text">
              <div class="profile-item-title">Login as Admin</div>
              <div class="profile-item-subtitle">Access admin dashboard</div>
            </div>
            <span class="material-icons profile-chevron">chevron_right</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Name Dialog -->
    <div v-if="showEditName" class="profile-modal-overlay" @click="showEditName = false">
      <div class="profile-dialog" @click.stop>
        <h3>Edit Display Name</h3>
        <input
          v-model="editNameValue"
          type="text"
          placeholder="Enter your name"
          class="profile-dialog-input"
        />
        <div class="profile-dialog-actions">
          <button class="profile-btn-secondary" @click="showEditName = false">Cancel</button>
          <button class="profile-btn-primary" @click="saveName">Save</button>
        </div>
      </div>
    </div>

    <!-- Edit Phone Dialog -->
    <div v-if="showEditPhone" class="profile-modal-overlay" @click="showEditPhone = false">
      <div class="profile-dialog" @click.stop>
        <h3>Edit Phone Number</h3>
        <input
          v-model="editPhoneValue"
          type="tel"
          placeholder="Enter phone number"
          class="profile-dialog-input"
        />
        <div class="profile-dialog-actions">
          <button class="profile-btn-secondary" @click="showEditPhone = false">Cancel</button>
          <button class="profile-btn-primary" @click="savePhone">Save</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/authStore.js'
import { showToast } from '../services/toast.js'
import api from '../services/api.js'

const authStore = useAuthStore()

// User profile data
const userProfile = ref({
  displayName: '',
  email: '',
  phone: ''
})

// Preferences
const selectedLanguage = ref('English')
const fontScale = ref(1.0)
const highContrast = ref(false)
const reduceAnimations = ref(false)

// Favorites
const favoritesCount = ref(0)

// Auth state - use authStore instead of localStorage
const isLoggedIn = computed(() => authStore.isLoggedIn)

// Dialog states
const showEditName = ref(false)
const showEditPhone = ref(false)
const editNameValue = ref('')
const editPhoneValue = ref('')

// Font size labels
const fontSizeLabels = {
  0.8: 'Small',
  0.9: 'Normal',
  1.0: 'Default',
  1.1: 'Large',
  1.2: 'Extra Large',
  1.3: 'Huge'
}

// Methods
const goBack = () => router.back()
const goToSettings = () => router.push('/settings')
const goToFavorites = () => router.push('/favorites')
const goToAdminLogin = () => router.push('/admin/login')

const changeAvatar = () => {
  showToast('Avatar upload coming soon!', 'info')
}

const editName = () => {
  editNameValue.value = userProfile.value.displayName
  showEditName.value = true
}

const saveName = () => {
  userProfile.value.displayName = editNameValue.value
  showEditName.value = false
  // Save to localStorage for now
  localStorage.setItem('tp_user_name', editNameValue.value)
}

const editPhone = () => {
  editPhoneValue.value = userProfile.value.phone
  showEditPhone.value = true
}

const savePhone = () => {
  userProfile.value.phone = editPhoneValue.value
  showEditPhone.value = false
  localStorage.setItem('tp_user_phone', editPhoneValue.value)
}

const saveLanguage = async () => {
  localStorage.setItem('tp_language', selectedLanguage.value)
  // TODO: Sync with backend if logged in
}

const saveFontScale = async () => {
  localStorage.setItem('tp_font_scale', fontScale.value)
  // Apply font scale to root element
  document.documentElement.style.setProperty('--font-scale', fontScale.value)
  // TODO: Sync with backend if logged in
}

const saveHighContrast = async () => {
  localStorage.setItem('tp_high_contrast', highContrast.value)
  if (highContrast.value) {
    document.body.classList.add('high-contrast')
  } else {
    document.body.classList.remove('high-contrast')
  }
  // TODO: Sync with backend if logged in
}

const saveReduceAnimations = async () => {
  localStorage.setItem('tp_reduce_animations', reduceAnimations.value)
  if (reduceAnimations.value) {
    document.body.classList.add('reduce-animations')
  } else {
    document.body.classList.remove('reduce-animations')
  }
}

const logout = () => {
  authStore.logout(router, '/')
}

// Load preferences from localStorage
const loadPreferences = () => {
  userProfile.value.displayName = localStorage.getItem('tp_user_name') || ''
  userProfile.value.phone = localStorage.getItem('tp_user_phone') || ''
  selectedLanguage.value = localStorage.getItem('tp_language') || 'English'
  fontScale.value = parseFloat(localStorage.getItem('tp_font_scale')) || 1.0
  highContrast.value = localStorage.getItem('tp_high_contrast') === 'true'
  reduceAnimations.value = localStorage.getItem('tp_reduce_animations') === 'true'

  // Apply saved preferences
  document.documentElement.style.setProperty('--font-scale', fontScale.value)
  if (highContrast.value) document.body.classList.add('high-contrast')
  if (reduceAnimations.value) document.body.classList.add('reduce-animations')
}

// Load favorites count
const loadFavorites = async () => {
  try {
    const res = await api.get('/core/favorites/')
    favoritesCount.value = res.data.length
  } catch (error) {
    // Fallback: count from localStorage
    const localFavorites = JSON.parse(localStorage.getItem('tp_favorites') || '[]')
    favoritesCount.value = localFavorites.length
  }
}

onMounted(() => {
  loadPreferences()
  loadFavorites()
})
</script>

<style>
@import '../assets/profileview.css';
</style>
