import Dexie from 'dexie'

const db = new Dexie('TechnoPathDB')

// Version 4: Standardize soft-delete fields to match backend (is_deleted pattern)
// Note: is_deleted = true means soft-deleted (hidden from normal queries)
//       is_active = status field for enabling/disabling (separate from soft-delete)
db.version(4).stores({
  // Core entities - use is_deleted for soft-delete (matches backend)
  facilities:        '++id, code, map_svg_id, is_deleted',
  rooms:             '++id, facility_id, code, map_svg_id, floor, is_deleted',
  departments:       '++id, code, is_active',  // is_active = status field
  
  // Navigation - use is_deleted for soft-delete
  navigation_nodes:  '++id, map_svg_id, node_type, floor, is_deleted',
  navigation_edges:  '++id, from_node_id, to_node_id, is_deleted',
  
  // Map - use is_deleted for soft-delete (was is_active)
  map_markers:       '++id, facility_id, room_id, marker_type, is_deleted',
  map_labels:        '++id, is_deleted',
  
  // Chatbot
  faq_entries:       '++id, category, keywords, is_deleted',
  ai_chat_logs:      '++id, mode, created_at',
  
  // Notifications
  notifications:     '++id, type, is_read, source_color, created_at',
  notification_types: '++id, name, is_active',  // status field
  notification_preferences: '++id, user_id, notification_type_id',
  
  // Feedback & Ratings
  feedback:          '++id, category, synced, created_at',
  ratings:           '++id, facility_id, room_id, category, is_deleted, created_at',
  feedback_flags:    '++id, rating_id, status, created_at',
  
  // Analytics & Audit
  search_history:    '++id, query, created_at',
  admin_audit_log:   '++id, action, entity_type, created_at',
  // NOTE: Removed unused tables: app_usage, usage_analytics, connectivity_log
  
  // User & Device
  users:             '++id, username, role, is_active',  // is_active = account status
  device_preferences: '++id, user_id, device_id',
  
  // Config
  app_config:        '++id, config_key',
  
  // Sync metadata
  sync_meta:         'key'
}).upgrade(tx => {
  // Migration: Update existing data where is_active was used as soft-delete
  // Convert is_active=false to is_deleted=true for affected tables
  return Promise.all([
    // Facilities: if is_active exists and is false, set is_deleted=true
    tx.table('facilities').toCollection().modify(facility => {
      if (facility.is_active === false && !facility.is_deleted) {
        facility.is_deleted = true
      }
      delete facility.is_active  // Remove old field
    }),
    // Rooms
    tx.table('rooms').toCollection().modify(room => {
      if (room.is_active === false && !room.is_deleted) {
        room.is_deleted = true
      }
      delete room.is_active
    }),
    // Navigation nodes
    tx.table('navigation_nodes').toCollection().modify(node => {
      if (node.is_active === false && !node.is_deleted) {
        node.is_deleted = true
      }
      delete node.is_active
    }),
    // Map markers
    tx.table('map_markers').toCollection().modify(marker => {
      if (marker.is_active === false && !marker.is_deleted) {
        marker.is_deleted = true
      }
      delete marker.is_active
    }),
    // Map labels
    tx.table('map_labels').toCollection().modify(label => {
      if (label.is_active === false && !label.is_deleted) {
        label.is_deleted = true
      }
      delete label.is_active
    }),
    // Ratings
    tx.table('ratings').toCollection().modify(rating => {
      if (rating.is_active === false && !rating.is_deleted) {
        rating.is_deleted = true
      }
      // Keep is_active as separate status field
    })
  ])
})

export default db
