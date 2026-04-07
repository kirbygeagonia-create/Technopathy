<template>
  <div class="fr-panel-container">
    <div class="fr-header">
      <h3>Facilities & Rooms</h3>
      <button class="close-btn-icon" @click="$emit('close')">
        <span class="material-icons">close</span>
      </button>
    </div>
    
    <div class="fr-layout">
      <!-- Facilities Column -->
      <div class="fr-col facilities-col">
        <div class="col-header">
          <h4>Facilities</h4>
          <span v-if="selectedFacility" class="clear-selection" @click.stop="clearFacilityFilter">Clear</span>
        </div>
        <div class="col-content">
          <div v-if="facilities.length === 0" class="empty-state">No data synced.</div>
          <div
            v-for="fac in facilities"
            :key="fac.id"
            class="list-item"
            :class="{ active: selectedFacility && selectedFacility.id === fac.id }"
            @click="selectFacility(fac)"
          >
            <div class="item-icon facility-item-icon">
              <span class="material-icons">business</span>
            </div>
            <div class="item-details">
              <span class="item-name">{{ fac.name }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Rooms Column -->
      <div class="fr-col rooms-col">
        <div class="col-header">
          <h4>Rooms {{ selectedFacility ? `(${selectedFacility.name})` : '(All)' }}</h4>
        </div>
        <div class="col-content">
          <div v-if="filteredRooms.length === 0" class="empty-state">
            No rooms found.
          </div>
          <div
            v-for="room in filteredRooms"
            :key="room.id"
            class="list-item"
            :class="{ active: selectedRoom && selectedRoom.id === room.id }"
            @click="selectRoom(room)"
          >
            <div class="item-icon room-item-icon">
              <span class="material-icons">meeting_room</span>
            </div>
            <div class="item-details">
              <span class="item-name">{{ room.name }}</span>
              <span v-if="!selectedFacility" class="item-sub">{{ getFacilityName(room.facility_id) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Room detail expansion / display if needed -->
    <div v-if="selectedRoomDetails" class="room-details-overlay" @click="selectedRoomDetails = null">
      <div class="room-details-card" @click.stop>
        <div class="room-details-header">
          <h3>{{ selectedRoomDetails.name }}</h3>
          <button @click="selectedRoomDetails = null" class="close-btn-icon"><span class="material-icons">close</span></button>
        </div>
        <div class="room-details-body">
          <p><strong>Facility:</strong> {{ getFacilityName(selectedRoomDetails.facility_id) }}</p>
          <p><strong>Type:</strong> Room/Classroom</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import db from '../services/db.js'

const emit = defineEmits(['close'])

const facilities = ref([])
const rooms = ref([])

const selectedFacility = ref(null)
const selectedRoom = ref(null)
const selectedRoomDetails = ref(null)

const loadDataFromIndexedDB = async () => {
  try {
    const facs = await db.facilities.toArray()
    const rms = await db.rooms.toArray()
    facilities.value = facs
    rooms.value = rms
  } catch (error) {
    console.error('Failed to load facilities/rooms from IndexedDB:', error)
  }
}

onMounted(() => {
  loadDataFromIndexedDB()
})

const getFacilityName = (facilityId) => {
  const fac = facilities.value.find(f => f.id === facilityId || f.id === parseInt(facilityId))
  return fac ? fac.name : 'Unknown Building'
}

const filteredRooms = computed(() => {
  if (selectedFacility.value) {
    return rooms.value.filter(r => r.facility_id === selectedFacility.value.id || parseInt(r.facility_id) === selectedFacility.value.id)
  }
  return rooms.value
})

const selectFacility = (fac) => {
  if (selectedFacility.value && selectedFacility.value.id === fac.id) {
    selectedFacility.value = null // toggle off
  } else {
    selectedFacility.value = fac
  }
}

const selectRoom = (room) => {
  selectedRoom.value = room
  selectedRoomDetails.value = room
  
  // Requirement: Tapping a room should reflect its parent facility as the active selection
  if (room.facility_id) {
    const parentFac = facilities.value.find(f => f.id === room.facility_id || f.id === parseInt(room.facility_id))
    if (parentFac) {
      selectedFacility.value = parentFac
    }
  }
}

const clearFacilityFilter = () => {
  selectedFacility.value = null
}

</script>

<style scoped>
.fr-panel-container {
  display: flex;
  flex-direction: column;
  height: 80vh;
  max-height: 600px;
  background: var(--color-bg, #fff);
  border-radius: 16px;
  overflow: hidden;
  font-family: var(--font-primary, sans-serif);
}

.fr-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid var(--color-border, #eee);
  background: var(--color-surface, #f9f9f9);
}

.fr-header h3 {
  margin: 0;
  font-size: 18px;
  color: var(--color-text-primary, #333);
}

.close-btn-icon {
  background: none;
  border: none;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: var(--color-text-secondary, #666);
}

.close-btn-icon:hover {
  background: rgba(0,0,0,0.05);
}

.fr-layout {
  display: flex;
  flex-direction: row;
  flex: 1;
  overflow: hidden;
}

.fr-col {
  flex: 1;
  display: flex;
  flex-direction: column;
  border-right: 1px solid var(--color-border, #eee);
}

.fr-col:last-child {
  border-right: none;
}

.col-header {
  padding: 12px;
  background: var(--color-surface, #f5f5f5);
  border-bottom: 1px solid var(--color-border, #eee);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.col-header h4 {
  margin: 0;
  font-size: 14px;
  color: var(--color-text-secondary, #666);
}

.clear-selection {
  font-size: 12px;
  color: var(--color-primary, #FF9800);
  cursor: pointer;
}

.col-content {
  flex: 1;
  overflow-y: auto;
  padding: 8px 0;
}

.list-item {
  display: flex;
  align-items: center;
  padding: 8px 12px;
  cursor: pointer;
  min-height: 44px; /* Minimum tap target: 44x44px */
  border-bottom: 1px solid var(--color-border, #f5f5f5);
  transition: background 0.2s;
}

.list-item:hover {
  background: var(--color-surface, #f9f9f9);
}

.list-item.active {
  background: rgba(255, 152, 0, 0.1); /* Primary color light */
}

.item-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 12px;
  flex-shrink: 0;
}

.facility-item-icon {
  background: #FFF3E0;
  color: #FF9800;
}

.room-item-icon {
  background: #E3F2FD;
  color: #2196F3;
}

.item-icon .material-icons {
  font-size: 18px;
}

.item-details {
  display: flex;
  flex-direction: column;
}

.item-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-primary, #333);
}

.item-sub {
  font-size: 11px;
  color: var(--color-text-hint, #999);
}

.empty-state {
  padding: 24px;
  text-align: center;
  color: var(--color-text-hint, #999);
  font-size: 14px;
}

/* Overlay for Room Details */
.room-details-overlay {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
}

.room-details-card {
  background: var(--color-bg, #fff);
  border-radius: 12px;
  width: 250px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.2);
  display: flex;
  flex-direction: column;
}

.room-details-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid var(--color-border, #eee);
  background: #E3F2FD;
  border-radius: 12px 12px 0 0;
}

.room-details-header h3 {
  margin: 0;
  font-size: 16px;
  color: #2196F3;
}

.room-details-body {
  padding: 16px;
  font-size: 14px;
}

.room-details-body p {
  margin: 0 0 8px 0;
}

/* Responsiveness - ensure no clipping at 320px */
@media (max-width: 430px) {
  .item-icon {
    margin-right: 8px;
    width: 28px;
    height: 28px;
  }
  .item-icon .material-icons {
    font-size: 16px;
  }
  .item-name {
    font-size: 13px;
  }
  .col-header {
    padding: 8px;
  }
  .col-header h4 {
    font-size: 13px;
  }
  .list-item {
    padding: 8px;
  }
}
</style>
