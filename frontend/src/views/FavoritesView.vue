<template>
  <div class="favorites-view">
    <header class="favorites-header">
      <button class="back-btn" @click="$router.back()">
        <span class="material-icons">arrow_back</span>
      </button>
      <h1>Favorites</h1>
    </header>

    <div class="favorites-content">
      <!-- Skeleton Loading -->
      <div v-if="isLoading" class="favorites-skeleton">
        <div v-for="n in 4" :key="n" class="fav-skeleton-card">
          <div class="skeleton" style="width:48px;height:48px;border-radius:12px;flex-shrink:0"></div>
          <div style="flex:1;display:flex;flex-direction:column;gap:8px">
            <div class="skeleton" style="height:14px;width:55%;border-radius:6px"></div>
            <div class="skeleton" style="height:11px;width:35%;border-radius:6px"></div>
          </div>
        </div>
      </div>

      <div v-else-if="favorites.length === 0" class="empty-state">
        <span class="material-icons">favorite_border</span>
        <p>No favorites yet</p>
        <p class="sub">Tap the star icon on locations to save them here</p>
      </div>

      <div v-else class="favorites-list">
        <div v-for="item in favorites" :key="item.id" class="favorite-card" @click="goToLocation(item)">
          <div class="favorite-icon">
            <span class="material-icons">place</span>
          </div>
          <div class="favorite-info">
            <h3>{{ item.name }}</h3>
            <p>{{ item.description || formatFavoriteType(item.type) }}</p>
          </div>
          <button class="remove-btn" @click.stop="removeFavorite(item.id)">
            <span class="material-icons">close</span>
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
const isLoading = ref(true)

onMounted(() => {
  loadFavorites()
})

function loadFavorites() {
  isLoading.value = true
  const saved = localStorage.getItem('tp_favorites')
  if (saved) {
    favorites.value = JSON.parse(saved)
  }
  isLoading.value = false
}

function formatFavoriteType(type) {
  const labels = { facility: 'Building / Facility', room: 'Room', building: 'Building' }
  return labels[type] || type || 'Location'
}

function removeFavorite(id) {
  favorites.value = favorites.value.filter(f => f.id !== id)
  localStorage.setItem('tp_favorites', JSON.stringify(favorites.value))
}

function goToLocation(item) {
  // Handles composite IDs saved as "facility_123" or "room_456"
  // Also handles legacy 'building' type for backward compatibility
  if (item.type === 'facility' || item.type === 'building') {
    // Navigate to map and highlight the facility by its svg_id or name
    const target = item.map_svg_id || item.svgId || item.name || ''
    router.push({ path: '/map', query: { highlight: target } })
  } else if (item.type === 'room') {
    router.push({ path: '/navigate', query: { to: item.map_svg_id || item.name || item.id } })
  } else {
    // Fallback: go to map
    router.push('/map')
  }
}
</script>

<style scoped>
.favorites-view {
  min-height: 100vh;
  background: #f5f5f5;
}

.favorites-header {
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

.favorites-header h1 {
  font-size: 20px;
  font-weight: 600;
  margin: 0;
}

.favorites-content {
  padding: 16px;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #999;
}

.empty-state .material-icons {
  font-size: 64px;
  margin-bottom: 16px;
}

.empty-state p {
  font-size: 18px;
  font-weight: 500;
  margin: 0 0 8px;
}

.empty-state .sub {
  font-size: 14px;
  color: #bbb;
}

.favorites-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.favorite-card {
  display: flex;
  align-items: center;
  background: #fff;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  cursor: pointer;
}

.favorite-icon {
  width: 40px;
  height: 40px;
  background: #FF9800;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
}

.favorite-icon .material-icons {
  font-size: 20px;
  color: white;
}

.favorite-info {
  flex: 1;
}

.favorite-info h3 {
  font-size: 16px;
  font-weight: 500;
  margin: 0 0 4px;
}

.favorite-info p {
  font-size: 13px;
  color: #888;
  margin: 0;
  text-transform: capitalize;
}

.remove-btn {
  background: none;
  border: none;
  padding: 8px;
  cursor: pointer;
  color: #999;
}

.remove-btn .material-icons {
  font-size: 20px;
}
</style>
