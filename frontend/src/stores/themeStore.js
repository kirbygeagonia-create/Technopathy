import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  // State
  const isDarkMode = ref(false)
  
  // Initialize from localStorage or default to light mode
  const initTheme = () => {
    const stored = localStorage.getItem('tp_dark_mode')
    if (stored !== null) {
      isDarkMode.value = stored === 'true'
    } else {
      // Default to light mode, don't use system preference
      isDarkMode.value = false
    }
    applyTheme()
  }
  
  // Apply theme to document
  const applyTheme = () => {
    document.body.classList.toggle('dark-mode', isDarkMode.value)
    document.documentElement.classList.remove('dark-mode-preload')
  }
  
  // Toggle theme
  const toggleTheme = () => {
    isDarkMode.value = !isDarkMode.value
    localStorage.setItem('tp_dark_mode', isDarkMode.value.toString())
    applyTheme()
  }
  
  // Set theme explicitly
  const setTheme = (dark) => {
    isDarkMode.value = dark
    localStorage.setItem('tp_dark_mode', isDarkMode.value.toString())
    applyTheme()
  }
  
  // Computed getter
  const darkMode = computed(() => isDarkMode.value)
  
  return {
    isDarkMode,
    darkMode,
    initTheme,
    toggleTheme,
    setTheme,
    applyTheme
  }
})
