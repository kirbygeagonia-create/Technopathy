# TechnoPath: SEAIT Guide Map and Navigation System
## Functional Decomposition Diagram (FDD)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                    TECHNOPATH: SEAIT GUIDE MAP AND NAVIGATION SYSTEM                      │
└─────────────────────────────────────────────────────────────────────────────────────────┘
                                          │
        ┌─────────────────────────────────┼─────────────────────────────────┐
        │                                 │                                 │
┌───────▼────────┐              ┌──────────▼──────────┐            ┌────────▼───────┐
│  MOBILE USER   │              │    ADMIN PANEL      │            │  SYSTEM CORE   │
│    MODULE      │              │      MODULE         │            │    MODULE      │
└───────┬────────┘              └──────────┬──────────┘            └────────┬───────┘
        │                                  │                                │
        ▼                                  ▼                                ▼
┌───────────────────┐           ┌──────────────────────┐        ┌────────────────────┐
│ ┌───────────────┐ │           │ ┌──────────────────┐ │        │ ┌────────────────┐ │
│ │ Campus Map    │ │           │ │ Admin Management │ │        │ │ Database       │ │
│ │ View          │ │           │ │ (Dashboard)      │ │        │ │ Management     │ │
│ └───────┬───────┘ │           │ └────────┬─────────┘ │        │ └────────┬───────┘ │
│         │         │           │          │           │        │          │         │
│ ┌───────▼───────┐ │           │ ┌────────▼────────┐  │        │ ┌────────▼───────┐ │
│ │ Search &      │ │           │ │ Map Management  │  │        │ │ API Services   │ │
│ │ Discovery     │ │           │ │   Sub-Module    │  │        │ │ (REST API)     │ │
│ └───────┬───────┘ │           │ ├─ Facilities     │  │        │ └────────────────┘ │
│         │         │           │ ├─ Rooms         │  │        │                    │
│ ┌───────▼───────┐ │           │ ├─ Navigation     │  │        │ ┌────────────────┐ │
│ │ Navigation    │ │           │ │   Graph        │  │        │ │ Sync & Offline │ │
│ │ System        │ │           │ ├─ FAQ/Chatbot   │  │        │ │ Services       │ │
│ └───────┬───────┘ │           │ └─ QR Codes      │  │        │ └────────────────┘ │
│         │         │           │                   │  │        │                    │
│ ┌───────▼───────┐ │           │ ┌────────────────┐  │  │        │ ┌────────────────┐ │
│ │ AI Chatbot    │ │           │ │ Communications │  │  │        │ │ Analytics      │ │
│ │ Assistant     │ │           │ │   Sub-Module   │  │  │        │ │ & Reporting    │ │
│ └───────┬───────┘ │           │ ├─ Announcements │  │  │        │ └────────────────┘ │
│         │         │           │ ├─ Pending       │  │  │        └────────────────────┘
│ ┌───────▼───────┐ │           │ │   Approvals    │  │  │
│ │ Notifications │ │           │ ├─ Send          │  │  │
│ │ System        │ │           │ │   Notification │  │  │
│ └───────┬───────┘ │           │ └────────────────┘  │  │
│         │         │           │                     │  │
│ ┌───────▼───────┐ │           │ ┌────────────────┐  │  │
│ │ Information   │ │           │ │ Administration │  │  │
│ │ Center        │ │           │ │   Sub-Module   │  │  │
│ ├─ Building     │ │           │ ├─ Admin Accounts│  │  │
│ │   Info        │ │           │ ├─ Feedback &    │  │  │
│ ├─ Rooms Info   │ │           │ │   Ratings      │  │  │
│ ├─ Instructor   │ │           │ ├─ Audit Log     │  │  │
│ │   Info        │ │           │ └────────────────┘  │  │
│ └─ Employees    │ │           └───────────────────────┘  │
└───────────────────┘
        │
┌───────▼───────────────┐
│ User Engagement Module│
├─ Favorites            │
├─ Ratings & Feedback   │
├─ Profile Management   │
└─ Settings             │
└───────────────────────┘
```

## Detailed Functional Decomposition

### 1. MOBILE USER MODULE (Guest Access - Students, Visitors, Faculty)

#### 1.1 Campus Map View
- Interactive SEAIT campus map with SVG overlay
- Facility and room markers with positioning
- Zoom and pan controls
- Deep linking via QR codes
- Offline map rendering

#### 1.2 Search & Discovery
- Real-time search with autocomplete
- Recent searches history
- Facility/room filtering
- Search result navigation
- Location-based suggestions

#### 1.3 Navigation System
- Point-to-point routing
- Turn-by-turn directions
- Route visualization with SVG overlay
- Walking distance and time estimation
- QR code scanning for quick location access

#### 1.4 AI Chatbot Assistant
- Natural language query processing
- FAQ-based offline responses
- Online AI-powered responses (when available)
- Quick action suggestions
- Chat history management

#### 1.5 Notifications System
- Push notifications for announcements
- Department-scoped notifications
- Read status tracking
- Notification preferences
- Emergency alerts

#### 1.6 Information Center
- Building information database
- Room details and schedules
- Instructor directory
- Employee directory
- Department contacts

#### 1.7 User Engagement
- Favorite locations management
- App rating system
- Feedback submission
- User profile preferences
- App settings (theme, language, accessibility)

---

### 2. ADMIN PANEL MODULE (Role-Based Access)

#### 2.1 Admin Dashboard (Management Hub)
- System overview with statistics
- Quick action shortcuts
- Pending approvals counter
- Recent activity feed
- Department-specific widgets

#### 2.2 Map Management Sub-Module
**Facilities Management**
- CRUD operations for buildings
- Facility metadata (description, location, floors)
- Image management
- QR code generation

**Rooms Management**
- Room CRUD per facility
- Room type classification
- Floor and capacity management
- SVG map ID linking

**Navigation Graph**
- Node management (waypoints, rooms, entrances)
- Edge creation for pathways
- Distance calculations
- Graph visualization

**FAQ/Chatbot Management**
- FAQ entry CRUD
- Category organization
- Keyword tagging
- Usage analytics

**QR Code Management**
- Facility QR generation
- Room QR generation
- QR linking to map locations

#### 2.3 Communications Sub-Module
**Announcements**
- Create department/campus-wide announcements
- Approval workflow management
- Scope selection (campus-wide, college, basic ed, department)
- Target department filtering

**Pending Approvals** (Super Admin only)
- Review pending announcements
- Approve/reject with notes
- Bulk approval actions

**Send Notifications**
- Immediate push notifications
- Priority levels (normal, important, urgent, emergency)
- Target audience selection
- Expiration settings

#### 2.4 Administration Sub-Module
**Admin Accounts** (Super Admin only)
- Create/edit admin users
- Role assignment (Super Admin, Dean, Program Head, Basic Ed Head)
- Department assignment
- Account activation/deactivation
- Login attempt monitoring

**Feedback & Ratings**
- View all user feedback
- Flag inappropriate content
- Response management
- Analytics by category

**Audit Log**
- Complete activity tracking
- Action filtering (login, CRUD, approvals)
- IP address logging
- Data change history

---

### 3. SYSTEM CORE MODULE

#### 3.1 Database Management
- PostgreSQL/SQLite database
- Model relationships
- Data integrity constraints
- Migration management

#### 3.2 API Services (REST API)
- Django REST Framework endpoints
- JWT authentication
- Rate limiting
- API versioning
- CORS handling

#### 3.3 Sync & Offline Services
- Background data synchronization
- IndexedDB caching
- Offline-first architecture
- Conflict resolution
- Queue management for offline actions

#### 3.4 Analytics & Reporting
- App usage tracking
- Search analytics
- Navigation statistics
- User engagement metrics
- Admin activity reports

---

## Role-Based Feature Matrix

| Feature | Super Admin | Dean | Program Head | Basic Ed Head | Guest |
|---------|-------------|------|--------------|---------------|-------|
| **MAP MANAGEMENT** |
| Manage Facilities | ✓ | ✗ | ✗ | ✗ | ✗ |
| Manage All Rooms | ✓ | ✗ | ✗ | ✗ | ✗ |
| Manage Own Dept Rooms | ✓ | ✗ | ✓ | ✓ | ✗ |
| Navigation Graph | ✓ | ✗ | ✗ | ✗ | ✗ |
| FAQ/Chatbot | ✓ | ✗ | ✗ | ✗ | ✗ |
| QR Codes | ✓ | ✗ | ✗ | ✗ | ✗ |
| **COMMUNICATIONS** |
| Post Campus Announcement | ✓ | *(needs approval)* | *(needs approval)* | *(needs approval)* | ✗ |
| Post Dept Announcement | ✓ | ✓ | ✗ | ✗ | ✗ |
| Approve Announcements | ✓ | ✗ | ✗ | ✗ | ✗ |
| Send Notifications | ✓ | ✗ | ✗ | ✗ | ✗ |
| **ADMINISTRATION** |
| Manage Admin Accounts | ✓ | ✗ | ✗ | ✗ | ✗ |
| View All Feedback | ✓ | ✗ | ✗ | ✗ | ✗ |
| View Dept Feedback | ✓ | ✓ | ✗ | ✗ | ✗ |
| View Audit Log | ✓ | ✗ | ✗ | ✗ | ✗ |
| **MOBILE FEATURES** |
| View Map | ✓ | ✓ | ✓ | ✓ | ✓ |
| Search/Navigate | ✓ | ✓ | ✓ | ✓ | ✓ |
| Chatbot | ✓ | ✓ | ✓ | ✓ | ✓ |
| View Notifications | ✓ | ✓ | ✓ | ✓ | ✓ |
| Submit Feedback | ✓ | ✓ | ✓ | ✓ | ✓ |

---

*Document Version: 1.0*
*Generated from TechnoPath V4 Codebase Analysis*
