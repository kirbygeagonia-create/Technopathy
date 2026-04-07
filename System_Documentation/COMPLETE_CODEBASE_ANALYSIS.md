# TechnoPath V4 - Comprehensive Codebase Analysis

**Date:** April 5, 2026  
**Version:** 4.0  
**Project:** TechnoPath: SEAIT Guide Map and Navigation System

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Technology Stack & Dependencies](#2-technology-stack--dependencies)
3. [Project Structure](#3-project-structure)
4. [Backend Analysis (Django)](#4-backend-analysis-django)
5. [Frontend Analysis (Vue.js)](#5-frontend-analysis-vuejs)
6. [Database Architecture](#6-database-architecture)
7. [API Endpoints](#7-api-endpoints)
8. [Services & Data Flow](#8-services--data-flow)
9. [Key Algorithms](#9-key-algorithms)
10. [Installation & Setup Requirements](#10-installation--setup-requirements)

---

## 1. Project Overview

TechnoPath is a **Progressive Web Application (PWA)** designed for South East Asian Institute of Technology (SEAIT) campus navigation. It provides:

- Interactive 2D campus maps with building floor plans
- Turn-by-turn navigation using Dijkstra's algorithm
- AI-powered chatbot with offline fallback
- Role-based admin panel (Super Admin, Dean, Program Head, Basic Ed Head)
- QR code access points
- Offline-first architecture using IndexedDB

---

## 2. Technology Stack & Dependencies

### 2.1 Backend Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| **Django** | >=4.2 | Web framework |
| **Django REST Framework** | >=3.15 | API toolkit |
| **djangorestframework-simplejwt** | >=5.3 | JWT authentication |
| **django-cors-headers** | >=4.3 | CORS handling |
| **python-decouple** | >=3.8 | Environment config |
| **Pillow** | >=10.0 | Image processing |
| **Flask** | >=3.0 | AI chatbot microservice |
| **flask-cors** | >=4.0 | Flask CORS |
| **requests** | >=2.31.0 | HTTP library |

### 2.2 Frontend Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| **Vue.js** | ^3.4.0 | Frontend framework |
| **Vue Router** | ^4.3.0 | Client-side routing |
| **Pinia** | ^2.1.0 | State management |
| **Axios** | ^1.6.0 | HTTP client |
| **Dexie** | ^3.2.0 | IndexedDB wrapper |
| **Leaflet** | ^1.9.4 | Map library |
| **Fuse.js** | ^7.0.0 | Fuzzy search |
| **jsQR** | ^1.4.0 | QR code scanning |
| **lucide-vue-next** | ^1.0.0 | Icons |
| **qrcode.vue** | ^3.8.1 | QR code generation |
| **Vite** | ^6.2.0 | Build tool |
| **vite-plugin-pwa** | ^0.19.8 | PWA support |

### 2.3 Database Systems

- **PostgreSQL** - Production database
- **SQLite** - Development database (technopath.db)
- **IndexedDB** - Browser offline storage

---

## 3. Project Structure

```
technopath_pwa/version4_technopath/
├── backend_django/           # Django backend
│   ├── apps/                 # Django applications
│   │   ├── announcements/    # Announcement system with approval workflow
│   │   ├── chatbot/          # FAQ & AI chat log models
│   │   ├── core/             # Core models (departments, audit, analytics)
│   │   ├── facilities/       # Buildings & facilities management
│   │   ├── feedback/         # User feedback system
│   │   ├── navigation/       # Navigation graph (nodes & edges)
│   │   ├── notifications/    # Push notifications
│   │   ├── rooms/            # Room management
│   │   └── users/            # Admin user authentication
│   ├── technopath/           # Django project settings
│   │   ├── settings.py       # Main configuration
│   │   ├── urls.py           # URL routing
│   │   └── wsgi.py           # WSGI entry
│   ├── manage.py             # Django management
│   ├── requirements.txt      # Python dependencies
│   └── technopath.db         # SQLite database
│
├── frontend/                 # Vue.js frontend
│   ├── src/
│   │   ├── components/       # Vue components
│   │   │   ├── admin/        # Admin panel components (12 files)
│   │   │   └── *.vue         # Shared components
│   │   ├── views/            # Page views (14 files)
│   │   ├── services/         # Business logic (8 files)
│   │   ├── stores/           # Pinia stores (3 files)
│   │   ├── router/           # Vue Router config
│   │   ├── assets/           # Static assets
│   │   ├── App.vue           # Root component
│   │   └── main.js           # Entry point
│   ├── package.json          # NPM dependencies
│   └── vite.config.js        # Vite configuration
│
├── chatbot_flask/            # Flask AI service (optional)
│   └── requirements.txt      # Flask dependencies
│
├── System_Documentation/     # Documentation folder
│   └── *.md                  # Various documentation files
│
└── web/                      # Static web files
    └── manifest.json         # PWA manifest
```

---

## 4. Backend Analysis (Django)

### 4.1 Django Apps Structure

| App | Models | Views | Serializers | Purpose |
|-----|--------|-------|-------------|---------|
| **users** | AdminUser | LoginView, AdminListCreateView, AuditLogView | N/A | Authentication & RBAC |
| **facilities** | Facility | FacilityListView, FacilityDetailView | FacilitySerializer | Building management |
| **rooms** | Room | RoomListView, RoomDetailView | RoomSerializer | Room management |
| **navigation** | NavigationNode, NavigationEdge | NavigationNodeListView, NavigationEdgeListView | NavigationNodeSerializer, NavigationEdgeSerializer | Pathfinding graph |
| **chatbot** | FAQEntry, AIChatLog | FAQListView, ChatLogView | FAQEntrySerializer | AI chatbot data |
| **notifications** | Notification, NotificationReadStatus | NotificationListView | NotificationSerializer | Push notifications |
| **feedback** | Feedback | FeedbackListView | FeedbackSerializer | User feedback |
| **announcements** | Announcement | AnnouncementListView, PendingApprovalsView | AnnouncementSerializer | Announcements with approval |
| **core** | Department, MapMarker, MapLabel, Rating, FeedbackFlag, AdminAuditLog, SearchHistory, AppUsage, UsageAnalytics, DevicePreference, AppConfig, ConnectivityLog | 14+ view classes | 14+ serializers | Core functionality |

### 4.2 Key Models & Relationships

#### AdminUser (Custom User Model)
```python
# Located in: apps/users/models.py

ROLE_CHOICES = [
    ('super_admin',   'Safety and Security Office'),
    ('dean',          'College Dean'),
    ('program_head',  'College Program Head'),
    ('basic_ed_head', 'Basic Education Head'),
]

DEPARTMENT_CHOICES = [
    ('safety_security',          'Safety and Security Office'),
    ('office_of_the_dean',       'Office of the Dean'),
    ('college_agriculture',      'College of Agriculture and Fisheries'),
    ('college_criminology',      'College of Criminal Justice Education'),
    ('college_business',         'College of Business and Good Governance'),
    ('college_ict',              'College of Information and Communication Technology'),
    ('dept_civil_engineering',   'Department of Civil Engineering'),
    ('college_teacher_education','College of Teacher Education'),
    ('tesda',                    'Technical Education and Skills Development Authority'),
    ('general_education',        'General Education Department'),
    ('basic_education',          'Basic Education Department'),
]
```

**Key Methods:**
- `can_manage_facilities()` - Super Admin only
- `can_manage_all_rooms()` - Super Admin only
- `can_manage_own_rooms()` - Dean, Program Head, Basic Ed Head
- `can_approve_announcements()` - Super Admin only
- `can_publish_directly()` - Super Admin always, Dean for department only
- `get_permissions_dict()` - Returns all permissions for JWT response

#### Department Model
```python
# Located in: apps/core/models.py

class Department(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)
    head_user = models.ForeignKey('users.AdminUser', on_delete=models.SET_NULL, 
                                   null=True, blank=True, related_name='headed_departments')
    is_active = models.BooleanField(default=True)
```

#### Navigation Graph Models
```python
# Located in: apps/navigation/models.py

class NavigationNode(models.Model):
    NODE_TYPES = [
        ('room', 'Room'), ('facility', 'Facility'), ('waypoint', 'Waypoint'),
        ('entrance', 'Entrance'), ('staircase', 'Staircase'),
        ('elevator', 'Elevator'), ('junction', 'Junction'),
    ]
    name = models.CharField(max_length=200)
    node_type = models.CharField(max_length=20, choices=NODE_TYPES)
    facility = models.ForeignKey(Facility, on_delete=models.SET_NULL, null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)
    x = models.FloatField()
    y = models.FloatField()
    floor = models.IntegerField(default=1)
    is_deleted = models.BooleanField(default=False)

class NavigationEdge(models.Model):
    from_node = models.ForeignKey(NavigationNode, on_delete=models.CASCADE, related_name='edges_from')
    to_node = models.ForeignKey(NavigationNode, on_delete=models.CASCADE, related_name='edges_to')
    distance = models.IntegerField()
    is_bidirectional = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
```

#### Announcement Model (with Approval Workflow)
```python
# Located in: apps/announcements/models.py

class Announcement(models.Model):
    STATUS_CHOICES = [
        ('pending_approval', 'Pending Approval'),
        ('published',        'Published'),
        ('rejected',         'Rejected'),
        ('archived',         'Archived'),
    ]
    
    SCOPE_CHOICES = [
        ('campus_wide',       'Entire Campus'),
        ('all_college',       'All College Students'),
        ('basic_ed_only',     'Basic Education Only'),
        ('department',        'Specific Department Only'),
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_by = models.ForeignKey('users.AdminUser', on_delete=models.SET_NULL, null=True)
    source_label = models.CharField(max_length=200)  # Department label for display
    source_color = models.CharField(max_length=20, default='orange')
    scope = models.CharField(max_length=20, choices=SCOPE_CHOICES, default='campus_wide')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending_approval')
    requires_approval = models.BooleanField(default=True)
    approved_by = models.ForeignKey('users.AdminUser', on_delete=models.SET_NULL, 
                                   null=True, blank=True, related_name='approved_announcements')
    rejected_by = models.ForeignKey('users.AdminUser', on_delete=models.SET_NULL,
                                   null=True, blank=True, related_name='rejected_announcements')
    rejection_note = models.TextField(blank=True, null=True)
```

### 4.3 Django Settings Configuration

```python
# Key settings from technopath/settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',
    'apps.users',
    'apps.facilities',
    'apps.rooms',
    'apps.navigation',
    'apps.chatbot',
    'apps.notifications',
    'apps.feedback',
    'apps.core',
    'apps.announcements',
]

AUTH_USER_MODEL = 'users.AdminUser'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=8),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}

CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'http://localhost:3000',
    'http://127.0.0.1:5173',
]
```

---

## 5. Frontend Analysis (Vue.js)

### 5.1 Vue Application Structure

```javascript
// main.js - Application entry point

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router/index.js'
import { syncAllData, registerConnectivityListener } from './services/sync.js'

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.mount('#app')

// Initial data sync
syncAllData().then(result => {
  if (result.success) {
    console.log('TechnoPath: Data synced at', result.syncedAt)
  } else {
    console.log('TechnoPath: Running offline with cached data')
  }
})

// Auto-sync on reconnection
registerConnectivityListener((result) => {
  console.log('TechnoPath: Reconnected and synced:', result)
})
```

### 5.2 Router Configuration

```javascript
// router/index.js

const routes = [
  { path: '/', redirect: '/home' },
  { path: '/splash', component: SplashScreen },
  { path: '/home', component: HomeView },
  { path: '/map', component: MapView },
  { path: '/navigate', component: NavigateView },
  { path: '/chatbot', component: ChatbotView },
  { path: '/notifications', component: NotificationsView },
  { path: '/settings', component: SettingsView },
  { path: '/profile', component: ProfileView },
  { path: '/favorites', component: FavoritesView },
  { path: '/feedback', component: FeedbackView },
  { path: '/qr-scanner', component: QRScannerView },
  { path: '/info', component: InfoView },
  { path: '/admin-login', component: AdminLoginView },
  { path: '/admin', component: AdminView, meta: { requiresAuth: true } },
]
```

### 5.3 Views (Pages)

| View | File | Purpose |
|------|------|---------|
| **HomeView** | `views/HomeView.vue` | Main campus map with search |
| **MapView** | `views/MapView.vue` | Interactive 2D floor plans |
| **NavigateView** | `views/NavigateView.vue` | Turn-by-turn navigation |
| **ChatbotView** | `views/ChatbotView.vue` | AI chatbot interface |
| **NotificationsView** | `views/NotificationsView.vue` | In-app notifications |
| **QRScannerView** | `views/QRScannerView.vue` | QR code scanning |
| **AdminView** | `views/AdminView.vue` | Admin panel shell |
| **AdminLoginView** | `views/AdminLoginView.vue` | Admin authentication |

### 5.4 Admin Components

| Component | File | Purpose |
|-----------|------|---------|
| **AdminDashboard** | `admin/AdminDashboard.vue` | Statistics & overview |
| **AdminFacilities** | `admin/AdminFacilities.vue` | Facility CRUD |
| **AdminRooms** | `admin/AdminRooms.vue` | Room CRUD |
| **AdminNavGraph** | `admin/AdminNavGraph.vue` | Navigation graph editor |
| **AdminFAQ** | `admin/AdminFAQ.vue` | FAQ management |
| **AdminQRCode** | `admin/AdminQRCode.vue` | QR code generator |
| **AdminAnnouncements** | `admin/AdminAnnouncements.vue` | Create announcements |
| **AdminPendingApprovals** | `admin/AdminPendingApprovals.vue` | Approve/reject workflow |
| **AdminSendNotification** | `admin/AdminSendNotification.vue` | Send notifications |
| **AdminAccounts** | `admin/AdminAccounts.vue` | User management |
| **AdminFeedback** | `admin/AdminFeedback.vue` | View feedback |
| **AdminAuditLog** | `admin/AdminAuditLog.vue` | View audit trail |

---

## 6. Database Architecture

### 6.1 Complete Table List (25+ Tables)

#### Core Entity Tables
| Table | Django Model | Key Fields |
|-------|--------------|------------|
| **admin_users** | AdminUser | username, role, department, password, login_attempts |
| **departments** | Department | name, code, head_user_id |
| **facilities** | Facility | name, code, department_id, latitude, longitude |
| **rooms** | Room | name, facility_id, floor, x, y, room_type |

#### Navigation Tables
| Table | Django Model | Key Fields |
|-------|--------------|------------|
| **navigation_nodes** | NavigationNode | name, node_type, x, y, floor, facility_id, room_id |
| **navigation_edges** | NavigationEdge | from_node_id, to_node_id, distance, is_bidirectional |

#### Map Visualization Tables
| Table | Django Model | Key Fields |
|-------|--------------|------------|
| **map_markers** | MapMarker | name, x_position, y_position, marker_type, facility_id, room_id |
| **map_labels** | MapLabel | label_text, x_position, y_position, font_size, rotation |

#### Communication Tables
| Table | Django Model | Key Fields |
|-------|--------------|------------|
| **announcements** | Announcement | title, content, created_by, status, scope, approved_by |
| **notifications** | Notification | title, message, type, source_label, announcement_id |
| **notification_read_status** | NotificationReadStatus | user_id, notification_id, read_at |
| **notification_types** | NotificationType | name, icon_name, color_hex |
| **notification_preferences** | NotificationPreference | user_id, notification_type_id, is_enabled |

#### Chatbot Tables
| Table | Django Model | Key Fields |
|-------|--------------|------------|
| **faq_entries** | FAQEntry | question, answer, category, keywords, usage_count |
| **ai_chat_logs** | AIChatLog | user_query, ai_response, mode, faq_entry_id |

#### Feedback System Tables
| Table | Django Model | Key Fields |
|-------|--------------|------------|
| **feedback** | Feedback | rating, comment, category, facility_id, room_id |
| **ratings** | Rating | rating, comment, category, facility_id, room_id, user_id |
| **feedback_flags** | FeedbackFlag | rating_id, reason, status, resolved_by |

#### Audit & Analytics Tables
| Table | Django Model | Key Fields |
|-------|--------------|------------|
| **admin_audit_log** | AdminAuditLog | admin_id, action, entity_type, old_value_json, new_value_json |
| **search_history** | SearchHistory | user_id, query, results_count, was_clicked |
| **app_usage** | AppUsage | user_id, session_date, session_duration, screen_views |
| **usage_analytics** | UsageAnalytics | user_id, event_type, event_data, screen_name |

#### System Configuration Tables
| Table | Django Model | Key Fields |
|-------|--------------|------------|
| **device_preferences** | DevicePreference | device_id, dark_mode, font_scale, high_contrast |
| **app_config** | AppConfig | config_key, config_value, description |
| **connectivity_log** | ConnectivityLog | user_id, is_online, connection_type, latency_ms |

### 6.2 Entity Relationship Diagram

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  departments    │────<│  admin_users    │     │  facilities     │
│  (head_user)    │     │  (role-based)   │     │  (department)   │
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                         │
                              ┌─────────────────────────┼─────────────────────────┐
                              │                         │                         │
                              ▼                         ▼                         ▼
                    ┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
                    │     rooms       │       │ navigation_nodes│       │  map_markers    │
                    │  (facility)     │       │(facility/room)  │       │(facility/room)  │
                    └─────────────────┘       └────────┬────────┘       └─────────────────┘
                                                      │
                              ┌───────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │ navigation_edges│
                    │(from_node/to)   │
                    └─────────────────┘
```

---

## 7. API Endpoints

### 7.1 URL Routing Structure

```python
# technopath/urls.py

urlpatterns = [
    path('', api_root, name='api-root'),
    path('admin/', admin.site.urls),
    path('api/auth/login/', TokenObtainPairView.as_view()),
    path('api/auth/refresh/', TokenRefreshView.as_view()),
    path('api/users/', include('apps.users.urls')),
    path('api/facilities/', include('apps.facilities.urls')),
    path('api/rooms/', include('apps.rooms.urls')),
    path('api/navigation/', include('apps.navigation.urls')),
    path('api/chatbot/', include('apps.chatbot.urls')),
    path('api/notifications/', include('apps.notifications.urls')),
    path('api/feedback/', include('apps.feedback.urls')),
    path('api/core/', include('apps.core.urls')),
    path('api/announcements/', include('apps.announcements.urls')),
]
```

### 7.2 Complete API Endpoint List

#### Authentication Endpoints
| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| POST | `/api/auth/login/` | JWT login | Public |
| POST | `/api/auth/refresh/` | Refresh token | Public |
| POST | `/api/users/login/` | Custom login with audit | Public |
| POST | `/api/users/logout/` | Logout with audit | Authenticated |
| GET | `/api/users/me/` | Get current user | Authenticated |

#### Admin Management (Super Admin Only)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/users/admins/` | List admin accounts |
| POST | `/api/users/admins/` | Create admin account |
| PUT | `/api/users/admins/<id>/` | Update admin account |
| DELETE | `/api/users/admins/<id>/` | Deactivate admin |
| GET | `/api/users/audit-log/` | View audit log |

#### Facilities
| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| GET | `/api/facilities/` | List facilities | ReadOnlyOrSuperAdmin |
| POST | `/api/facilities/` | Create facility | Super Admin |
| GET | `/api/facilities/<id>/` | Get facility detail | ReadOnlyOrSuperAdmin |
| PUT | `/api/facilities/<id>/` | Update facility | Super Admin |
| DELETE | `/api/facilities/<id>/` | Soft delete | Super Admin |

#### Rooms
| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| GET | `/api/rooms/` | List rooms | CanManageRoom |
| POST | `/api/rooms/` | Create room | CanManageRoom |
| GET | `/api/rooms/<id>/` | Get room detail | CanManageRoom |
| PUT | `/api/rooms/<id>/` | Update room | CanManageRoom |
| DELETE | `/api/rooms/<id>/` | Soft delete | CanManageRoom |

#### Navigation
| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| GET | `/api/navigation/nodes/` | List nodes | ReadOnlyOrSuperAdmin |
| POST | `/api/navigation/nodes/` | Create node | Super Admin |
| GET | `/api/navigation/edges/` | List edges | ReadOnlyOrSuperAdmin |
| POST | `/api/navigation/edges/` | Create edge | Super Admin |

#### Core Data
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/core/departments/` | List departments |
| GET | `/api/core/map-markers/` | List map markers |
| GET | `/api/core/map-labels/` | List map labels |
| GET | `/api/core/ratings/` | List ratings |
| GET | `/api/core/search-history/` | List search history |
| GET | `/api/core/app-config/` | Get app configuration |

#### Announcements
| Method | Endpoint | Description | Permission |
|--------|----------|-------------|------------|
| GET | `/api/announcements/` | List announcements | Authenticated |
| POST | `/api/announcements/` | Create announcement | CanPost |
| GET | `/api/announcements/pending/` | List pending | CanApprove |
| POST | `/api/announcements/<id>/approve/` | Approve | CanApprove |
| POST | `/api/announcements/<id>/reject/` | Reject | CanApprove |

---

## 8. Services & Data Flow

### 8.1 Frontend Services

#### API Service (`services/api.js`)
```javascript
import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json'
  }
})

// JWT token interceptor
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('tp_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})
```

#### Offline Data Service (`services/offlineData.js`)
```javascript
// Key functions:
- getFacilities()           // Facilities with caching
- getRooms(facilityId)      // Rooms with facility filter
- getMapMarkers()           // Map markers
- getNavigationData()       // Nodes & edges for pathfinding
- getFAQEntries()           // FAQ for chatbot
- getNotifications()        // Notifications with read states
- getAppConfig()            // App configuration
- getOfflineStatus()        // Cache status summary
```

#### Pathfinder Service (`services/pathfinder.js`)
```javascript
// Dijkstra's algorithm implementation
export function dijkstra(nodes, edges, startId, endId)

// Find path between locations
export async function findPath(startName, endName)

// Generate turn-by-turn directions
function generateSteps(pathNodes, totalDistance)

// Calculate turn angle
function calculateAngle(p1, p2, p3)
```

#### AI Chatbot Service (`services/aiChatbot.js`)
```javascript
// Priority chain:
// 1. Flask Chatbot API (if online)
// 2. OpenAI API (if configured & online)
// 3. Rule-based fallback (always works)

export async function sendMessage(userMessage)
export function clearHistory()
export function getStatus()
export async function initChatHistory()
```

#### Sync Service (`services/sync.js`)
```javascript
// Key functions:
- isOnline()                // Check connectivity
- syncAllData()             // Full data sync
- registerConnectivityListener(callback)  // Auto-sync on reconnect
- getSyncStatus()           // Sync metadata
```

### 8.2 IndexedDB Schema (`services/db.js`)
```javascript
import Dexie from 'dexie'

const db = new Dexie('TechnoPathDB')

db.version(1).stores({
  facilities: 'id, name, code, department_id',
  rooms: 'id, name, facility_id, floor, room_type',
  map_markers: 'id, name, facility_id, room_id, marker_type',
  navigation_nodes: 'id, name, node_type, floor',
  navigation_edges: 'id, from_node_id, to_node_id',
  faq_entries: 'id, question, category, keywords',
  notifications: 'id, title, type, is_read, created_at',
  app_config: 'id, config_key',
  ai_chat_logs: '++id, mode, created_at',
  sync_meta: 'key'  // Last sync timestamp
})
```

### 8.3 Auth Store (`stores/authStore.js`)
```javascript
// Pinia store for authentication

state: {
  user: null,           // Current user object
  token: null,          // JWT access token
  refreshToken: null    // JWT refresh token
}

getters: {
  isLoggedIn, isAdmin, isSuperAdmin, isDean,
  isProgramHead, isBasicEdHead,
  // 20+ permission getters from login response
  canManageFacilities, canManageAllRooms, canManageOwnRooms,
  canApproveAnnouncements, canPublishDirectly, // etc.
}

actions: {
  login(username, password)   // JWT login
  logout()                    // Clear session
}
```

---

## 9. Key Algorithms

### 9.1 Dijkstra's Shortest Path Algorithm

```javascript
// Located in: services/pathfinder.js

export function dijkstra(nodes, edges, startId, endId) {
  const distances = {}
  const previous = {}
  const visited = new Set()
  const queue = []

  // Initialize distances
  nodes.forEach(n => {
    distances[n.id] = Infinity
    previous[n.id] = null
  })
  distances[startId] = 0
  queue.push({ id: startId, dist: 0 })

  while (queue.length > 0) {
    queue.sort((a, b) => a.dist - b.dist)
    const { id: currentId } = queue.shift()

    if (visited.has(currentId)) continue
    visited.add(currentId)
    if (currentId === endId) break

    // Find neighbors
    const neighbors = edges.filter(
      e => (!e.is_deleted) && (
        e.from_node_id === currentId ||
        (e.is_bidirectional && e.to_node_id === currentId)
      )
    )

    // Update distances
    for (const edge of neighbors) {
      const neighborId = edge.from_node_id === currentId 
        ? edge.to_node_id 
        : edge.from_node_id
      if (visited.has(neighborId)) continue
      const newDist = distances[currentId] + edge.distance
      if (newDist < distances[neighborId]) {
        distances[neighborId] = newDist
        previous[neighborId] = currentId
        queue.push({ id: neighborId, dist: newDist })
      }
    }
  }

  // Reconstruct path
  const path = []
  let current = endId
  while (current !== null) {
    path.unshift(current)
    current = previous[current]
  }

  if (path[0] !== startId) return null
  return { path, distance: distances[endId] }
}
```

### 9.2 Turn Angle Calculation

```javascript
function calculateAngle(p1, p2, p3) {
  const dx1 = p2.x - p1.x
  const dy1 = p2.y - p1.y
  const dx2 = p3.x - p2.x
  const dy2 = p3.y - p2.y
  
  const angle1 = Math.atan2(dy1, dx1)
  const angle2 = Math.atan2(dy2, dx2)
  
  let angle = (angle2 - angle1) * 180 / Math.PI
  if (angle > 180) angle -= 360
  if (angle < -180) angle += 360
  
  return angle
}

// Turn classification:
// angle > 30°   -> "Turn right"
// angle < -30°  -> "Turn left"
// |angle| > 150° -> "Make a U-turn"
```

---

## 10. Installation & Setup Requirements

### 10.1 Machine Requirements

#### Backend (Python/Django)
```bash
# Required software:
- Python 3.8+ (3.10 recommended)
- pip (Python package manager)
- PostgreSQL 14+ (for production)
- SQLite 3 (included with Python, for development)

# Optional:
- Git (for version control)
- Virtual environment (venv)
```

#### Frontend (Node.js/Vue.js)
```bash
# Required software:
- Node.js 18+ (LTS recommended)
- npm 9+ or yarn 1.22+

# Optional:
- Git (for version control)
```

### 10.2 Installation Steps

#### Backend Setup
```bash
# 1. Navigate to backend directory
cd backend_django

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run migrations
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Start server
python manage.py runserver
```

#### Frontend Setup
```bash
# 1. Navigate to frontend directory
cd frontend

# 2. Install dependencies
npm install

# 3. Start development server
npm run dev

# 4. Build for production
npm run build
```

#### Environment Variables

**Backend (.env file in backend_django/):**
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

**Frontend (.env file in frontend/):**
```env
VITE_API_URL=http://localhost:8000
VITE_FLASK_CHATBOT_URL=http://localhost:5000
VITE_OPENAI_API_KEY=your-openai-key (optional)
```

### 10.3 Default Ports

| Service | Port | URL |
|---------|------|-----|
| Django Backend | 8000 | http://localhost:8000 |
| Vue.js Frontend | 5173 | http://localhost:5173 |
| Flask Chatbot | 5000 | http://localhost:5000 (optional) |

---

## Summary

This comprehensive analysis documents the complete TechnoPath V4 codebase including:

- **25+ database tables** with full relationship mapping
- **9 Django apps** with models, views, and serializers
- **14 Vue.js views** and **19+ components**
- **8 frontend services** for offline/online data management
- **Role-based access control** with 4 user tiers
- **Offline-first architecture** using IndexedDB
- **Dijkstra's algorithm** for campus navigation
- **AI chatbot** with 3-tier fallback system

The system is designed as a Progressive Web Application with full offline capability, making it ideal for campus navigation even without internet connectivity.

---

*Generated: April 5, 2026*
*TechnoPath V4 - SEAIT Campus Guide System*
