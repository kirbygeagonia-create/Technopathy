<template>
  <div v-if="isVisible" class="onboarding-overlay">
    <!-- Backdrop with cutout for highlighted element -->
    <div class="onboarding-backdrop" @click="skipTutorial"></div>
    
    <!-- Tutorial Card -->
    <div class="onboarding-card" :class="`step-${currentStep}`">
      <!-- Progress dots -->
      <div class="onboarding-progress">
        <div
          v-for="(_, index) in steps"
          :key="index"
          class="onboarding-dot"
          :class="{ active: index === currentStep }"
        ></div>
      </div>

      <!-- Step Content -->
      <div class="onboarding-content-wrapper">
        <Transition :name="transitionName" mode="out-in">
          <div :key="currentStep" class="onboarding-content">
            <div class="onboarding-icon">
              <span class="material-icons">{{ steps[currentStep].icon }}</span>
            </div>
            <h2 class="onboarding-title">{{ steps[currentStep].title }}</h2>
            <p class="onboarding-description">{{ steps[currentStep].description }}</p>
          </div>
        </Transition>
      </div>

      <!-- Actions -->
      <div class="onboarding-actions">
        <button v-if="currentStep > 0" class="onboarding-btn-secondary" @click="prevStep">
          Back
        </button>
        <button class="onboarding-btn-primary" @click="nextStep">
          {{ isLastStep ? 'Get Started' : 'Next' }}
        </button>
      </div>

      <!-- Skip option -->
      <button class="onboarding-skip" @click="skipTutorial">
        Skip tutorial
      </button>
    </div>

    <!-- Feature highlights (positioned absolutely based on step) -->
    <div
      v-if="steps[currentStep].highlight"
      class="onboarding-highlight"
      :style="getHighlightStyle()"
    >
      <div class="highlight-pulse"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const emit = defineEmits(['complete', 'skip'])

const currentStep = ref(0)
const isVisible = ref(false)
const transitionName = ref('slide-left')

const steps = [
  {
    icon: 'map',
    title: 'Welcome to Technopath',
    description: 'Your interactive campus guide. Navigate SEAIT with ease and discover campus facilities.',
    highlight: null
  },
  {
    icon: 'search',
    title: 'Quick Search',
    description: 'Find any building, room, or facility instantly. Use the search bar at the top to locate your destination.',
    highlight: 'search'
  },
  {
    icon: 'touch_app',
    title: 'Interactive Map',
    description: 'Tap on markers to see details. Zoom and pan to explore. Tap markers to add favorites or navigate.',
    highlight: 'map'
  },
  {
    icon: 'favorite',
    title: 'Save Favorites',
    description: 'Save frequently visited locations for quick access. Your favorites sync across sessions.',
    highlight: 'favorites'
  },
  {
    icon: 'chat',
    title: 'AI Assistant',
    description: 'Have questions? Our chatbot can help you find locations, hours, and answer campus FAQs.',
    highlight: 'chatbot'
  },
  {
    icon: 'navigation',
    title: 'Get Directions',
    description: 'Use the navigate feature to find the best route between any two points on campus.',
    highlight: 'navigate'
  }
]

const isLastStep = computed(() => currentStep.value === steps.length - 1)

const getHighlightStyle = () => {
  // Return responsive positioning styles based on current step
  // Uses viewport-relative units and safe-area insets for better mobile support
  const styles = {
    search: { 
      top: 'calc(var(--safe-top, 0px) + 80px)', 
      left: '50%', 
      transform: 'translateX(-50%)', 
      width: 'min(90%, 400px)', 
      height: '60px' 
    },
    map: { 
      top: '50%', 
      left: '50%', 
      transform: 'translate(-50%, -50%)', 
      width: 'min(200px, 50vw)', 
      height: 'min(200px, 30vh)' 
    },
    favorites: { 
      bottom: 'calc(120px + var(--safe-bottom, 0px))', 
      right: '20px', 
      width: '56px', 
      height: '56px' 
    },
    chatbot: { 
      bottom: 'calc(140px + var(--safe-bottom, 0px))', 
      left: '50%', 
      transform: 'translateX(-50%)', 
      width: '56px', 
      height: '56px' 
    },
    navigate: { 
      bottom: 'calc(140px + var(--safe-bottom, 0px))', 
      left: '50%', 
      transform: 'translateX(-50%)', 
      width: '56px', 
      height: '56px' 
    }
  }
  return styles[steps[currentStep.value].highlight] || {}
}

const nextStep = () => {
  if (isLastStep.value) {
    completeTutorial()
  } else {
    transitionName.value = 'slide-left'
    currentStep.value++
  }
}

const prevStep = () => {
  if (currentStep.value > 0) {
    transitionName.value = 'slide-right'
    currentStep.value--
  }
}

const skipTutorial = () => {
  localStorage.setItem('tp_onboarding_completed', 'true')
  localStorage.setItem('tp_onboarding_skipped', 'true')
  isVisible.value = false
  emit('skip')
}

const completeTutorial = () => {
  localStorage.setItem('tp_onboarding_completed', 'true')
  isVisible.value = false
  emit('complete')
}

// Check if should show onboarding
onMounted(() => {
  const completed = localStorage.getItem('tp_onboarding_completed')
  const skipped = localStorage.getItem('tp_onboarding_skipped')
  
  if (!completed && !skipped) {
    // Small delay to let the app render first
    setTimeout(() => {
      isVisible.value = true
    }, 500)
  }
})

// Expose methods for manual triggering
defineExpose({
  start: () => {
    currentStep.value = 0
    isVisible.value = true
  },
  reset: () => {
    localStorage.removeItem('tp_onboarding_completed')
    localStorage.removeItem('tp_onboarding_skipped')
    currentStep.value = 0
    isVisible.value = true
  }
})
</script>

<style>
@import '../assets/onboarding.css';
</style>
