<template>
  <div class="splash-screen" :class="{ 'splash-exit': isExiting }">
    <!-- Logo -->
    <div class="splash-logo-container">
      <img
        src="../assets/SEAITlogo.png"
        alt="SEAIT Logo"
        class="splash-logo-img"
        @error="logoFailed = true"
        v-if="!logoFailed"
      />
      <span v-else class="material-icons splash-logo-fallback">school</span>
    </div>

    <!-- Title -->
    <h1 class="splash-title">SEAIT Campus Guide</h1>
    <p class="splash-subtitle">TechnoPath Navigation System</p>

    <!-- Loading spinner -->
    <div class="splash-spinner-wrap">
      <div class="splash-spinner"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const logoFailed = ref(false)
const isExiting = ref(false)
const startTime = Date.now()
const minDisplay = 1500  // Minimum 1.5 seconds for UX

onMounted(() => {
  // Smart splash: ensure minimum display time while loading
  const elapsed = Date.now() - startTime
  const remaining = Math.max(0, minDisplay - elapsed)
  
  setTimeout(() => {
    isExiting.value = true
    // Wait for exit animation to complete
    setTimeout(() => {
      sessionStorage.setItem('tp_splash_shown', 'true')
      router.replace('/')
    }, 450)
  }, remaining)
})
</script>

<style>
@import '../assets/splash.css';
</style>
