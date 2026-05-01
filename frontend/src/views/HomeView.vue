<template>
  <div class="home-view">
    <!-- Onboarding Tutorial -->
    <OnboardingTutorial 
      v-if="showOnboarding" 
      ref="onboardingRef" 
      @complete="onOnboardingComplete" 
      @skip="onOnboardingSkip" 
    />

    <!-- Header Bar with Search -->
    <header class="home-header">
      <div class="home-header-content">
        <div class="home-header-icon">
          <span class="material-icons">school</span>
        </div>
        <div class="home-header-text">
          <h1>TechnoPath</h1>
          <p>SEAIT Campus Guide</p>
        </div>
      </div>
      <!-- Search Bar in Header -->
      <div class="home-header-search">
        <div class="home-search-input-wrapper">
          <span class="material-icons search-icon">search</span>
          <input
            v-model="searchText"
            type="text"
            placeholder="Search locations, facilities..."
            @keyup.enter="performSearch"
            @input="debouncedSearch"
            class="home-search-input"
          />
          <button v-if="searchText" class="clear-btn" @click="searchText = ''">
            <span class="material-icons">close</span>
          </button>
        </div>
      </div>
    </header>

    <!-- Unified Top Search & Filter Area -->
    <div class="home-top-overlay">
      <!-- Search Suggestions Dropdown -->
      <div class="home-suggestions-overlay" v-if="searchSuggestions.length > 0 && searchText">
        <div class="search-suggestions unified-suggestions">
          <div
            v-for="suggestion in searchSuggestions.slice(0, 6)"
            :key="suggestion.name"
            class="suggestion-item"
            @click="selectSuggestion(suggestion)"
          >
            <span class="material-icons">
              {{ suggestion.icon || 'place' }}
            </span>
            <div class="suggestion-info">
              <span class="suggestion-name">{{ suggestion.name }}</span>
              <span class="suggestion-type">{{ suggestion.info }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- SEAIT Information Section -->
    <div class="seait-info-section">
      <div class="seait-header">
        <h1 class="seait-title">SEAIT</h1>
        <p class="seait-subtitle">South East Asian Institute of Technology</p>
      </div>

      <div class="seait-highlights">
        <div class="highlight-card">
          <span class="material-icons highlight-icon">school</span>
          <h3>Quality Education</h3>
          <p>Providing excellent technical and vocational education since establishment</p>
        </div>

        <div class="highlight-card stagger-card">
          <span class="material-icons highlight-icon">engineering</span>
          <h3>Modern Facilities</h3>
          <p>State-of-the-art classrooms, laboratories, and workshop areas</p>
        </div>

        <div class="highlight-card stagger-card">
          <span class="material-icons highlight-icon">location_on</span>
          <h3>Strategic Location</h3>
          <p>Conveniently located in the heart of the community with easy access</p>
        </div>

        <div class="highlight-card stagger-card">
          <span class="material-icons highlight-icon">groups</span>
          <h3>Expert Faculty</h3>
          <p>Dedicated instructors and staff committed to student success</p>
        </div>
      </div>

      <!-- Announcements Feed -->
      <div class="home-announcements">
        <h2 class="home-section-title">
          <span class="material-icons">campaign</span>
          Announcements
        </h2>
        <!-- Skeleton -->
        <template v-if="announcementsLoading">
          <div v-for="n in 3" :key="n" class="home-announcement-sk-wrap">
            <AppSkeleton :loading="true" name="home-announcement" animate="shimmer" />
          </div>
        </template>
        <!-- Real cards -->
        <template v-else-if="announcementsRef.length > 0">
          <div
            v-for="ann in announcementsRef"
            :key="ann.id"
            class="announcement-card stagger-card"
          >
            <div class="announcement-header">
              <span
                class="announcement-dept-chip"
                :style="{ background: getDeptColor(ann.department_color) }"
              >{{ ann.department_label || 'Campus' }}</span>
              <span class="announcement-date">{{ formatDate(ann.published_at || ann.created_at) }}</span>
            </div>
            <h3 class="announcement-title">{{ ann.title }}</h3>
            <p class="announcement-body" v-if="ann.body">{{ ann.body.substring(0, 120) }}{{ ann.body.length > 120 ? '…' : '' }}</p>
          </div>
        </template>
      </div>

      <!-- Interactive Campus Map -->
      <div class="seait-map-section">
        <h2 class="seait-map-title">Interactive Campus Map</h2>
        <div class="map-wrapper seait-embedded-map">
          <div class="map-container"
            ref="mapContainer"
            @wheel.prevent="handleZoom"
            @mousedown="startPan"
            @mousemove="handlePan"
            @mouseup="endPan"

            @mouseleave="endPan"
            @touchstart="startTouchPan"
            @touchmove="handleTouchPan"
            @touchend="endPan"
          >
            <div class="map-content"
              :style="mapTransformStyle"
            >
              <div class="campus-map-wrapper">
                <img src="../assets/Map_labeled.svg" class="campus-map-image" alt="Campus Map" draggable="false"/>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Campus Image Gallery -->
      <div class="seait-gallery">
        <h2 class="gallery-title">Campus Gallery</h2>
        <div class="gallery-grid">
          <div class="gallery-item">
            <img src="../assets/campus-1.jpg" alt="SEAIT Campus Aerial View 1" />
          </div>
          <div class="gallery-item">
            <img src="../assets/campus-2.jpg" alt="SEAIT Campus Aerial View 2" />
          </div>
          <div class="gallery-item">
            <img src="../assets/campus-3.jpg" alt="SEAIT Campus Aerial View 3" />
          </div>
          <div class="gallery-item">
            <img src="../assets/campus-4.jpg" alt="SEAIT Campus Aerial View 4" />
          </div>
          <div class="gallery-item gallery-item-wide">
            <img src="../assets/campus-5.jpg" alt="SEAIT Campus Panoramic View" />
          </div>
        </div>
      </div>

    </div>

    <!-- Bottom controls - MOBILE ONLY -->
    <div class="bottom-controls mobile-only">
      <!-- Action Pill Buttons -->
      <div class="home-action-pills">
        <button class="home-pill-btn home-pill-notifications" @click="goToNotifications">
          <span class="material-icons">notifications</span>
          <span class="home-pill-label">Alerts</span>
          <span v-if="unreadNotifications > 0" class="home-pill-badge">
            {{ unreadNotifications > 9 ? '9+' : unreadNotifications }}
          </span>
        </button>
        <button class="home-pill-btn home-pill-chatbot" @click="goToChatbot">
          <span class="material-icons">smart_toy</span>
          <span class="home-pill-label">Ask AI</span>
        </button>
        <button class="home-pill-btn home-pill-rating" @click="openRateApp">
          <span class="material-icons">star_rate</span>
          <span class="home-pill-label">Rate</span>
        </button>
      </div>

      <!-- Menu and action buttons -->
      <div class="action-row">
        <button class="menu-btn" @click="showMenu = true">
          <span class="material-icons">menu</span>
        </button>
      </div>
    </div>

    <!-- Slide-up Menu Sheet -->
    <div v-if="showMenu" class="menu-sheet-overlay" @click="showMenu = false">
      <div class="menu-sheet" @click.stop>
        <div class="menu-sheet-header">
          <div class="menu-sheet-handle"></div>
          <h3>Menu</h3>
        </div>
        <div class="menu-sheet-content">
          <!-- Quick Nav Grid -->
          <div class="menu-quick-nav">
            <button class="menu-quick-item" @click="() => { showMenu = false; router.push('/map') }">
              <span class="material-icons">map</span>
              <span>Map</span>
            </button>
            <button class="menu-quick-item" @click="() => { showMenu = false; router.push('/navigate') }">
              <span class="material-icons">directions</span>
              <span>Navigate</span>
            </button>
            <button class="menu-quick-item" @click="() => { showMenu = false; router.push('/favorites') }">
              <span class="material-icons">favorite</span>
              <span>Favorites</span>
            </button>
            <button class="menu-quick-item" @click="() => { showMenu = false; router.push('/feedback') }">
              <span class="material-icons">feedback</span>
              <span>Feedback</span>
            </button>
          </div>
          <div class="menu-divider"></div>
          <div class="menu-item" @click="goToBuildingInfo">
            <div class="menu-item-icon">
              <span class="material-icons">business</span>
            </div>
            <span>Building Information</span>
          </div>
          <div class="menu-divider"></div>
          <div class="menu-item" @click="openLink('https://www.facebook.com/profile.php?id=61559175458971')">
            <div class="menu-item-icon">
              <span class="material-icons">local_police</span>
            </div>
            <span>Safety Office & Security</span>
          </div>
          <div class="menu-item" @click="openLink('https://www.facebook.com/search/top?q=silakbo')">
            <div class="menu-item-icon">
              <span class="material-icons">group</span>
            </div>
            <span>Silakbo</span>
          </div>
          <div class="menu-item" @click="openLink('https://www.facebook.com/SEAITOfficial')">
            <div class="menu-item-icon">
              <span class="material-icons">school</span>
            </div>
            <span>SEAIT Official</span>
          </div>
        </div>
        <div class="menu-sheet-footer">
          <button class="menu-close-btn" @click="showMenu = false">
            <span class="material-icons">close</span>
            Close
          </button>
        </div>
      </div>
    </div>

    <!-- Locate Dialog -->
    <div v-if="showLocate" class="modal-overlay" @click="showLocate = false">
      <div class="dialog" @click.stop>
        <h3>Where are you now?</h3>
        <input
          v-model="locateInput"
          type="text"
          placeholder="Enter your current location"
        />
        <div class="dialog-actions">
          <button @click="showLocate = false">Cancel</button>
          <button class="primary" @click="setLocation">Set Location</button>
        </div>
      </div>
    </div>

    <!-- Rating Dialog -->
    <div v-if="showRating" class="modal-overlay" @click="showRating = false">
      <div class="dialog" @click.stop>
        <h3>Rate this App</h3>
        <div class="star-rating">
          <span
            v-for="n in 5"
            :key="n"
            class="star material-icons"
            :class="{ filled: n <= rating }"
            @click="rating = n"
          >
            {{ n <= rating ? 'star' : 'star_border' }}
          </span>
        </div>
        <textarea
          v-model="ratingComment"
          placeholder="Leave a comment (optional)"
          rows="3"
        ></textarea>
        <div class="dialog-actions">
          <button @click="showRating = false">Cancel</button>
          <button class="primary" @click="submitRating">Submit</button>
        </div>
      </div>
    </div>

    <!-- Search Results Dialog -->
    <div v-if="searchResults.length > 0" class="modal-overlay" @click="searchResults = []">
      <div class="dialog results-dialog" @click.stop>
        <h3>Search Results ({{ searchResults.length }})</h3>
        <div class="results-list">
          <div
            v-for="result in searchResults"
            :key="result.name"
            class="result-item"
            @click="selectSearchResult(result)"
          >
            <div class="result-icon">
              <span class="material-icons" style="color: #FF9800;">
                {{ result.type === 'Facility' ? 'business' : 'meeting_room' }}
              </span>
            </div>
            <div class="result-info">
              <div class="result-name">{{ result.name }}</div>
              <div class="result-type">{{ result.type }} - {{ result.info }}</div>
            </div>
          </div>
        </div>
        <button class="close-btn" @click="searchResults = []">Close</button>
      </div>
    </div>

    <!-- Chatbot Overlay Sheet -->
    <BottomSheetOverlay v-model="showChatbotSheet" max-height="90vh">
      <div class="sheet-inner-scroll">
        <ChatbotView :embedded="true" @close="showChatbotSheet = false" />
      </div>
    </BottomSheetOverlay>

    <!-- Notifications Overlay Sheet -->
    <BottomSheetOverlay v-model="showNotificationsSheet" max-height="88vh">
      <div class="sheet-inner-scroll">
        <NotificationsView :embedded="true" @close="showNotificationsSheet = false" />
      </div>
    </BottomSheetOverlay>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import offlineData from '../services/offlineData.js'
import { useSyncStore } from '../stores/syncStore.js'
import { useAuthStore } from '../stores/authStore.js'
import { showToast } from '../services/toast.js'
import OnboardingTutorial from '../components/OnboardingTutorial.vue'
import { isOnline } from '../services/sync.js'
import api from '../services/api.js'
import useMapPanZoom from '../composables/useMapPanZoom.js'
import BottomSheetOverlay from '../components/BottomSheetOverlay.vue'
import ChatbotView from './ChatbotView.vue'
import NotificationsView from './NotificationsView.vue'
import { registerBones } from 'boneyard-js'
import AppSkeleton from '../components/AppSkeleton.vue'

registerBones({
  'home-announcement': {
    width: 400, height: 90,
    bones: [
      { x: 0, y: 0,  w: 22, h: 18, r: 9 },
      { x: 0, y: 26, w: 68, h: 16, r: 6 },
      { x: 0, y: 50, w: 90, h: 12, r: 5 },
      { x: 0, y: 68, w: 72, h: 12, r: 5 },
    ]
  }
})

const router = useRouter()
const route = useRoute()
const syncStore = useSyncStore()
const authStore = useAuthStore()

// Data
const facilities = ref([])
const rooms = ref([])
const instructors = ref([])
const employees = ref([])
const departments = ref([])
// const mapMarkers = ref([]) // Disabled - markers removed from map
const selectedFacility = ref('')
const selectedRoom = ref('')
const isFacilitiesExpanded = ref(false)
const isRoomsExpanded = ref(false)
const searchText = ref('')
const currentLocation = ref('')
const unreadNotifications = ref(0)
const showMenu = ref(false)
const showLocate = ref(false)
const showRating = ref(false)
const locateInput = ref('')
const rating = ref(5)
const ratingComment = ref('')
const searchResults = ref([])
const recentSearches = ref([])
const searchSuggestions = ref([])
let searchDebounceTimer = null
const selectedMarker = ref(null)
const isMarkerInfoVisible = ref(false)

// Map zoom and pan — use shared composable
const mapContainer = ref(null)

const {

  scale, translateX, translateY,

  transformStyle: mapTransformStyle,

  zoomIn, zoomOut,

  onPointerDown: startPan,

  onPointerMove: handlePan,

  onPointerUp: endPan,

  onWheel: handleZoom,

  onTouchStart: startTouchPan,

  onTouchMove: handleTouchPan,

  initTransform

} = useMapPanZoom()



// Filtered markers - DISABLED (markers removed from map view)

// const filteredMarkers = computed(() => {

//   if (!selectedFacility.value && !selectedRoom.value) {

//     return mapMarkers.value

//   }

//   return mapMarkers.value.filter(marker => {

//     if (selectedFacility.value && marker.marker_type === 'facility') {

//       return marker.name === selectedFacility.value

//     }

//     if (selectedRoom.value && marker.marker_type === 'room') {

//       return marker.name === selectedRoom.value

//     }

//     return true

//   })

// })



// Methods

const loadData = async () => {

  try {

    // Use offline-aware data service

    const [facilitiesRes, roomsRes] = await Promise.all([

      offlineData.getFacilities(),

      offlineData.getRooms()

      // offlineData.getMapMarkers() // Disabled - markers removed

    ])

    

    facilities.value = facilitiesRes.data

    rooms.value = roomsRes.data

    // mapMarkers.value = markerRes.data // Disabled - markers removed

    

    // Load additional data for global search

    await loadAdditionalSearchData()

    

    // Log data source for debugging

    console.log(`[HomeView] Data loaded - Facilities: ${facilitiesRes.source}, Rooms: ${roomsRes.source}`)

    

    // If any data came from cache and is stale, show a subtle notification

    if (facilitiesRes.stale || roomsRes.stale) {

      console.log('[HomeView] Using cached data - will sync when connection is available')

    }

    

    // Try to load search history from API if online

    if (isOnline()) {

      try {

        const searchRes = await api.get('/core/search-history/')

        recentSearches.value = searchRes.data.slice(0, 10)

      } catch {

        // Silently fail for search history

      }

    }

  } catch (error) {

    console.error('Error loading data:', error)

    // Final fallback mock data

    useFallbackData()

  }

}



const useFallbackData = () => {

  facilities.value = [

    { id: 1, name: 'Library', description: 'Main Campus Library' },

    { id: 2, name: 'Gymnasium', description: 'School Sports and Recreation Center' },

    { id: 3, name: 'Cafeteria', description: 'Main Campus Dining Hall' },

    { id: 4, name: 'Registrar Office', description: 'Student Services and Records' },

    { id: 5, name: 'CL1', description: 'Classroom Building 1' },

  ]

  rooms.value = []

  // mapMarkers disabled - markers removed from map

  // mapMarkers.value = [

  //   { id: 1, name: 'Library', marker_type: 'facility', x_position: 0.2, y_position: 0.5 },

  //   { id: 2, name: 'Registrar Office', marker_type: 'facility', x_position: 0.7, y_position: 0.5 },

  //   { id: 3, name: 'Cafeteria', marker_type: 'facility', x_position: 0.8, y_position: 0.7 },

  //   { id: 4, name: 'Gymnasium', marker_type: 'facility', x_position: 0.15, y_position: 0.8 },

  //   { id: 5, name: 'CL1', marker_type: 'facility', x_position: 0.5, y_position: 0.6 },

  // ]

}



const getMarkerStyle = (marker) => ({

  left: `${marker.x_position * 100}%`,

  top: `${marker.y_position * 100}%`,

  color: marker.marker_type === 'facility' ? '#FF9800' : '#4CAF50'

})



const handleDeepLink = () => {

  const source = route.query.source

  const location = route.query.location

  const welcome = route.query.welcome

  

  // Handle welcome parameter for first-time visitors

  if (welcome === 'true') {

    showToast('Welcome to SEAIT Campus! Use the map to find your way around.', 'success', 5000)

    // Default to first facility

    if (facilities.value.length > 0 && !selectedFacility.value) {

      selectedFacility.value = facilities.value[0].name

    }

    return

  }

  

  // Default facility and room selection

  if (facilities.value.length > 0 && !selectedFacility.value) selectedFacility.value = facilities.value[0].name

  if (rooms.value.length > 0 && !selectedRoom.value) selectedRoom.value = rooms.value[0].name

}



watch(() => route.query, () => {

  handleDeepLink()

})



const loadNotificationCount = async () => {

  try {

    const res = await api.get('/notifications/')

    unreadNotifications.value = res.data.filter(n => !n.is_read).length

  } catch (error) {

    console.error('Error loading notifications:', error)

  }

}



const toggleFacilities = () => {

  isFacilitiesExpanded.value = !isFacilitiesExpanded.value

  if (isFacilitiesExpanded.value) isRoomsExpanded.value = false

}



const toggleRooms = () => {

  isRoomsExpanded.value = !isRoomsExpanded.value

  if (isRoomsExpanded.value) isFacilitiesExpanded.value = false

}



// Filtered rooms based on selected facility

const filteredRooms = computed(() => {

  if (!selectedFacility.value) {

    return rooms.value

  }

  return rooms.value.filter(room => {

    // Support both facility name and facility_id matching

    const roomFacility = room.facility || room.facility_name

    const roomFacilityId = room.facility_id

    

    // Check if room belongs to selected facility by name

    if (roomFacility === selectedFacility.value) return true

    

    // Check if room belongs by facility_id - find facility ID

    const facility = facilities.value.find(f => f.name === selectedFacility.value)

    if (facility && roomFacilityId === facility.id) return true

    

    return false

  })

})



const selectFacility = (name) => {

  selectedFacility.value = name

  isFacilitiesExpanded.value = false

  // Reset room selection if current room is not in this facility

  if (selectedRoom.value) {

    const roomInFacility = filteredRooms.value.find(r => r.name === selectedRoom.value)

    if (!roomInFacility) {

      selectedRoom.value = ''

    }

  }

}



const clearFilters = () => {

  selectedFacility.value = ''

  selectedRoom.value = ''

}



const selectRoom = (name) => {

  selectedRoom.value = name

  isRoomsExpanded.value = false

  // Auto-select the parent facility

  const room = rooms.value.find(r => r.name === name)

  if (room && room.facility) {

    selectedFacility.value = room.facility

  }

}



const showMarkerInfo = (marker) => {

  selectedMarker.value = marker

  isMarkerInfoVisible.value = true

}



const closeMarkerInfo = () => {

  isMarkerInfoVisible.value = false

  selectedMarker.value = null

}



const addToFavorites = () => {

  if (!selectedMarker.value) return

  

  const marker = selectedMarker.value

  const favorites = JSON.parse(localStorage.getItem('tp_favorites') || '[]')

  

  // Generate composite key to prevent ID collisions between views

  const compositeId = `${marker.marker_type}_${marker.id || marker.name}`

  

  // Check if already in favorites using composite ID

  if (favorites.some(f => f.id === compositeId)) {

    showToast('This location is already in your favorites!', 'info')

    return

  }

  

  // Add to favorites with composite ID

  favorites.push({

    id: compositeId,

    name: marker.name,

    type: marker.marker_type,

    description: marker.description || marker.marker_type,

    addedAt: new Date().toISOString()

  })

  

  localStorage.setItem('tp_favorites', JSON.stringify(favorites))

  showToast(`${marker.name} added to favorites!`, 'success')

}



const navigateToMarker = () => {

  if (!selectedMarker.value) return

  router.push({

    path: '/navigate',

    query: { to: selectedMarker.value.name }

  })

  closeMarkerInfo()

}



const showLocateDialog = () => {

  locateInput.value = currentLocation.value

  showLocate.value = true

}



const setLocation = () => {

  currentLocation.value = locateInput.value

  showLocate.value = false

}



const showRatingDialog = () => {

  rating.value = 5

  ratingComment.value = ''

  showRating.value = true

}



const ratingHint = computed(() => {
  const hints = ['', 'Very Poor', 'Poor', 'Okay', 'Good', 'Excellent']
  return hints[rating.value] || ''
})

const submitRating = async () => {
  try {
    await api.post('/core/ratings/', {
      rating: rating.value,
      comment: ratingComment.value,
      category: 'app'
    })
    showRating.value = false
    showToast('Thank you for your rating!', 'success')
  } catch (error) {
    console.error('Error submitting rating:', error)
  }
}



// Search suggestions with debouncing

const updateSearchSuggestions = () => {

  if (!searchText.value) {

    searchSuggestions.value = []

    return

  }

  

  const query = searchText.value.toLowerCase()

  const allItems = [

    ...facilities.value.map(f => ({ name: f.name, type: 'Facility', info: f.description || 'Campus facility', icon: 'business' })),

    ...rooms.value.map(r => ({ name: r.name, type: 'Room', info: r.description || 'Classroom/Lab', icon: 'meeting_room' })),

    ...instructors.value.map(i => ({ name: i.name, type: 'Instructor', info: i.department || 'Faculty', icon: 'school' })),

    ...employees.value.map(e => ({ name: e.name, type: 'Employee', info: e.department || 'Staff', icon: 'person' })),

    ...departments.value.map(d => ({ name: d.name || d.code, type: 'Department', info: 'Academic Department', icon: 'account_balance' }))

  ]

  

  searchSuggestions.value = allItems.filter(item => {

    return item.name.toLowerCase().includes(query) || 

           item.info.toLowerCase().includes(query)

  }).slice(0, 8)

}



const debouncedSearch = () => {

  clearTimeout(searchDebounceTimer)

  searchDebounceTimer = setTimeout(updateSearchSuggestions, 200) // 200ms debounce

}



const selectSuggestion = (suggestion) => {

  searchText.value = suggestion.name

  searchSuggestions.value = []

  // Navigate based on item type

  switch (suggestion.type) {

    case 'Facility':

      router.push(`/info/buildings`)

      break

    case 'Room':

      router.push(`/info/rooms`)

      break

    case 'Instructor':

      router.push(`/instructor-info`)

      break

    case 'Employee':

      router.push('/employees')

      break

    case 'Department':

      router.push('/info/departments')

      break

    default:

      performSearch()

  }

}



const performSearch = async () => {

  if (!searchText.value) return

  

  const query = searchText.value.toLowerCase()

  const allItems = [

    ...facilities.value.map(f => ({ name: f.name, type: 'Facility', info: f.description || 'Campus facility' })),

    ...rooms.value.map(r => ({ name: r.name, type: 'Room', info: r.description || 'Classroom/Lab' })),

    ...instructors.value.map(i => ({ name: i.name, type: 'Instructor', info: i.department || 'Faculty' })),

    ...employees.value.map(e => ({ name: e.name, type: 'Employee', info: e.department || 'Staff' })),

    ...departments.value.map(d => ({ name: d.name || d.code, type: 'Department', info: 'Academic Department' }))

  ]

  

  searchResults.value = allItems.filter(item => {

    return item.name.toLowerCase().includes(query) || 

           item.info.toLowerCase().includes(query)

  })

  

  // Save search to history if results found

  if (searchResults.value.length > 0) {

    try {

      await api.post('/core/search-history/', {

        query: searchText.value,

        results_count: searchResults.value.length,

        was_clicked: false

      })

      // Refresh recent searches

      const res = await api.get('/core/search-history/')

      recentSearches.value = res.data.slice(0, 10)

    } catch (error) {

      console.log('Failed to save search history')

    }

  }

  

  if (searchResults.value.length === 0) {

    showToast(`No locations found for "${searchText.value}"`, 'warning')

  }

}



const selectRecentSearch = (query) => {

  searchText.value = query

  performSearch()

}



const clearRecentSearches = async () => {

  try {

    // Delete each search history entry

    await Promise.all(recentSearches.value.map(search => 

      api.delete(`/core/search-history/${search.id}/`).catch(() => {})

    ))

    recentSearches.value = []

  } catch (error) {

    console.error('Error clearing search history:', error)

    recentSearches.value = []

  }

}



const selectSearchResult = (result) => {

  if (result.type === 'Facility') {

    selectedFacility.value = result.name

  } else {

    selectedRoom.value = result.name

  }

  searchResults.value = []

  searchText.value = ''

}



// Load additional search data (instructors, employees, departments)
const loadAdditionalSearchData = async () => {
  try {
    // Fetch instructors from directory (public endpoint)
    const instructorsRes = await api.get('/users/directory/?role=instructor').catch(() => ({ data: [] }))
    instructors.value = instructorsRes.data || []
    
    // Fetch employees from directory (public endpoint)
    const employeesRes = await api.get('/users/directory/?role=staff').catch(() => ({ data: [] }))
    employees.value = employeesRes.data || []
    
    // Fetch departments
    const departmentsRes = await api.get('/core/departments/').catch(() => ({ data: [] }))
    departments.value = departmentsRes.data || []
    
    console.log(`[HomeView] Additional data loaded - Instructors: ${instructors.value.length}, Employees: ${employees.value.length}, Departments: ${departments.value.length}`)
  } catch (error) {
    console.log('[HomeView] Failed to load additional search data:', error)
  }
}

// Navigation
const showChatbotSheet = ref(false)
const showNotificationsSheet = ref(false)

const goToNotifications = () => { showNotificationsSheet.value = true }
const goToChatbot = () => { showChatbotSheet.value = true }

const goToBuildingInfo = () => { showMenu.value = false; router.push('/building-info') }

const goToRoomsInfo = () => { showMenu.value = false; router.push('/rooms-info') }

const goToInstructorInfo = () => { showMenu.value = false; router.push('/instructor-info') }

const goToEmployees = () => { showMenu.value = false; router.push('/employees') }

const goToAdmin = () => { showMenu.value = false; router.push('/admin') }

const goToNavGraph = () => { showMenu.value = false; router.push({ path: '/admin', query: { section: 'navigation' } }) }

const openRateApp = () => { showMenu.value = false; showRating.value = true }

const openLink = (url) => { showMenu.value = false; window.open(url, '_blank') }



const onboardingRef = ref(null)

const showOnboarding = ref(false)

// Announcements feed
const announcementsRef = ref([])
const announcementsLoading = ref(true)

async function loadAnnouncements() {
  announcementsLoading.value = true
  try {
    const res = await api.get('/announcements/')
    announcementsRef.value = (res.data || [])
      .filter(a => a.status === 'published')
      .slice(0, 3) // Show max 3 on home
  } catch { /* silent fail */ } finally {
    announcementsLoading.value = false
  }
}

function getDeptColor(colorName) {
  const colors = {
    orange: '#FF9800', teal: '#009688', blue: '#2196F3',
    green: '#4CAF50', red: '#F44336', purple: '#9C27B0',
    amber: '#FFC107', charcoal: '#607D8B', dark_blue: '#1565C0',
    brown: '#795548', indigo: '#3F51B5', dark_green: '#2E7D32',
  }
  return colors[colorName] || '#FF9800'
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return d.toLocaleDateString('en-PH', { month: 'short', day: 'numeric', year: 'numeric' })
}



const onOnboardingComplete = () => {

  localStorage.setItem('tp_onboarding_completed', 'true')

  localStorage.setItem('tp_onboarding_completed_at', Date.now().toString())

  showOnboarding.value = false

}



const onOnboardingSkip = () => {

  localStorage.setItem('tp_onboarding_completed', 'true')

  localStorage.setItem('tp_onboarding_completed_at', Date.now().toString())

  showOnboarding.value = false

}



// Lifecycle

onMounted(async () => {
  await loadData()
  handleDeepLink()
  loadNotificationCount()
  loadAnnouncements()

  if (!syncStore.lastSyncedAt) {
    syncStore.sync()
  }

  // Note: Removed 5-second aggressive polling

  // sync.js handles periodic sync (30s interval) which includes notifications

  

  // Check if onboarding should be shown (only first time)

  const onboardingCompleted = localStorage.getItem('tp_onboarding_completed')

  if (!onboardingCompleted) {

    showOnboarding.value = true

  }

})

</script>

<style>
/* Styles moved to external file: src/assets/homeview.css */
@import '../assets/homeview.css';

/* Action Pill Buttons */
.home-action-pills {
  display: flex;
  gap: 8px;
  padding: 0 4px;
  justify-content: flex-end;
}

.home-pill-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 16px;
  border: none;
  border-radius: 99px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  position: relative;
  transition: transform 0.15s, box-shadow 0.15s;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}
.home-pill-btn:active { transform: scale(0.96); }
.home-pill-btn .material-icons { font-size: 18px; }

.home-pill-notifications {
  background: var(--color-primary, #FF9800);
  color: #fff;
}
.home-pill-chatbot {
  background: #1565C0;
  color: #fff;
}
.home-pill-rating {
  background: #fff;
  color: var(--color-primary, #FF9800);
  border: 1.5px solid var(--color-primary, #FF9800);
}
.home-pill-badge {
  position: absolute;
  top: -4px; right: -4px;
  background: #F44336;
  color: #fff;
  font-size: 10px;
  font-weight: 700;
  padding: 2px 5px;
  border-radius: 99px;
  min-width: 18px;
  text-align: center;
}

/* Menu Quick Nav */
.menu-quick-nav {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
  padding: 8px 0 16px;
}
.menu-quick-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding: 14px 8px;
  background: var(--color-surface, #f5f5f5);
  border: none;
  border-radius: 16px;
  font-size: 11px;
  font-weight: 600;
  color: var(--color-primary-text, #333);
  cursor: pointer;
  transition: background 0.15s;
}
.menu-quick-item:active { background: var(--color-surface-2, #e0e0e0); }
.menu-quick-item .material-icons {
  font-size: 24px;
  color: var(--color-primary, #FF9800);
}

/* Sheet Inner Scroll */
.sheet-inner-scroll {
  flex: 1;
  overflow-y: auto;
  overscroll-behavior: contain;
  -webkit-overflow-scrolling: touch;
}

/* Announcement Skeleton */
.home-announcement-sk-wrap {
  height: 90px;
  margin-bottom: 12px;
  border-radius: 12px;
  overflow: hidden;
}

/* Announcements Section */
.home-announcements { padding: 16px; }
.home-section-title {
  display: flex; align-items: center; gap: 8px;
  font-size: 18px; font-weight: 600;
  color: var(--color-primary-text, #333);
  margin-bottom: 12px;
}
.announcement-card {
  background: var(--color-bg, #fff);
  border-radius: 16px;
  padding: 16px;
  margin-bottom: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  border-left: 4px solid var(--color-primary, #FF9800);
}
.announcement-header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 8px;
}
.announcement-dept-chip {
  font-size: 11px; font-weight: 600; color: #fff;
  padding: 3px 10px; border-radius: 99px; letter-spacing: 0.3px;
}
.announcement-date { font-size: 12px; color: var(--color-text-secondary, #666); }
.announcement-title { font-size: 15px; font-weight: 600; margin-bottom: 6px; }
.announcement-body { font-size: 13px; color: var(--color-text-secondary, #666); line-height: 1.5; }

/* Rating Sheet Styles */
.rating-sheet-content {
  padding: 20px 24px 32px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}
.rating-sheet-title {
  font-size: 20px;
  font-weight: 700;
  color: var(--color-primary-text, #333);
}
.star-rating { display: flex; gap: 8px; }
.star { font-size: 40px; cursor: pointer; color: #ccc; transition: color 0.15s; }
.star.filled { color: #FF9800; }
.rating-hint { font-size: 14px; color: var(--color-text-secondary, #666); min-height: 20px; }
.rating-textarea {
  width: 100%;
  border: 1px solid var(--color-border, #e0e0e0);
  border-radius: 12px;
  padding: 12px;
  font-size: 14px;
  resize: none;
  font-family: inherit;
}
.rating-actions { display: flex; gap: 12px; width: 100%; }
.rating-cancel-btn {
  flex: 1;
  padding: 14px;
  border: 1px solid var(--color-border, #e0e0e0);
  border-radius: 12px;
  background: transparent;
  font-size: 15px;
  cursor: pointer;
}
.rating-submit-btn {
  flex: 2;
  padding: 14px;
  border: none;
  border-radius: 12px;
  background: var(--color-primary, #FF9800);
  color: #fff;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
}
</style>

