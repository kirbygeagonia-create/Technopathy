<template>
  <div class="admin-panel admin-settings-view">
    <div class="admin-header">
      <div class="admin-header-title">
        <span class="material-icons">qr_code_2</span>
        <h2>QR Code Generator</h2>
      </div>
    </div>
    
    <div class="admin-card">
      <p class="mb-4 text-gray-600">Generate QR codes for campus access and navigation. Create a <strong>Campus Entry QR</strong> for the main gate, or deep-linked codes for specific facilities and rooms that visitors can scan to instantly navigate to their destination.</p>
      
      <div class="form-group">
        <label>Select Location Type</label>
        <select v-model="locationType" class="form-select">
          <option value="campus_entry">Campus Entry (Main Gate)</option>
          <option value="facility">Facility/Building</option>
          <option value="room">Room</option>
        </select>
        <p v-if="locationType === 'campus_entry'" class="form-hint">
          Generates a QR code for the main gate that directs visitors to the TechnoPath app
        </p>
      </div>
      
      <div class="form-group" v-if="locationType === 'facility'">
        <label>Select Facility</label>
        <select v-model="selectedFacilityId" class="form-select">
          <option value="" disabled>-- Choose Facility --</option>
          <option v-for="fac in facilities" :key="fac.id" :value="fac.id">
            {{ fac.name }}
          </option>
        </select>
      </div>
      
      <div class="form-group" v-if="locationType === 'room'">
        <label>Select Room</label>
        <select v-model="selectedRoomId" class="form-select">
          <option value="" disabled>-- Choose Room --</option>
          <option v-for="room in rooms" :key="room.id" :value="room.id">
            {{ room.name }} ({{ getFacilityName(room.facility_id) }})
          </option>
        </select>
      </div>

      <div class="form-actions mt-4">
        <button class="tp-btn-primary" @click="generateQR" :disabled="!canGenerate">
          <span class="material-icons">qr_code</span> Generate QR
        </button>
      </div>
    </div>

    <!-- QR Code Preview -->
    <div class="admin-card mt-6 qr-preview-card" v-if="qrValue">
      <h3 class="font-bold mb-4">Preview</h3>
      <div class="qr-preview-container" ref="qrWrapper">
        <qrcode-vue :value="qrValue" :size="250" level="H" ref="qrCodeComp" />
        <p class="qr-target-text mt-2 font-medium">{{ targetName }}</p>
      </div>
      <p class="qr-url-text mt-4 text-sm text-gray-500 break-all">{{ qrValue }}</p>
      
      <div class="form-actions justify-center mt-6">
        <button class="tp-btn-secondary" @click="downloadQR">
          <span class="material-icons">download</span> Download QR
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import QrcodeVue from 'qrcode.vue'
import api from '../../services/api.js'

const facilities = ref([])
const rooms = ref([])

const locationType = ref('facility')
const selectedFacilityId = ref('')
const selectedRoomId = ref('')

const qrValue = ref('')
const targetName = ref('')
const qrWrapper = ref(null)

const loadData = async () => {
  try {
    const [facRes, roomRes] = await Promise.all([
      api.get('/facilities/'),
      api.get('/rooms/')
    ])
    facilities.value = facRes.data
    rooms.value = roomRes.data
  } catch (err) {
    console.error('Failed to load locations', err)
  }
}

onMounted(() => {
  loadData()
})

const getFacilityName = (id) => {
  const f = facilities.value.find(f => f.id === id)
  return f ? f.name : ''
}

const canGenerate = computed(() => {
  if (locationType.value === 'campus_entry') return true
  if (locationType.value === 'facility') return !!selectedFacilityId.value
  if (locationType.value === 'room') return !!selectedRoomId.value
  return false
})

const generateQR = () => {
  // Build public URL with query parameter
  const origin = window.location.origin
  let id = ''
  let label = ''
  
  if (locationType.value === 'campus_entry') {
    // Main gate QR - just the app URL with a welcome parameter
    qrValue.value = `${origin}/?source=maingate&welcome=true`
    targetName.value = 'SEAIT Campus Main Gate - TechnoPath Guide'
    return
  } else if (locationType.value === 'facility') {
    id = selectedFacilityId.value
    const fac = facilities.value.find(f => f.id === id)
    label = fac ? fac.name : 'Facility'
  } else {
    id = selectedRoomId.value
    const r = rooms.value.find(f => f.id === id)
    label = r ? `${r.name} (${getFacilityName(r.facility_id)})` : 'Room'
  }
  
  // Format: /?source=qr&location=type_id
  qrValue.value = `${origin}/?source=qr&location=${locationType.value}_${id}`
  targetName.value = label
}

const downloadQR = () => {
  if (!qrWrapper.value) return
  const canvas = qrWrapper.value.querySelector('canvas')
  if (!canvas) return
  
  let filename = 'technopath_qr_'
  if (locationType.value === 'campus_entry') {
    filename += 'main_gate_campus_entry'
  } else {
    filename += targetName.value.replace(/[^a-z0-9]/gi, '_').toLowerCase()
  }
  
  const link = document.createElement('a')
  link.download = `${filename}.png`
  link.href = canvas.toDataURL('image/png')
  link.click()
}
</script>

<style scoped>
.qr-preview-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}
.qr-preview-container {
  padding: 24px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
}
.form-select {
  width: 100%;
  padding: 10px;
  border-radius: 8px;
  border: 1px solid var(--color-border);
  margin-top: 8px;
}
.mt-4 { margin-top: 16px; }
.mt-6 { margin-top: 24px; }
.mb-4 { margin-bottom: 16px; }
.justify-center { justify-content: center; }
.form-hint {
  font-size: 12px;
  color: #666;
  margin-top: 6px;
  font-style: italic;
}
</style>
