<template>
  <div class="profile-view">
    <header class="profile-header">
      <button class="back-btn" @click="$router.back()">
        <span class="material-icons">arrow_back</span>
      </button>
      <h1>Profile</h1>
    </header>

    <div v-if="isLoading" class="profile-sk-wrap">
      <AppSkeleton :loading="true" name="profile-card" animate="shimmer" />
    </div>
    <div class="profile-content" v-else>
      <div class="profile-card">
        <div class="avatar">
          <span class="material-icons">person</span>
        </div>
        <h2>{{ userName }}</h2>
        <p class="email">{{ userEmail }}</p>
      </div>

      <div class="info-section">
        <h3>Account Information</h3>
        <div class="info-item">
          <span class="label">Student ID</span>
          <span class="value">{{ studentId }}</span>
        </div>
        <div class="info-item">
          <span class="label">Department</span>
          <span class="value">{{ department }}</span>
        </div>
        <div class="info-item">
          <span class="label">Year Level</span>
          <span class="value">{{ yearLevel }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/authStore.js'
import { registerBones } from 'boneyard-js'
import AppSkeleton from '../components/AppSkeleton.vue'

registerBones({
  'profile-card': {
    width: 390, height: 280,
    bones: [
      { x: 33, y: 0,   w: 34, h: 80,  r: '50%' },
      { x: 25, y: 92,  w: 50, h: 20,  r: 8     },
      { x: 20, y: 120, w: 60, h: 14,  r: 6     },
      { x: 0,  y: 155, w: 40, h: 14,  r: 6     },
      { x: 55, y: 155, w: 45, h: 14,  r: 6     },
      { x: 0,  y: 180, w: 40, h: 14,  r: 6     },
      { x: 55, y: 180, w: 45, h: 14,  r: 6     },
      { x: 0,  y: 205, w: 40, h: 14,  r: 6     },
      { x: 55, y: 205, w: 45, h: 14,  r: 6     },
    ]
  }
})

const auth = useAuthStore()
const isLoading = ref(true)
const isLoggedIn = computed(() => auth.isLoggedIn)

const userName = ref('Guest User')
const userEmail = ref('guest@seait.edu.ph')
const studentId = ref('-')
const department = ref('-')
const yearLevel = ref('-')

onMounted(() => {
  // If user is logged in, use auth store data
  if (auth.isLoggedIn && auth.user) {
    userName.value = auth.displayName || auth.user.username || 'Guest User'
    userEmail.value = auth.user.email || 'guest@seait.edu.ph'
    department.value = auth.departmentLabel || auth.user.department || '-'
    // Student ID and year level from profile if available
    const savedProfile = localStorage.getItem('tp_user_profile')
    if (savedProfile) {
      const profile = JSON.parse(savedProfile)
      studentId.value = profile.studentId || '-'
      yearLevel.value = profile.yearLevel || '-'
    }
  } else {
    // Load guest profile data from localStorage
    const savedProfile = localStorage.getItem('tp_user_profile')
    if (savedProfile) {
      const profile = JSON.parse(savedProfile)
      userName.value = profile.name || userName.value
      userEmail.value = profile.email || userEmail.value
      studentId.value = profile.studentId || studentId.value
      department.value = profile.department || department.value
      yearLevel.value = profile.yearLevel || yearLevel.value
    }
  }
  setTimeout(() => { isLoading.value = false }, 450)
})
</script>

<style scoped>
.profile-view {
  min-height: 100vh;
  background: #f5f5f5;
}

.profile-header {
  display: flex;
  align-items: center;
  padding: 16px;
  background: #fff;
  border-bottom: 1px solid #e0e0e0;
}

.back-btn {
  background: none;
  border: none;
  padding: 8px;
  margin-right: 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
}

.back-btn .material-icons {
  font-size: 24px;
  color: #333;
}

.profile-header h1 {
  font-size: 20px;
  font-weight: 600;
  margin: 0;
}

.profile-content {
  padding: 20px;
}

.profile-card {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  text-align: center;
  margin-bottom: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.avatar {
  width: 80px;
  height: 80px;
  background: #FF9800;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
}

.avatar .material-icons {
  font-size: 40px;
  color: white;
}

.profile-card h2 {
  font-size: 22px;
  font-weight: 600;
  margin: 0 0 8px;
}

.email {
  color: #666;
  margin: 0;
}

.info-section {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.info-section h3 {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 16px;
  color: #333;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}

.info-item:last-child {
  border-bottom: none;
}

.label {
  color: #666;
  font-size: 14px;
}

.value {
  font-weight: 500;
  color: #333;
  font-size: 14px;
}

.profile-sk-wrap { padding: 24px; height: 320px; }
</style>
