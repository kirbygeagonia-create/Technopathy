<template>
  <div class="adminlogin-view">
    <div class="adminlogin-card">
      <h1>TechnoPath Admin</h1>
      <p class="adminlogin-subtitle">SEAIT Campus Guide Administration</p>

      <form @submit.prevent="handleLogin">
        <div class="adminlogin-input-group">
          <label>Username</label>
          <input 
            v-model="username" 
            type="text" 
            placeholder="Enter username"
            required
          />
        </div>

        <div class="adminlogin-input-group">
          <label>Password</label>
          <input 
            v-model="password" 
            type="password" 
            placeholder="Enter password"
            required
          />
        </div>

        <div v-if="error" class="adminlogin-error-message">
          {{ error }}
        </div>

        <button type="submit" class="adminlogin-btn-primary" :disabled="isLoading">
          {{ isLoading ? 'Logging in...' : 'Login' }}
        </button>
      </form>

      <p class="adminlogin-back-link">
        <button class="adminlogin-btn-back-link" @click="goBack">
          <span class="material-icons" style="font-size: 16px; vertical-align: middle;">arrow_back</span>
          Back to app
        </button>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/authStore.js'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const error = ref('')
const isLoading = ref(false)

async function handleLogin() {
  error.value = ''
  isLoading.value = true
  console.log('Login started...')

  const result = await authStore.login(username.value, password.value)
  console.log('Login result:', result)
  
  if (result.success) {
    console.log('Login successful, redirecting to /admin')
    await router.push('/admin')
  } else {
    console.error('Login failed:', result.error)
    error.value = result.error
  }
  
  isLoading.value = false
}

function goBack() {
  router.push('/')
}
</script>

<style>
/* Styles moved to external file: src/assets/adminlogin.css */
@import '../assets/adminlogin.css';
</style>
