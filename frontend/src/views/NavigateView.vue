<template>
  <div class="svg-navigate-view">
    <!-- Top bar -->
    <header class="svg-nav-header">
      <div class="svg-nav-header-content">
        <div class="svg-nav-header-icon">
          <span class="material-icons">explore</span>
        </div>
        <div class="svg-nav-header-text">
          <h1>Navigate</h1>
          <p>Find your way around campus</p>
        </div>
      </div>
    </header>

    <!-- Destination Info Panel (bottom, only during navigation) -->
    <div
      class="dest-info-panel"
      v-if="isNavigating && currentPath"
      :class="{ 'minimized': isDestPreviewMinimized }"
    >
      <div class="dest-info-header" @click="isDestPreviewMinimized = !isDestPreviewMinimized">
        <div class="dest-info-header-main">
          <div class="dest-info-from">
            <span class="dest-info-label-small">From:</span>
            <span class="dest-info-value-small">{{ getLocationName(fromLocation) || 'Start' }}</span>
          </div>
          <span class="dest-info-arrow">→</span>
          <div class="dest-info-to">
            <span class="dest-info-label">TO:</span>
            <span class="dest-info-name">{{ currentPath?.name || getLocationName(toLocation) || 'Destination' }}</span>
          </div>
        </div>
        <button class="dest-info-toggle">
          <span class="material-icons">{{ isDestPreviewMinimized ? 'expand_less' : 'expand_more' }}</span>
        </button>
      </div>
      <!-- Collapsible Content -->
      <div class="dest-info-content" v-show="!isDestPreviewMinimized">
        <!-- Facility Field -->
        <div class="dest-info-field" v-if="currentPath?.facility">
          <span class="dest-info-field-label">Facility:</span>
          <span class="dest-info-field-value">{{ currentPath?.facility }}</span>
        </div>
        <!-- Room & Floor Grid -->
        <div class="dest-info-grid" v-if="currentPath?.room || currentPath?.floor">
          <div class="dest-info-field" v-if="currentPath?.room">
            <span class="dest-info-field-label">Room:</span>
            <span class="dest-info-field-value">{{ currentPath?.room }}</span>
          </div>
          <div class="dest-info-field" v-if="currentPath?.floor">
            <span class="dest-info-field-label">Floor:</span>
            <span class="dest-info-field-value">{{ currentPath?.floor }}</span>
          </div>
        </div>
        <!-- Description Field -->
        <div class="dest-info-field" v-if="currentPath?.description">
          <span class="dest-info-field-label">Description:</span>
          <span class="dest-info-field-value">{{ currentPath?.description }}</span>
        </div>
      </div>
    </div>

    <!-- Location Selection Panel -->
    <div class="svg-nav-panel" v-if="!isNavigating">
      <!-- Loading or no paths message -->
      <div v-if="availablePaths.length === 0" class="svg-nav-empty">
        <span class="material-icons" style="font-size: 48px; color: #ccc;">map</span>
        <p>No navigation paths available.</p>
        <p class="svg-nav-hint">Go to Admin Panel → Map Management → SVG Paths to create paths first.</p>
      </div>

      <div v-else-if="locations.length === 0" class="svg-nav-empty">
        <span class="material-icons" style="font-size: 48px; color: #ccc;">refresh</span>
        <p>Loading navigation paths...</p>
      </div>

      <template v-else>
        <!-- Top: From & To Location Dropdowns -->
        <div class="svg-nav-locations-top">
          <!-- From Location -->
          <div class="svg-nav-field svg-nav-field-compact">
            <select v-model="fromLocation" class="svg-nav-select">
              <option value="">From: Select location</option>
              <option v-for="location in fromLocations" :key="location.id" :value="location.id">
                {{ location.name }}
              </option>
            </select>
          </div>

          <!-- To Location -->
          <div class="svg-nav-field svg-nav-field-compact">
            <select 
              v-model="toLocation" 
              class="svg-nav-select"
              :disabled="!fromLocation"
            >
              <option value="">
                {{ fromLocation ? 'To: Select destination' : 'First select From location' }}
              </option>
              <option v-for="location in toLocations" :key="location.id" :value="location.id">
                {{ location.name }}
              </option>
            </select>
          </div>

          <!-- Start Button (inline) -->
          <button
            v-if="fromLocation && toLocation"
            class="svg-nav-start-btn svg-nav-start-btn-compact"
            @click="startNavigation"
            :disabled="!fromLocation || !toLocation"
          >
            <span class="material-icons">play_arrow</span>
          </button>
        </div>

      </template>
    </div>

    <div class="svg-nav-controls" v-if="isNavigating && currentStepInfo">
      <div class="svg-nav-progress">
        <span class="svg-nav-step-info">
          Step {{ (currentStepInfo.step ?? 0) + 1 }} of {{ currentStepInfo.totalSteps ?? 0 }}
        </span>
        <span class="svg-nav-current-location">{{ currentStepInfo.elementId ?? '-' }}</span>
      </div>
      
      <div class="svg-nav-buttons">
        <button 
          class="svg-nav-btn" 
          @click="previousStep" 
          :disabled="currentStepInfo.isFirst ?? true"
        >
          <span class="material-icons">skip_previous</span>
          Previous
        </button>
        
        <button class="svg-nav-btn svg-nav-stop" @click="stopNavigation">
          <span class="material-icons">stop</span>
          Stop
        </button>
        
        <button 
          class="svg-nav-btn" 
          @click="nextStep" 
          :disabled="currentStepInfo.isLast ?? true"
        >
          Next
          <span class="material-icons">skip_next</span>
        </button>
      </div>
    </div>

    <!-- SVG Map Container -->
    <div 
      class="svg-map-container" 
      ref="mapContainer" 
      @wheel="handleWheelZoom"
      @mousedown="startDrag"
      @mousemove="drag"
      @mouseup="endDrag"
      @mouseleave="endDrag"
      @touchstart="startDrag"
      @touchmove="drag"
      @touchend="endDrag"
      :class="{ 'is-dragging': isDragging }"
    >
      <svg 
        ref="svgMap"
        class="svg-map"
        :viewBox="viewBoxString"
        preserveAspectRatio="xMidYMid meet"
        xmlns="http://www.w3.org/2000/svg"
        :style="{ transform: `rotate(${rotation}deg)` }"
      >
        <!-- Map content will be loaded dynamically -->
        <g v-if="mapLoaded" v-html="safeSvgContent"></g>
        
        <!-- Navigation Path Overlay -->
        <g v-if="isNavigating && pathPositions.length > 0" class="nav-path-overlay">
          <!-- Connecting Lines with glow effect -->
          <polyline
            :points="pathPoints"
            fill="none"
            stroke="#FF9800"
            stroke-width="20"
            stroke-linecap="round"
            stroke-linejoin="round"
            opacity="0.9"
            filter="drop-shadow(0 0 10px rgba(255,152,0,0.8))"
          />
          <!-- Secondary outline for better visibility -->
          <polyline
            :points="pathPoints"
            fill="none"
            stroke="#FFF"
            stroke-width="10"
            stroke-linecap="round"
            stroke-linejoin="round"
            opacity="0.5"
          />
          
          <!-- Path Points -->
          <circle
            v-for="(pos, index) in pathPositions"
            :key="`point-${pos.id}-${index}`"
            :cx="pos.x"
            :cy="pos.y"
            :r="index === (currentStepInfo?.step ?? -1) ? 30 : 18"
            :fill="index === (currentStepInfo?.step ?? -1) ? '#FF5722' : '#4CAF50'"
            :stroke="'white'"
            :stroke-width="index === (currentStepInfo?.step ?? -1) ? 6 : 3"
            filter="drop-shadow(0 0 8px rgba(0,0,0,0.5))"
          />
          
          <!-- Labels - Only show for first and last point -->
          <text
            v-for="(pos) in endpointLabels"
            :key="`label-${pos.id}-${pos.index}`"
            :x="pos.x"
            :y="pos.y - 30"
            text-anchor="middle"
            fill="#333"
            font-size="24"
            font-weight="bold"
            style="text-shadow: 2px 2px 4px white;"
          >
            {{ pos.label }}
          </text>
        </g>

        <!-- Current Position Indicator -->
        <g v-if="isNavigating && currentPosition" class="current-position">
          <circle
            :cx="currentPosition.x"
            :cy="currentPosition.y"
            r="30"
            fill="none"
            stroke="#FF5722"
            stroke-width="4"
            opacity="0.5"
          >
            <animate
              attributeName="r"
              values="25;35;25"
              dur="1.5s"
              repeatCount="indefinite"
            />
            <animate
              attributeName="opacity"
              values="0.8;0.3;0.8"
              dur="1.5s"
              repeatCount="indefinite"
            />
          </circle>
        </g>
      </svg>

      <!-- Map Loading Skeleton + CometSpinner -->
      <div v-if="!mapLoaded && !mapError" class="svg-map-skeleton-wrap">
        <AppSkeleton :loading="true" name="navigate-map" animate="shimmer" wrap-class="map-sk-full" />
        <div class="map-sk-center">
          <CometSpinner size="52px" />
          <p class="map-sk-hint">Loading campus map…</p>
        </div>
      </div>

      <!-- Map Error State -->
      <div v-if="mapError" class="svg-map-error-state">
        <span class="material-icons">map_off</span>
        <p>{{ mapError }}</p>
      </div>
    </div>

    <!-- Floating Action Buttons - Positioned above bottom nav -->
    <div class="nav-fab-container" v-if="!isNavigating">
      <!-- Rotate Counter-Clockwise -->
      <button 
        class="nav-fab-btn nav-rotate-ccw-btn" 
        @click="rotateCounterClockwise"
        title="Rotate Left"
      >
        <span class="material-icons">rotate_left</span>
      </button>

      <!-- Rotate Clockwise -->
      <button 
        class="nav-fab-btn nav-rotate-cw-btn" 
        @click="rotateClockwise"
        title="Rotate Right"
      >
        <span class="material-icons">rotate_right</span>
      </button>

      <!-- Notifications -->
      <button 
        class="nav-fab-btn nav-notifications-btn" 
        @click="$router.push('/notifications')"
        title="Notifications"
      >
        <span class="material-icons">notifications</span>
        <span v-if="unreadCount > 0" class="nav-fab-badge">{{ unreadCount > 99 ? '99+' : unreadCount }}</span>
      </button>

      <!-- Rate -->
      <button 
        class="nav-fab-btn nav-rate-btn" 
        @click="$router.push('/feedback')"
        title="Rate & Feedback"
      >
        <span class="material-icons">star</span>
      </button>
      
      <!-- Chatbot -->
      <button
        class="nav-fab-btn nav-chatbot-btn"
        @click="$router.push('/chatbot')"
        title="Chatbot"
      >
        <span class="material-icons">smart_toy</span>
      </button>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import pathManager from '../services/pathManager.js'
import { useLocations } from '../composables/useLocations.js'
import api from '../services/api.js'
import { registerBones } from 'boneyard-js'
import AppSkeleton from '../components/AppSkeleton.vue'
import CometSpinner from '../components/CometSpinner.vue'
import DOMPurify from 'dompurify'

registerBones({
  'navigate-map': {
    width: 390, height: 520,
    bones: [
      { x: 0, y: 0,   w: 100, h: 48,  r: 24 },
      { x: 0, y: 56,  w: 100, h: 340, r: 16 },
      { x: 0, y: 404, w: 100, h: 72,  r: 16 },
      { x: 4, y: 420, w: 50,  h: 16,  r: 6  },
      { x: 4, y: 442, w: 32,  h: 12,  r: 5  },
    ]
  }
})

// DOM References
const mapContainer = ref(null)
const svgMap = ref(null)

// State
const mapLoaded = ref(false)
const svgContent = ref('')
const fromLocation = ref('')
const toLocation = ref('') // Single TO location
const viewBox = ref({ x: 0, y: 0, width: 3306, height: 7159 })
const ORIGINAL_VIEWBOX = { width: 3306, height: 7159 }
const zoomLevel = ref(1)
const rotation = ref(0)
const pathPositions = ref([])
const unreadCount = ref(0)

// Load notification count from API
const loadNotificationCount = async () => {
  try {
    const res = await api.get('/notifications/')
    unreadCount.value = res.data.filter(n => !n.is_read).length
  } catch (error) {
    console.error('Error loading notifications:', error)
    unreadCount.value = 0
  }
}
const mapError = ref(null)

// Sanitize SVG content for safe v-html rendering
const safeSvgContent = computed(() =>
  DOMPurify.sanitize(svgContent.value || '', {
    USE_PROFILES: { svg: true },
    ADD_TAGS: ['use', 'symbol', 'defs', 'clipPath'],
  })
)

// Destination info panel minimized state
const isDestPreviewMinimized = ref(false)

onMounted(() => {
  // Component mounted
})

onUnmounted(() => {
  // Component unmounted
})

// Use shared locations composable (connects to AdminNavGraph)
const { locations, getLocationName, extractFromSVG, extractLocationsFromPaths } = useLocations()

// Show From and To endpoints (first and last points of paths)
// Allow any valid string ID
const validLocation = (l) => {
  return l && l.id && typeof l.id === 'string' && l.id.trim() !== ''
}


const fromLocations = computed(() => {
  const endpoints = locations.value.filter(l => l.subtype === 'from' && validLocation(l))
  return endpoints.length > 0 ? endpoints : locations.value.filter(validLocation)
})

// Filter TO locations based on selected FROM location
const toLocations = computed(() => {
  if (!fromLocation.value) {
    // No From selected yet - show all available destinations or empty
    return []
  }
  
  // Find all paths that start from the selected From location
  const pathsFromSelected = availablePaths.value.filter(p => {
    // Check if path starts with the selected From location
    if (p.elementIds && p.elementIds.length >= 2) {
      return p.elementIds[0] === fromLocation.value
    }
    // Fallback: check from field
    return p.from === fromLocation.value
  })
  
  // Extract unique destination IDs from these paths
  const destinationIds = new Set()
  pathsFromSelected.forEach(p => {
    if (p.elementIds && p.elementIds.length >= 2) {
      // Add all destinations except the first one (which is the From)
      p.elementIds.slice(1).forEach(id => destinationIds.add(id))
    }
    // Also check the 'to' field if it exists
    if (p.to) {
      destinationIds.add(p.to)
    }
  })
  
  // Convert to location objects
  const destinations = Array.from(destinationIds).map(id => {
    const loc = locations.value.find(l => l.id === id)
    if (loc) return loc
    // Create a basic location object if not found in locations list
    return { id, name: id }
  }).filter(Boolean)
  
  return destinations
})

// Drag/Pan state
const isDragging = ref(false)
const dragStart = ref({ x: 0, y: 0 })
const viewBoxStart = ref({ x: 0, y: 0 })

// Get path manager state
const isNavigating = computed(() => pathManager.isNavigating.value)
const currentPath = computed(() => pathManager.currentPath.value)
const currentStepInfo = computed(() => {
  return pathManager.getCurrentStep() || {
    step: 0,
    totalSteps: 0,
    elementId: '',
    isFirst: true,
    isLast: true
  }
})

// Available paths
const availablePaths = computed(() => pathManager.getAllPaths())

// ViewBox string for SVG attribute
const viewBoxString = computed(() => {
  return `${viewBox.value.x} ${viewBox.value.y} ${viewBox.value.width} ${viewBox.value.height}`
})

// Current position based on step
const currentPosition = computed(() => {
  if (!isNavigating.value || pathPositions.value.length === 0) return null
  if (!currentStepInfo.value || currentStepInfo.value.step == null) return null
  const pos = pathPositions.value[currentStepInfo.value.step]
  if (!pos || pos.x == null || pos.y == null || isNaN(pos.x) || isNaN(pos.y)) return null
  return pos
})

// Path points for polyline
const pathPoints = computed(() => {
  if (pathPositions.value.length === 0) return ''
  return pathPositions.value
    .filter(p => !p.notFound && p.x != null && p.y != null && !isNaN(p.x) && !isNaN(p.y))
    .map(p => `${p.x},${p.y}`)
    .join(' ')
})

// Only show labels for first and last points (From and To) - middle stops are invisible
const endpointLabels = computed(() => {
  if (pathPositions.value.length === 0) return []
  const labels = []
  // Only add first point (FROM)
  if (pathPositions.value.length > 0) {
    const first = pathPositions.value[0]
    if (first && first.x != null && first.y != null && !isNaN(first.x) && !isNaN(first.y)) {
      labels.push({ ...first, index: 0, label: 'From: ' + first.id })
    }
  }
  // Only add last point (TO) if different from first
  if (pathPositions.value.length > 1) {
    const last = pathPositions.value[pathPositions.value.length - 1]
    // Skip if last is same as first (single point path)
    if (last && last.id !== pathPositions.value[0].id && last.x != null && last.y != null && !isNaN(last.x) && !isNaN(last.y)) {
      labels.push({ ...last, index: pathPositions.value.length - 1, label: 'To: ' + last.id })
    }
  }
  return labels
})

// Load SVG map
const loadMap = async () => {
  console.log('[NavigateView] Starting to load map...')
  try {
    // Load SVG file
    const response = await fetch('Map_labeled.svg')
    console.log('[NavigateView] Map response:', response.status, response.ok)
    if (!response.ok) throw new Error(`Failed to load map: ${response.status}`)
    
    const svgText = await response.text()
    
    // Extract inner content from SVG
    const parser = new DOMParser()
    const doc = parser.parseFromString(svgText, 'image/svg+xml')
    const svg = doc.querySelector('svg')
    
    if (svg) {
      // Get viewBox from original SVG
      const originalViewBox = svg.getAttribute('viewBox')
      if (originalViewBox) {
        const [x, y, width, height] = originalViewBox.split(' ').map(Number)
        viewBox.value = { x, y, width, height }
      }
      
      // Extract inner content
      svgContent.value = svg.innerHTML
      mapLoaded.value = true
      
      // Don't extract locations from SVG elements - use only path locations
      // await extractFromSVG(svgText)
      
      // Wait for DOM update then calculate positions
      await nextTick()
      
      if (isNavigating.value && currentPath.value) {
        calculatePathPositions()
      }
    }
  } catch (error) {
    console.error('[NavigateView] Error loading map:', error)
    mapError.value = error.message || 'Failed to load map'
    // Use inline fallback SVG
    svgContent.value = getFallbackSvgContent()
    mapLoaded.value = true
  }
}

// Calculate positions of path elements
const calculatePathPositions = () => {
  if (!currentPath.value || !currentPath.value.elementIds) {
    pathPositions.value = []
    return
  }
  
  const positions = []
  const svgWidth = viewBox.value.width
  const svgHeight = viewBox.value.height
  
  console.log('[NavigateView] Calculating positions for:', currentPath.value.elementIds)
  console.log('[NavigateView] SVG dimensions:', svgWidth, 'x', svgHeight)
  console.log('[NavigateView] Available locations:', locations.value?.length || 0)
  
  // Use saved coordinates from visualPoints or points if available
  const savedPoints = currentPath.value.visualPoints || currentPath.value.points || []
  
  for (let i = 0; i < currentPath.value.elementIds.length; i++) {
    const elementId = currentPath.value.elementIds[i]
    
    // Skip invalid elementIds
    if (!elementId || typeof elementId !== 'string') {
      console.warn('[NavigateView] Skipping invalid elementId:', elementId)
      positions.push({ x: 0, y: 0, id: elementId || 'unknown', notFound: true })
      continue
    }
    
    // FIRST: Try to use saved coordinates from visualPoints/points
    let savedCoord = null
    if (i < savedPoints.length) {
      const pt = savedPoints[i]
      if (pt && typeof pt === 'object') {
        // visualPoints format: {x, y, id, row, col, gridSize}
        if (pt.x !== undefined && pt.y !== undefined) {
          savedCoord = { x: pt.x, y: pt.y }
        }
        // points format: [x, y]
        else if (Array.isArray(pt) && pt.length >= 2) {
          savedCoord = { x: pt[0], y: pt[1] }
        }
      }
    }
    
    if (savedCoord && savedCoord.x !== undefined && savedCoord.y !== undefined) {
      console.log('[NavigateView] Using saved coord for', elementId, ':', savedCoord.x, savedCoord.y)
      positions.push({
        x: savedCoord.x,
        y: savedCoord.y,
        id: elementId
      })
      continue
    }
    
    // SECOND: Try to find position from locations (facilities)
    if (locations.value && Array.isArray(locations.value)) {
      const location = locations.value.find(l => l.id === elementId)
      if (location && (location.x !== undefined && location.x !== null)) {
        console.log('[NavigateView] Using location coord for', elementId, ':', location.x, location.y)
        positions.push({
          x: location.x,
          y: location.y,
          id: elementId
        })
        continue
      }
    }
    
    // THIRD: Fallback to finding SVG element
    if (svgMap.value) {
      const element = svgMap.value.querySelector(`#${elementId}`)
      if (element) {
        const bbox = element.getBBox()
        positions.push({
          x: bbox.x + bbox.width / 2,
          y: bbox.y + bbox.height / 2,
          id: elementId
        })
        continue
      }
    }
    
    // LAST RESORT: Not found
    positions.push({ x: 0, y: 0, id: elementId, notFound: true })
  }
  
  console.log('[NavigateView] Final path positions count:', positions.length)
  positions.forEach((p, i) => {
    const x = p.x != null ? p.x.toFixed(1) : 'null'
    const y = p.y != null ? p.y.toFixed(1) : 'null'
    console.log(`  [${i}] ${p.id}: x=${x}, y=${y}`)
  })
  pathPositions.value = positions
}

// Start navigation with from/to locations
const startNavigation = async () => {
  if (!fromLocation.value || !toLocation.value) {
    alert('Please select both starting point and destination.')
    return
  }
  
  console.log('[NavigateView] Starting navigation from', fromLocation.value, 'to', toLocation.value)
  
  try {
    const pathId = await findOrCreatePath(fromLocation.value, toLocation.value)
    
    if (!pathId) {
      alert('No path found. Please create a path in Admin Panel → SVG Paths.')
      return
    }
    
    const path = pathManager.getPath(pathId)
    if (!path || !path.visualPoints || path.visualPoints.length === 0) {
      alert('Path has no coordinates! Please edit the path in Admin Panel and add X/Y coordinates.')
      return
    }
    
    pathManager.startNavigation(pathId)
    console.log('[NavigateView] Navigation started!', pathId)
    
    await nextTick()
    calculatePathPositions()
    
  } catch (error) {
    console.error('[NavigateView] Error starting navigation:', error)
    alert('Failed to start navigation: ' + error.message)
  }
}

// Find a path that contains all stops in order
const findMultiStopPath = async (from, toLocations) => {
  console.log('[NavigateView] Looking for multi-stop path from', from, 'through', toLocations)
  
  // Build the full route: from + all to locations
  const fullRoute = [from, ...toLocations]
  console.log('[NavigateView] Full route needed:', fullRoute)
  
  // Find a path where elementIds contains all route locations in order
  const matchingPath = availablePaths.value.find(p => {
    if (!p.elementIds || p.elementIds.length < fullRoute.length) return false
    
    // Check if all locations appear in order in elementIds
    let routeIndex = 0
    for (const elementId of p.elementIds) {
      if (elementId === fullRoute[routeIndex]) {
        routeIndex++
        if (routeIndex === fullRoute.length) break
      }
    }
    
    const match = routeIndex === fullRoute.length
    if (match) {
      console.log('[NavigateView] Found matching multi-stop path:', p.id, 'elementIds:', p.elementIds)
    }
    return match
  })
  
  if (matchingPath) {
    return matchingPath.id
  }
  
  // Fallback: try to find a path that at least contains from and first to
  console.log('[NavigateView] No exact multi-stop match, falling back to first segment')
  return await findOrCreatePath(from, toLocations[0])
}

// Find or create a path between two locations
const findOrCreatePath = async (from, to) => {
  console.log('[NavigateView] Looking for path from', from, 'to', to)
  console.log('[NavigateView] Available paths count:', availablePaths.value.length)
  
  // Debug: Log each path with visualPoints
  availablePaths.value.forEach((p, i) => {
    console.log(`[NavigateView] Path ${i}:`, p.id, 'from:', p.from, 'to:', p.to, 'elementIds:', p.elementIds, 'visualPoints:', p.visualPoints?.length || 0)
  })
  
  // First, try to find an existing path
  // Match by: (from/to fields) OR (elementIds first/last) OR (any path containing both points)
  const existingPath = availablePaths.value.find(p => {
    // Check 1: Match by from/to fields
    const matchFromTo = p.from === from && p.to === to
    
    // Check 2: Match by elementIds first and last
    const matchElementIds = p.elementIds && 
      p.elementIds.length >= 2 &&
      p.elementIds[0] === from && 
      p.elementIds[p.elementIds.length - 1] === to
    
    // Check 3: Match if path contains both from and to anywhere in elementIds
    const matchContainsBoth = p.elementIds && 
      p.elementIds.includes(from) && 
      p.elementIds.includes(to)
    
    const match = matchFromTo || matchElementIds || matchContainsBoth
    
    if (match) {
      console.log('[NavigateView] Found matching path:', p.id, 
        'from:', p.from, 'to:', p.to, 
        'elementIds:', p.elementIds,
        'visualPoints:', p.visualPoints?.length || 0)
    }
    return match
  })
  
  if (existingPath) {
    // Verify path has coordinates
    if (!existingPath.visualPoints || existingPath.visualPoints.length === 0) {
      console.warn('[NavigateView] Found path but it has no coordinates:', existingPath.id)
      alert('Selected path has no coordinates! Please go to Admin Panel → Map Management → SVG Paths and add X/Y coordinates for each point.')
      return null
    }
    console.log('[NavigateView] Using existing path with', existingPath.visualPoints.length, 'visual points:', existingPath.id)
    return existingPath.id
  }
  console.log('[NavigateView] No existing path found, creating temp')
  
  // If no existing path, create a temporary one
  const tempPathId = `temp_${from}_${to}_${Date.now()}`
  const tempPath = {
    id: tempPathId,
    name: `${getLocationName(from)} → ${getLocationName(to)}`,
    from: from,
    to: to,
    elementIds: [from, to],
    points: [],
    visualPoints: []
  }
  
  // Add to path manager using proper reactivity
  pathManager.paths.value = {
    ...pathManager.paths.value,
    [tempPathId]: tempPath
  }
  
  return tempPathId
}

// Helper function to get path info for a specific destination
const getPathForDestination = (toLocation) => {
  if (!fromLocation.value || !toLocation) return null
  
  // Find path from FROM to this TO
  return availablePaths.value.find(p => {
    // Match by elementIds array
    if (p.elementIds && p.elementIds.length === 2) {
      return p.elementIds[0] === fromLocation.value && p.elementIds[1] === toLocation
    }
    // Match by from/to fields
    return (p.from === fromLocation.value && p.to === toLocation) ||
           (p.from === fromLocation.value && p.elementIds?.includes(toLocation))
  })
}

// Stop navigation
const stopNavigation = () => {
  pathManager.stopNavigation()
  pathPositions.value = []
  fromLocation.value = ''
  toLocation.value = ''
  resetView()
}

// Navigate to next step
const nextStep = () => {
  pathManager.nextStep()
  updateViewToCurrentStep()
}

// Navigate to previous step
const previousStep = () => {
  pathManager.previousStep()
  updateViewToCurrentStep()
}

// Update viewBox to current step position with smooth animation
const updateViewToCurrentStep = () => {
  if (!currentPosition.value || currentPosition.value.notFound) return
  
  // Smooth transition to new position - use current zoom level
  const targetX = currentPosition.value.x
  const targetY = currentPosition.value.y
  
  centerOnPoint(targetX, targetY, zoomLevel.value, true)
}


// Drag/Grab handlers
const startDrag = (e) => {
  // Only drag with left mouse button or touch
  if (e.type === 'mousedown' && e.button !== 0) return
  
  isDragging.value = true
  const clientX = e.clientX || (e.touches?.[0]?.clientX)
  const clientY = e.clientY || (e.touches?.[0]?.clientY)
  
  dragStart.value = { x: clientX, y: clientY }
  viewBoxStart.value = { 
    x: viewBox.value.x, 
    y: viewBox.value.y 
  }
}

const drag = (e) => {
  if (!isDragging.value) return
  e.preventDefault()
  
  const clientX = e.clientX || (e.touches?.[0]?.clientX)
  const clientY = e.clientY || (e.touches?.[0]?.clientY)
  
  // Calculate the drag delta in screen pixels
  const deltaX = clientX - dragStart.value.x
  const deltaY = clientY - dragStart.value.y
  
  // Convert screen pixels to SVG viewBox units
  const container = mapContainer.value
  if (!container) return
  
  const rect = container.getBoundingClientRect()
  const svgUnitsPerPixelX = viewBox.value.width / rect.width
  const svgUnitsPerPixelY = viewBox.value.height / rect.height
  
  // Update viewBox (inverse direction for natural panning)
  viewBox.value = {
    ...viewBox.value,
    x: viewBoxStart.value.x - deltaX * svgUnitsPerPixelX,
    y: viewBoxStart.value.y - deltaY * svgUnitsPerPixelY
  }
}

const endDrag = () => {
  isDragging.value = false
}

// Handle mouse wheel zoom - zooms toward mouse cursor position
const handleWheelZoom = (event) => {
  event.preventDefault()
  
  if (!svgMap.value) return
  
  // Get mouse position in SVG coordinates
  const pt = svgMap.value.createSVGPoint()
  pt.x = event.clientX
  pt.y = event.clientY
  const svgP = pt.matrixTransform(svgMap.value.getScreenCTM().inverse())
  
  // Calculate zoom factor
  const zoomFactor = event.deltaY > 0 ? 0.9 : 1.1
  const oldZoom = zoomLevel.value
  const newZoom = Math.max(0.3, Math.min(5, oldZoom * zoomFactor))
  
  // Calculate new viewBox to zoom toward mouse position
  const zoomRatio = oldZoom / newZoom
  const newWidth = viewBox.value.width * zoomRatio
  const newHeight = viewBox.value.height * zoomRatio
  
  // Calculate offset to keep mouse point stable
  const mouseOffsetX = svgP.x - viewBox.value.x
  const mouseOffsetY = svgP.y - viewBox.value.y
  
  const newX = svgP.x - (mouseOffsetX * zoomRatio)
  const newY = svgP.y - (mouseOffsetY * zoomRatio)
  
  // Update viewBox and zoom level
  viewBox.value = {
    x: newX,
    y: newY,
    width: newWidth,
    height: newHeight
  }
  zoomLevel.value = newZoom
}

// Zoom controls
const zoomIn = () => {
  const centerX = viewBox.value.x + viewBox.value.width / 2
  const centerY = viewBox.value.y + viewBox.value.height / 2
  zoomLevel.value = Math.min(zoomLevel.value * 1.3, 5)
  centerOnPoint(centerX, centerY, zoomLevel.value)
}

const zoomOut = () => {
  const centerX = viewBox.value.x + viewBox.value.width / 2
  const centerY = viewBox.value.y + viewBox.value.height / 2
  zoomLevel.value = Math.max(zoomLevel.value / 1.3, 0.3)
  centerOnPoint(centerX, centerY, zoomLevel.value)
}

const resetView = () => {
  viewBox.value = { x: 0, y: 0, width: ORIGINAL_VIEWBOX.width, height: ORIGINAL_VIEWBOX.height }
  zoomLevel.value = 1
  rotation.value = 0
}

// Rotation controls
const rotateClockwise = () => {
  rotation.value = (rotation.value + 90) % 360
}

const rotateCounterClockwise = () => {
  rotation.value = (rotation.value - 90) % 360
}

// Fallback SVG content
// Center viewBox on a specific point with optional zoom
const centerOnPoint = (targetX, targetY, zoom = 1, animate = false) => {
  const width = ORIGINAL_VIEWBOX.width / zoom
  const height = ORIGINAL_VIEWBOX.height / zoom
  
  const newX = targetX - width / 2
  const newY = targetY - height / 2
  
  if (animate) {
    // Animate the transition
    const startX = viewBox.value.x
    const startY = viewBox.value.y
    const startWidth = viewBox.value.width
    const startHeight = viewBox.value.height
    
    const duration = 500
    const startTime = performance.now()
    
    const animateFrame = (currentTime) => {
      const elapsed = currentTime - startTime
      const progress = Math.min(elapsed / duration, 1)
      
      // Ease out cubic
      const ease = 1 - Math.pow(1 - progress, 3)
      
      viewBox.value = {
        x: startX + (newX - startX) * ease,
        y: startY + (newY - startY) * ease,
        width: startWidth + (width - startWidth) * ease,
        height: startHeight + (height - startHeight) * ease
      }
      
      if (progress < 1) {
        requestAnimationFrame(animateFrame)
      }
    }
    
    requestAnimationFrame(animateFrame)
  } else {
    viewBox.value = {
      x: newX,
      y: newY,
      width: width,
      height: height
    }
  }
}

const getFallbackSvgContent = () => {
  return `
    <rect width="3306" height="7159" fill="#f0f0f0"/>
    <text x="1653" y="3580" text-anchor="middle" font-size="100" fill="#999">
      Map Loading Failed
    </text>
  `
}

// Watch for path changes
watch(currentPath, (newPath) => {
  if (newPath && mapLoaded.value) {
    nextTick(() => calculatePathPositions())
  }
})

// Watch for path changes and extract locations
watch(availablePaths, () => {
  console.log('[NavigateView] Paths changed, extracting locations...')
  extractLocationsFromPaths()
}, { immediate: true })

// Watch for FROM location changes - reset TO location
watch(fromLocation, (newFrom, oldFrom) => {
  if (newFrom !== oldFrom) {
    console.log('[NavigateView] From location changed, resetting To location')
    toLocation.value = '' // Reset To location when From changes
  }
})

// Watch for TO location changes and recalculate path
watch(toLocation, () => {
  if (isNavigating.value && currentPath.value) {
    console.log('[NavigateView] TO location changed, recalculating...')
    calculatePathPositions()
  }
})

// Lifecycle
onMounted(async () => {
  loadMap()
  loadNotificationCount()
  // Wait for paths to load from storage/API, then extract locations
  await new Promise(resolve => setTimeout(resolve, 500))
  extractLocationsFromPaths()
  console.log('[NavigateView] Locations extracted:', locations.value.length)
  console.log('[NavigateView] From locations:', fromLocations.value.length)
  console.log('[NavigateView] To locations:', toLocations.value.length)
})

onUnmounted(() => {
  pathManager.stopNavigation()
})
</script>

<style scoped>
.svg-navigate-view {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: var(--color-surface, #f5f5f5);
}

/* Top location bar for mobile */
.svg-nav-locations-top {
  display: flex;
  gap: 12px;
  align-items: center;
  padding: 12px 16px;
  background: var(--color-bg, white);
  border-bottom: 1px solid var(--color-border, #eee);
}

.svg-nav-field-compact {
  flex: 1;
  margin-bottom: 0;
  min-width: 0;
}

/* Header - Orange gradient matching Settings */
.svg-nav-header {
  background: linear-gradient(135deg, #FF5722 0%, #FF9800 100%);
  padding: 16px 20px;
  color: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.svg-nav-header-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.svg-nav-header-icon {
  width: 48px;
  height: 48px;
  background: white !important;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.svg-nav-header-icon .material-icons {
  font-size: 24px;
  color: #FF5722;
}

.svg-nav-header-text h1 {
  margin: 0;
  font-size: 22px;
  font-weight: 600;
}

.svg-nav-header-text p {
  margin: 4px 0 0;
  font-size: 14px;
  opacity: 0.9;
}

/* Panel */
.svg-nav-controls {
  padding: 16px;
  background: var(--color-surface, #f5f5f5);
  border-top: 1px solid var(--color-border, #e0e0e0);
}

.svg-nav-field {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
  position: relative;
}

/* Modern Select Styling */
.svg-nav-input {
  padding: 12px 16px;
  border: 1px solid var(--color-border, #ddd);
  border-radius: 8px;
  font-size: 16px;
  background: var(--color-bg, white);
  color: var(--color-text-primary, #333);
  cursor: pointer;
  transition: all 0.2s ease;
}

.svg-nav-input:focus {
  outline: none;
  border-color: #FF5722;
  box-shadow: 0 0 0 3px rgba(255,87,34,0.15);
}

.svg-nav-select {
  flex: 1;
  padding: 12px 40px 12px 16px;
  border: 2px solid var(--color-border, #e0e0e0);
  border-radius: 12px;
  background: var(--color-bg, white);
  color: var(--color-text-primary, #333);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  appearance: none;
  -webkit-appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24'%3E%3Cpath fill='%23666' d='M7 10l5 5 5-5z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  background-size: 20px;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.svg-nav-select:hover {
  border-color: #FF9800;
  box-shadow: 0 4px 8px rgba(255,152,0,0.15);
}

.svg-nav-select:focus {
  outline: none;
  border-color: #FF5722;
  box-shadow: 0 0 0 3px rgba(255,87,34,0.15);
}

/* Multi-destination styles */
.svg-nav-multi-to {
  align-items: flex-start;
}

.svg-nav-to-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex: 1;
}

.svg-nav-to-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.svg-nav-remove-btn {
  background: #ff4444;
  color: white;
  border: none;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  padding: 0;
}

.svg-nav-remove-btn:hover {
  background: #cc0000;
}

.svg-nav-remove-btn .material-icons {
  font-size: 14px;
}

.svg-nav-add-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 6px 12px;
  font-size: 12px;
  cursor: pointer;
  margin-top: 4px;
  width: fit-content;
}

.svg-nav-add-btn:hover {
  background: #45a049;
}

.svg-nav-add-btn:disabled {
  background: #cccccc;
  cursor: not-allowed;
}

.svg-nav-icon {
  color: #666;
  font-size: 24px;
}

.svg-nav-icon.from { color: #4CAF50; }
.svg-nav-icon.to { color: #FF5722; }

/* Empty state */
.svg-nav-empty {
  text-align: center;
  padding: 40px 20px;
  color: #666;
}

.svg-nav-empty .material-icons {
  margin-bottom: 16px;
}

.svg-nav-empty p {
  margin: 0 0 8px 0;
  font-size: 16px;
}

.svg-nav-hint {
  font-size: 14px;
  color: #999;
  font-style: italic;
}

.svg-nav-actions {
  display: flex;
  gap: 12px;
}

.svg-nav-start-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 14px 24px;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}

.svg-nav-start-btn:hover:not(:disabled) {
  background: #45a049;
}

.svg-nav-start-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.svg-nav-full-route {
  margin-bottom: 12px;
  padding: 8px 12px;
  background: var(--color-bg, white);
  border-radius: 6px;
  font-size: 13px;
}

.route-line {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 4px;
}

.route-from {
  color: #4caf50;
  font-weight: 600;
}

.route-arrow {
  color: #999;
}

.route-stop {
  color: #ff9800;
}

.route-to {
  color: #2196f3;
  font-weight: 600;
}

.svg-nav-stops {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.svg-nav-stop {
  font-size: 13px;
  color: var(--color-text-secondary, #555);
  padding: 4px 8px;
  background: var(--color-bg, white);
  border-radius: 4px;
}

.svg-nav-stop.from-stop {
  background: #E8F5E9;
  color: #2E7D32;
  border-left: 3px solid #4CAF50;
}

.svg-nav-stop.to-stop {
  background: #FFEBEE;
  color: #C62828;
  border-left: 3px solid #FF5722;
}

/* Path Cards for Multi-Destination */
.svg-nav-path-cards {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 12px;
}

.svg-nav-path-card {
  background: var(--color-bg, white);
  border-radius: 8px;
  padding: 12px;
  border: 1px solid var(--color-border, #e0e0e0);
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.path-card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  padding-bottom: 8px;
  border-bottom: 1px solid #eee;
}

.path-card-number {
  background: #2196F3;
  color: white;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: bold;
}

.path-card-destination {
  font-weight: 600;
  color: #333;
  font-size: 14px;
}

.path-card-details {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.path-detail-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: #666;
}

.path-detail-item .material-icons {
  font-size: 14px;
  color: #2196F3;
}

.path-card-no-path {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #ff9800;
  font-size: 12px;
  padding: 8px;
  background: #fff3e0;
  border-radius: 4px;
}

.path-card-no-path .material-icons {
  font-size: 16px;
}

/* Navigation Controls */
.svg-nav-controls {
  display: flex;
  flex-direction: column;
  padding: 16px;
  background: rgba(255, 255, 255, 0.95);
  border-top: 1px solid #e0e0e0;
}

.svg-nav-progress {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.svg-nav-step-info {
  font-size: 14px;
  color: #666;
}

.svg-nav-current-location {
  font-size: 16px;
  font-weight: 500;
  color: #FF9800;
}

.svg-nav-buttons {
  display: flex;
  gap: 12px;
}

.svg-nav-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 12px 16px;
  background: #FF9800;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.svg-nav-btn:hover:not(:disabled) {
  background: #F57C00;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255,152,0,0.4);
}

.svg-nav-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.svg-nav-stop-btn {
  background: #f44336;
}

.svg-nav-stop-btn:hover {
  background: #d32f2f;
}

/* Multi-stop navigation styles */
.svg-nav-multi-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
}

.svg-nav-multi-info strong {
  color: #2196F3;
  font-size: 14px;
}

.svg-nav-multi-info small {
  color: #666;
  font-size: 11px;
}

.svg-nav-next-dest {
  background: #2196F3;
}

.svg-nav-next-dest:hover:not(:disabled) {
  background: #1976D2;
}

/* Map Container - Dark mode aware background */
.svg-map-container {
  flex: 1;
  position: relative;
  overflow: hidden;
  background: var(--color-surface-2, #e0e0e0);
  cursor: grab;
  touch-action: none;
  user-select: none;
}

.svg-map-container:active,
.svg-map-container.is-dragging {
  cursor: grabbing;
}

.svg-map {
  width: 100%;
  height: 100%;
  display: block;
  transition: all 0.5s ease-out;
}

.svg-map-loading {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: var(--color-surface);
  color: var(--color-text-secondary);
  z-index: 10;
}

.svg-map-error {
  color: #F44336;
  font-size: 14px;
  margin-top: 8px;
  padding: 8px 16px;
  background: #FFEBEE;
  border-radius: 4px;
}

.svg-map-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #FF9800;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Map Skeleton + CometSpinner styles */
.svg-map-skeleton-wrap { position: absolute; inset: 0; z-index: 10; }
.map-sk-full { width: 100%; height: 100%; }
.map-sk-center {
  position: absolute; top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  display: flex; flex-direction: column; align-items: center; gap: 12px;
  pointer-events: none;
}
.map-sk-hint {
  font-size: 13px; font-weight: 500; color: #FF9800;
  background: linear-gradient(90deg, rgba(255,152,0,0.4), #FF9800 50%, rgba(255,152,0,0.4));
  background-size: 200% auto;
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
  animation: mapHintShimmer 2s linear infinite;
}
@keyframes mapHintShimmer {
  0% { background-position: 200% center; } 100% { background-position: -200% center; }
}
.svg-map-error-state {
  position: absolute; inset: 0; z-index: 10;
  display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 10px;
  background: var(--color-surface, #fff); color: #F44336;
}

/* Navigation Path Overlay */
.nav-path-overlay {
  pointer-events: none;
}

/* Responsive - Liquid Design */
@media (max-width: 768px) {
  .svg-navigate-view {
    height: 100vh;
    height: 100dvh;
  }
  
  .svg-nav-panel,
  .svg-nav-controls {
    padding: 12px;
  }
  
  .svg-nav-header {
    padding: 12px 16px;
  }
  
  .svg-nav-header-icon {
    width: 40px;
    height: 40px;
  }
  
  .svg-nav-header-icon .material-icons {
    font-size: 20px;
  }
  
  .svg-nav-header-text h1 {
    font-size: 18px;
  }
  
  .svg-nav-header-text p {
    font-size: 12px;
  }
  
  .svg-nav-field {
    gap: 8px;
    margin-bottom: 12px;
  }
  
  .svg-nav-input,
  .svg-nav-select {
    font-size: 16px; /* Prevents zoom on iOS */
    padding: 10px 12px;
  }
  
  .svg-nav-buttons {
    flex-wrap: wrap;
    gap: 8px;
  }
  
  .svg-nav-btn {
    font-size: 13px;
    padding: 10px 12px;
    flex: 1;
    min-width: 100px;
  }
  
  /* Map container mobile */
  .svg-nav-map-container {
    min-height: 250px;
  }
  
  /* Navigation path info mobile */
  .svg-nav-path-info {
    max-width: calc(100vw - 24px);
    font-size: 14px;
  }
  
  .svg-nav-path-info-header {
    padding: 10px 12px;
  }
  
  /* Step counter mobile */
  .svg-nav-step-counter {
    font-size: 13px;
    padding: 8px 12px;
  }

  .nav-fab-container {
    bottom: 12px;
    right: 12px;
  }
}

/* Small mobile devices */
@media (max-width: 480px) {
  .svg-nav-header {
    padding: 10px 12px;
  }
  
  .svg-nav-header-icon {
    width: 36px;
    height: 36px;
  }
  
  .svg-nav-header-icon .material-icons {
    font-size: 18px;
  }
  
  .svg-nav-header-text h1 {
    font-size: 16px;
  }
  
  .svg-nav-header-text p {
    font-size: 11px;
  }
  
  .svg-nav-panel {
    padding: 10px;
  }
  
  .svg-nav-field {
    flex-direction: column;
    align-items: stretch;
  }
  
  .svg-nav-field > * {
    width: 100%;
  }
  
  .svg-nav-btn {
    font-size: 12px;
    padding: 8px 10px;
  }
  
  .svg-nav-multi-to {
    flex-direction: column;
  }
}

/* Destination Preview Panel - TO: LOCATION - Floating Draggable */
.svg-nav-destination-preview {
  background: #FFA726;
  border-radius: 12px;
  padding: 16px;
  margin: 12px 0;
  color: #333;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.svg-nav-destination-preview.floating {
  position: absolute;
  top: 80px;
  left: 16px;
  width: 280px;
  margin: 0;
  z-index: 100;
  cursor: move;
  user-select: none;
  opacity: 0.6;
  transition: opacity 0.2s ease;
}

.svg-nav-destination-preview.floating:hover {
  opacity: 1;
}

.svg-nav-destination-preview.floating.minimized {
  width: auto;
  min-width: 180px;
}

.dest-preview-toggle {
  background: rgba(255, 255, 255, 0.3);
  border: none;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding-bottom: 8px;
  border-bottom: 1px solid rgba(255,255,255,0.3);
}

.dest-info-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  cursor: pointer;
  padding: 6px 6px;
  border-bottom: 1px solid rgba(255,255,255,0.3);
}

.dest-info-header-main {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
}

.dest-info-from {
  display: flex;
  align-items: center;
  gap: 4px;
}

.dest-info-to {
  display: flex;
  align-items: center;
  gap: 4px;
}

.dest-info-label-small {
  font-size: 12px;
  color: #333;
  font-weight: 500;
}

.dest-info-value-small {
  font-size: 13px;
  color: #333;
}

.dest-info-arrow {
  color: #333;
  font-size: 14px;
}

.dest-info-panel.minimized .dest-info-header {
  padding-bottom: 0;
  border-bottom: none;
}

.dest-info-header .material-icons {
  color: #333;
  font-size: 20px;
}

.dest-info-label {
  font-weight: 600;
  color: #333;
  font-size: 14px;
}

.dest-info-name {
  font-weight: 500;
  color: #333;
  font-size: 14px;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.dest-info-toggle {
  background: transparent;
  border: none;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #333;
  padding: 0;
}

.dest-info-toggle:hover {
  color: #000;
}

.dest-info-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 8px;
  margin-bottom: 16px;
}

.dest-info-field {
  display: flex;
  flex-direction: column;
  gap: 2px;
  background: rgba(255,255,255,0.9);
  padding: 8px 12px;
  border-radius: 8px;
}

.dest-info-field-label {
  font-size: 12px;
  color: #666;
  font-weight: 500;
}

.dest-info-field-value {
  font-size: 14px;
  color: #333;
}

.dest-info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}

.dest-info-grid .dest-info-field {
  margin-bottom: 0;
}

@media (max-width: 480px) {
  .dest-info-panel {
    bottom: 130px;
    left: 12px;
    right: 12px;
    padding: 10px;
  }
}

/* Navigation FAB Buttons - Horizontal layout */
.nav-fab-container {
  position: fixed;
  bottom: 80px;
  right: 16px;
  display: flex;
  flex-direction: row;
  gap: 12px;
  z-index: 101;
}

/* All FAB buttons - Dark navy blue background */
.nav-fab-btn,
.nav-notifications-btn,
.nav-rate-btn,
.nav-chatbot-btn,
.nav-rotate-cw-btn,
.nav-rotate-ccw-btn {
  background: #0f172a !important;
  color: white !important;
  backdrop-filter: none !important;
}

.nav-fab-btn:hover,
.nav-notifications-btn:hover,
.nav-rate-btn:hover,
.nav-chatbot-btn:hover,
.nav-rotate-cw-btn:hover,
.nav-rotate-ccw-btn:hover {
  background: #1e3a5f !important;
}

/* Hide Feedback button on mobile */
/* Mobile - smaller 35px buttons */
@media (max-width: 768px) {
  .nav-fab-container {
    bottom: 80px;
    right: 12px;
    left: auto;
    gap: 8px;
  }

  .nav-fab-btn {
    width: 35px;
    height: 35px;
    min-width: 35px;
    min-height: 35px;
  }

  .nav-fab-btn .material-icons {
    font-size: 18px;
  }
}

/* Mobile - chatbot stays at bottom right */
@media (max-width: 480px) {
  .nav-fab-container {
    bottom: 80px;
    right: 12px;
    left: auto;
    gap: 8px;
  }

  .nav-fab-btn {
    width: 35px;
    height: 35px;
    min-width: 35px;
    min-height: 35px;
  }

  .nav-fab-btn .material-icons {
    font-size: 18px;
  }
}

.svg-nav-field-compact {
  flex: 1;
  margin-bottom: 0;
  min-width: 0;
}

.svg-nav-field-compact .svg-nav-select {
  font-size: 13px;
  padding: 8px 12px;
}

.svg-nav-field-compact .svg-nav-select:disabled {
  background: var(--color-bg-secondary, #f5f5f5);
  color: var(--color-text-muted, #999);
  cursor: not-allowed;
  opacity: 0.7;
}

.svg-nav-start-btn-compact {
  width: 44px;
  height: 44px;
  min-width: 44px;
  min-height: 44px;
  max-width: 44px;
  max-height: 44px;
  padding: 0;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  flex-grow: 0;
}

.svg-nav-start-btn-compact .material-icons {
  margin: 0;
  font-size: 24px;
}

@media (max-width: 480px) {
  .svg-nav-locations-top {
    padding: 6px 10px;
    gap: 6px;
  }
  
  .svg-nav-field-compact .svg-nav-select {
    font-size: 12px;
    padding: 6px 10px;
  }
  
  .svg-nav-start-btn-compact {
    width: 40px;
    height: 40px;
  }
  
  .svg-nav-start-btn-compact .material-icons {
    font-size: 22px;
  }
}

.nav-fab-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease;
  position: relative;
}

.nav-fab-btn .material-icons {
  font-size: 20px;
}

/* Make star icon larger to match visual size of other icons */
.nav-rate-btn .material-icons {
  font-size: 22px;
}

/* Multi-stop navigation styles */
.svg-nav-field.stop-field {
  display: flex;
  align-items: center;
  gap: 8px;
}

.svg-nav-field.stop-field .svg-nav-select {
  flex: 1;
}

.svg-nav-remove-stop {
  background: var(--color-surface-2, #f5f5f5);
  border: none;
  padding: 6px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-danger, #f44336);
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.svg-nav-remove-stop:hover {
  background: var(--color-danger-light, #ffebee);
}

.svg-nav-add-stop {
  display: flex;
  justify-content: center;
  margin: 8px 0;
}

.svg-nav-add-btn {
  background: var(--color-surface-2, #f5f5f5);
  border: 2px dashed var(--color-border, #ddd);
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: var(--color-text-secondary, #666);
  transition: all 0.2s ease;
}

.svg-nav-add-btn:hover {
  background: var(--color-primary-light, #e3f2fd);
  border-color: var(--color-primary, #1976d2);
  color: var(--color-primary, #1976d2);
}

.svg-nav-full-route.multi-stop-route {
  background: linear-gradient(135deg, #e8f5e9 0%, #fff3e0 100%);
}

.svg-nav-full-route .route-stop {
  background: #ff9800;
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-weight: 500;
}

.nav-fab-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
}

.nav-fab-btn .material-icons {
  font-size: 20px;
}

.nav-fab-badge {
  position: absolute;
  top: -4px;
  right: -4px;
  background: #F44336;
  color: white;
  font-size: 11px;
  font-weight: bold;
  min-width: 18px;
  height: 18px;
  border-radius: 9px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

/* Chatbot stays fixed on right side at all screen sizes */
@media (max-width: 768px) {
  .nav-fab-container {
    bottom: 80px;
    right: 12px;
    left: auto;
  }

  .nav-fab-btn {
    width: 50px;
    height: 50px;
  }

  .nav-fab-btn .material-icons {
    font-size: 24px;
  }
}
</style>
