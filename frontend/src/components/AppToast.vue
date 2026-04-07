<template>
  <transition name="toast-slide">
    <div v-if="toastState.visible" class="app-global-toast" :class="`toast-${toastState.type}`">
      <span class="material-icons toast-icon">{{ icon }}</span>
      <span class="toast-message">{{ toastState.message }}</span>
      <button class="toast-close" @click="hideToast">
        <span class="material-icons">close</span>
      </button>
    </div>
  </transition>
</template>

<script setup>
import { computed } from 'vue'
import { toastState, hideToast } from '../services/toast.js'

const icon = computed(() => {
  switch (toastState.type) {
    case 'success': return 'check_circle'
    case 'error': return 'error'
    case 'warning': return 'warning'
    case 'info':
    default: return 'info'
  }
})
</script>

<style scoped>
.app-global-toast {
  position: fixed;
  bottom: calc(var(--bottom-nav-height, 60px) + var(--safe-bottom, 0px) + 16px);
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  color: white;
  border-radius: var(--radius-md, 8px);
  box-shadow: var(--shadow-lg, 0 4px 12px rgba(0,0,0,0.15));
  z-index: 9999;
  min-width: 280px;
  max-width: 90vw;
}

body.dark-mode .app-global-toast {
  box-shadow: 0 4px 16px rgba(0,0,0,0.5);
}

.toast-success { background: var(--color-success, #388E3C); }
.toast-error { background: var(--color-danger, #D32F2F); }
.toast-warning { background: var(--color-warning, #F57C00); }
.toast-info { background: var(--color-info, #1976D2); }

.toast-icon { font-size: 20px; }

.toast-message { 
  flex: 1; 
  font-size: var(--text-sm, 14px); 
  font-family: var(--font-primary, sans-serif); 
  font-weight: 500;
}

.toast-close {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0.8;
  padding: 4px;
}

.toast-close:hover { opacity: 1; }
.toast-close .material-icons { font-size: 18px; }

.toast-slide-enter-active, .toast-slide-leave-active {
  transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}
.toast-slide-enter-from, .toast-slide-leave-to {
  opacity: 0;
  transform: translate(-50%, 20px);
}
</style>
