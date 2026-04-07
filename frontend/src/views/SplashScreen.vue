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

onMounted(() => {
  // Auto-navigate after 2.5 seconds (matching Flutter's 3s minus Vue mount time)
  setTimeout(() => {
    isExiting.value = true
    // Wait for exit animation to complete
    setTimeout(() => {
      sessionStorage.setItem('tp_splash_shown', 'true')
      router.replace('/')
    }, 450)
  }, 2500)
})
</script>

<style>
@import '../assets/splash.css';
</style>
