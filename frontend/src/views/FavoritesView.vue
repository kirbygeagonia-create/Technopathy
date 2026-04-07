<template>
  <div class="favorites-view">
    <!-- Header -->
    <div class="favorites-header">
      <button class="favorites-back-btn" @click="goBack">
        <span class="material-icons">arrow_back</span>
      </button>
      <h1>My Favorites</h1>
      <div class="favorites-spacer"></div>
    </div>

    <!-- Content -->
    <div class="favorites-content">
      <!-- Empty State -->
      <div v-if="favorites.length === 0" class="favorites-empty">
        <span class="material-icons favorites-empty-icon">favorite_border</span>
        <h3>No Favorites Yet</h3>
        <p>Save your frequently visited locations for quick access</p>
        <button class="favorites-explore-btn" @click="goToHome">
          <span class="material-icons">explore</span>
          Explore Map
        </button>
      </div>

      <!-- Favorites List -->
      <div v-else class="favorites-list">
        <div class="favorites-count">{{ favorites.length }} saved location{{ favorites.length !== 1 ? 's' : '' }}</div>

        <div
          v-for="favorite in favorites"
          :key="favorite.id"
          class="favorites-item"
        >
          <div class="favorites-item-content" @click="goToLocation(favorite)">
            <div class="favorites-item-icon" :class="favorite.type">
              <span class="material-icons">
                {{ favorite.type === 'facility' ? 'business' : 'meeting_room' }}
              </span>
            </div>
            <div class="favorites-item-text">
              <div class="favorites-item-title">{{ favorite.name }}</div>
              <div class="favorites-item-subtitle">{{ favorite.description || favorite.type }}</div>
              <div class="favorites-item-date">Added {{ formatDate(favorite.addedAt) }}</div>
            </div>
          </div>
          <button class="favorites-delete-btn" @click.stop="removeFavorite(favorite.id)">
            <span class="material-icons">delete_outline</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const favorites = ref([])

// Load favorites from localStorage
const loadFavorites = () => {
  const saved = localStorage.getItem('tp_favorites')
  favorites.value = saved ? JSON.parse(saved) : []
}

// Save favorites to localStorage
const saveFavorites = () => {
  localStorage.setItem('tp_favorites', JSON.stringify(favorites.value))
}

// Remove a favorite
const removeFavorite = (id) => {
  if (confirm('Remove this location from favorites?')) {
    favorites.value = favorites.value.filter(f => f.id !== id)
    saveFavorites()
  }
}

// Navigate to location on map
const goToLocation = (favorite) => {
  // Store selected location in sessionStorage for HomeView to pick up
  sessionStorage.setItem('tp_selected_location', JSON.stringify({
    type: favorite.type,
    name: favorite.name
  }))
  router.push('/')
}

// Format date
const formatDate = (dateString) => {
  if (!dateString) return 'recently'
  const date = new Date(dateString)
  const now = new Date()
  const diff = now - date
  
  // Less than 24 hours
  if (diff < 86400000) {
    const hours = Math.floor(diff / 3600000)
    if (hours < 1) return 'just now'
    return `${hours}h ago`
  }
  
  // Less than 7 days
  if (diff < 604800000) {
    const days = Math.floor(diff / 86400000)
    return `${days}d ago`
  }
  
  return date.toLocaleDateString()
}

// Navigation
const goBack = () => router.back()
const goToHome = () => router.push('/')

onMounted(() => {
  loadFavorites()
})
</script>

<style>
@import '../assets/favorites.css';
</style>
