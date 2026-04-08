import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router/index.js'
import '@fontsource/inter/400.css'
import '@fontsource/inter/500.css'
import '@fontsource/inter/600.css'
import '@fontsource/inter/700.css'
import './assets/main.css'
import 'material-icons/iconfont/material-icons.css'
import { useSyncStore } from './stores/syncStore.js'
import { registerConnectivityListener } from './services/sync.js'

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.mount('#app')

// On app load: sync data from Django to IndexedDB if online
// Use syncStore to properly manage isSyncing state
const syncStore = useSyncStore()
syncStore.sync().then(() => {
  if (syncStore.lastSyncedAt) {
    console.log('TechnoPath: Data synced at', syncStore.lastSyncedAt)
  } else {
    console.log('TechnoPath: Running offline with cached data')
  }
})

// Auto-sync whenever the device reconnects to the internet
registerConnectivityListener(() => {
  syncStore.sync()
  console.log('TechnoPath: Reconnected and synced')
})
