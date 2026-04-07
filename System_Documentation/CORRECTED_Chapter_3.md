# CHAPTER 3 - CORRECTED VERSION
## RESEARCH METHODOLOGY AND DESIGN

---

This chapter presents the research methodology, development environment, software engineering model, system development phases, project timeline, functional decomposition, use case analysis, storyboard design, database design, entity relationship diagram, and data dictionary employed in the development of TechnoPath: SEAIT Guide Map and Navigation System.

---

### Environment

TechnoPath: SEAIT Guide Map and Navigation System was developed and implemented at South East Asian Institute of Technology, Inc. (SEAIT), Barangay Crossing Rubber, National Highway, Tupi, South Cotabato 9505, Philippines. The study was conducted within the SEAIT campus premises, covering the RST, MST, and JST buildings, the Basic Education building, the gymnasium, canteens, playground, and other campus facilities and grounds.

System development and testing took place during the Second Semester of Academic Year 2025–2026, with the campus environment serving as both the development context and the deployment location for the Progressive Web Application.

---

### CORRECTED Software Engineering Methodology

The development of TechnoPath: SEAIT Guide Map and Navigation System adheres to the **Agile Software Development Life Cycle (SDLC) using the Scrum framework**.

The Agile methodology was selected because the study requires iterative development, continuous stakeholder feedback, and the flexibility to accommodate requirement changes and panel corrections throughout the development cycle. Stakeholders involved in the iterative review process include the panel of evaluators, the Safety and Security Office, College Deans, Program Heads, and representative end-users.

The Scrum framework organizes the development process into time-boxed iterations called **Sprints**, each lasting two to three weeks, during which a defined set of features is planned, designed, implemented, tested, and reviewed before proceeding to the next Sprint.

#### CORRECTED Technology Stack

**Frontend Development:**
- **Vue.js 3** with Composition API - Progressive JavaScript framework
- **Vue Router 4** - Client-side routing
- **Pinia** - State management
- **Axios** - HTTP client for API communication
- **Leaflet** - Interactive mapping library
- **IndexedDB** via localForage - Client-side storage for offline support
- **Vite** - Build tool and development server

**Backend Development:**
- **Django 4.2+** - Python web framework
- **Django REST Framework** - REST API toolkit
- **Django ORM** - Object-relational mapping
- **Django CORS Headers** - Cross-origin resource sharing
- **Simple JWT** - JSON Web Token authentication
- **WhiteNoise** - Static file serving

**Database Systems:**
- **PostgreSQL 14+** - Primary production database
- **SQLite 3** - Development and testing database
- **IndexedDB** - Browser-based offline storage

**AI Chatbot Service:**
- **Python Flask** (optional microservice) - AI API integration backend
- **External AI API** - Online conversational AI service
- **Local FAQ Database** - SQLite-based offline fallback

**Development Tools:**
- **Visual Studio Code** - Code editor
- **Git** - Version control
- **Node.js & npm** - Frontend package management
- **Python pip** - Backend package management
- **Chrome DevTools** - Debugging and testing

---

### System Development Phases

The development of TechnoPath: SEAIT Guide Map and Navigation System is organized into four Sprints, each containing the standard Agile phases of Planning, Analysis, Design, Implementation, Testing, and Review.

#### Sprint 1 — Core Foundation and Campus Map (Weeks 1–3)

**Phase 1: Planning**
The researchers define the project scope, identify the cited problems, establish the system requirements, and create the product backlog. The Sprint 1 backlog prioritizes the core campus map display, building floor maps, room labeling features, and the Vue.js frontend foundation.

**Phase 2: Analysis**
The researchers analyze the campus layout of SEAIT, gather floor plan data for the RST, MST, JST, and Basic Education buildings, identify all rooms, offices, and facilities to be included in the digital map, and define the data structure for storing room coordinates, building information, and navigation paths in PostgreSQL/SQLite.

**Phase 3: Design**
The researchers design the Vue.js component architecture, create the database schema for facilities, rooms, and navigation nodes using Django ORM, design the REST API endpoints, and create user interface wireframes for the home screen, map display, and room directory.

**Phase 4: Implementation**
The researchers develop the Vue.js application shell with routing and state management, implement the interactive 2D campus map display using SVG and Leaflet, build the Django backend with initial database models, implement the building floor map viewer with labeled rooms and highlighted offices, and set up the Django REST Framework API.

**Phase 5: Testing**
The researchers conduct unit testing on map rendering, room data retrieval, and floor-switching functionality, test the REST API endpoints, and perform initial usability testing with sample users.

**Phase 6: Review**
The researchers present the Sprint 1 increment to the thesis adviser and panel evaluators, gather feedback on map accuracy, room labeling, and interface design, and document corrections for the next Sprint.

#### Sprint 2 — Navigation Engine and QR Code Access (Weeks 4–6)

**Phase 1: Planning**
The researchers define the Sprint 2 backlog, prioritizing campus navigation route computation using Dijkstra's algorithm, visual route overlay on the map, the QR code access point feature, and the IndexedDB offline storage system.

**Phase 2: Analysis**
The researchers analyze the pathway connections between buildings, rooms, and campus areas; define the navigation graph (nodes and edges) with distance weights; determine the QR code content and deep linking workflow; and define the offline data synchronization requirements.

**Phase 3: Design**
The researchers design the navigation route overlay interface, the step-by-step direction display panel, the QR code generation and scanning workflow, the IndexedDB schema for offline storage, and the background sync mechanism.

**Phase 4: Implementation**
The researchers implement Dijkstra's shortest-path algorithm in JavaScript for offline route computation, develop the navigation route overlay on the 2D map, build the QR code access point feature with deep linking, implement IndexedDB storage using localForage, and create the background sync service worker.

**Phase 5: Testing**
The researchers conduct unit testing on the pathfinding algorithm, validate route accuracy across multiple origin-destination pairs, test the QR code scanning workflow, test offline mode functionality, and perform integration testing between the navigation engine and map display.

**Phase 6: Review**
The researchers present the Sprint 2 increment, gather feedback on navigation accuracy, QR code usability, and offline functionality.

#### Sprint 3 — Administrative Backend and Room Updates (Weeks 7–9)

**Phase 1: Planning**
The researchers define the Sprint 3 backlog, prioritizing the role-based administrative backend with four-tier hierarchy (Super Admin, Dean, Program Head, Basic Ed Head), the announcement approval workflow, and admin authentication.

**Phase 2: Analysis**
The researchers analyze the administrative workflow for the Safety and Security Office, College Deans, Program Heads, and Basic Ed Head; define role-based access permissions including the approval workflow for campus-wide announcements; and determine the CRUD operations with audit logging.

**Phase 3: Design**
The researchers design the admin authentication with JWT, the role-based access control system, the admin dashboard with statistics, CRUD management screens for facilities and rooms, the announcement approval workflow, and the admin audit log interface.

**Phase 4: Implementation**
The researchers develop the Django authentication module with JWT, implement the custom AdminUser model with role hierarchy, build CRUD operations with soft delete functionality, implement the role-based access control decorators, build the announcement approval workflow, and implement the comprehensive admin audit log.

**Phase 5: Testing**
The researchers conduct unit testing on the authentication module, validate CRUD operations for data integrity, test role-based access restrictions, test the approval workflow, and perform security testing on the admin system.

**Phase 6: Review**
The researchers present the Sprint 3 increment, gather feedback on the administrative workflow, approval process, and access control logic.

#### Sprint 4 — AI Chatbot, Notifications, and Deployment (Weeks 10–12)

**Phase 1: Planning**
The researchers define the Sprint 4 backlog, prioritizing the AI chatbot/virtual guide with dual-mode operation (online/offline), the notification system, the feedback and ratings module, and final deployment preparation.

**Phase 2: Analysis**
The researchers analyze the AI chatbot requirements for both online (API) and offline (FAQ) modes, define the FAQ database schema for keyword matching, determine the connectivity detection logic, and identify final UI improvements.

**Phase 3: Design**
The researchers design the AI chatbot conversational interface with mode indicators, the offline FAQ keyword matching logic, the notification bell and alert system with department scoping, the feedback submission form, and final UI refinements.

**Phase 4: Implementation**
The researchers develop the AI chatbot module with online mode (Axios to Python backend with AI API) and offline fallback mode (local FAQ keyword matching), implement the connectivity detection, build the notification system with department filtering, implement the anonymous feedback and ratings module, create the search analytics tracking, and apply final UI polish.

**Phase 5: Testing**
The researchers conduct comprehensive system testing, perform User Acceptance Testing (UAT) with sample students, faculty, and visitors, validate AI chatbot response accuracy in both modes, test notification delivery, and conduct performance testing.

**Phase 6: Review**
The researchers present the final system to the thesis adviser and panel evaluators, conduct the final defense presentation, gather evaluation scores, and prepare the system for institutional deployment.

---

### CORRECTED Functional Decomposition Diagram (FDD)

The Functional Decomposition Diagram (FDD) illustrates the main features and sub-functions of TechnoPath: SEAIT Guide Map and Navigation System, organized hierarchically from the system level down to individual functional components.

The system is decomposed into **three primary functional modules**:

#### Module 1: Mobile User Module
Provides all public-facing navigation and information features for Guest Users (Students, Faculty, Visitors).

**1.1 Campus Map View**
- Interactive SEAIT campus ground layout map
- SVG-based building floor maps with floor switching
- Facility and room markers with pop-up information
- Zoom, pan, and rotate controls
- QR code deep linking support
- GPS location display (where available)

**1.2 Search & Discovery**
- Real-time search with autocomplete
- Recent searches history
- Facility and room filtering
- Search result highlighting on map
- Popular/trending searches

**1.3 Navigation System**
- Point-to-point route computation using Dijkstra's Algorithm
- Visual route overlay on map
- Turn-by-step direction panel
- Distance and estimated walking time
- Route sharing capability

**1.4 AI Chatbot / Virtual Guide**
- Natural language query processing
- Online mode: AI API integration for conversational responses
- Offline mode: Local FAQ database with keyword matching
- Connectivity auto-detection and mode switching
- Quick action suggestions
- Chat history

**1.5 Notifications System**
- In-app notification bell
- Department-scoped announcements
- Priority-based alerts (Normal, Important, Urgent, Emergency)
- Read/unread status tracking
- Push notification support (where available)

**1.6 Information Center**
- Building information display
- Room details with capacity and type
- Office hours and contact information
- Instructor/Employee directory
- Facility images

**1.7 User Engagement**
- Favorites (saved locations)
- Star ratings for facilities and rooms
- Anonymous feedback submission
- User profile and preferences
- Accessibility settings (dark mode, font scaling)

#### Module 2: Admin Panel Module
Provides role-based administrative functions for managing campus data and system configuration.

**2.1 Admin Dashboard**
- System statistics (total facilities, rooms, users)
- Quick action buttons
- Pending approvals counter
- Recent activity feed
- Popular searches analytics

**2.2 Map Management**
- **Facilities Management**: Add, edit, delete facilities with soft delete
- **Rooms Management**: CRUD operations for rooms with facility linkage
- **Navigation Graph**: Node and edge management for pathfinding
- **Map Markers**: Interactive marker placement and configuration
- **Map Labels**: Text label positioning and styling
- **FAQ/Chatbot Management**: Knowledge base CRUD operations
- **QR Code Management**: Deep link QR generation

**2.3 Communications**
- **Announcements**: Create and manage announcements
  - Department-scoped (direct publish for Dean/Heads)
  - Campus-wide (requires Super Admin approval)
- **Pending Approvals**: Review and approve/reject announcement requests
- **Send Notifications**: Create and send system notifications to users

**2.4 Administration**
- **Admin Accounts**: User management with role assignment (Super Admin only)
  - Role: Super Admin, Dean, Program Head, Basic Ed Head
  - Department assignment
  - Account activation/deactivation
- **Feedback & Ratings**: View and moderate user feedback
  - All feedback (Super Admin)
  - Department feedback only (Dean)
- **Audit Log**: Complete activity tracking with filtering
  - All actions (Super Admin)
  - Department actions only (Dean)

#### Module 3: System Core Module
Provides the underlying technical infrastructure and services.

**3.1 Database Management**
- PostgreSQL primary database (production)
- SQLite development database
- Django ORM models and migrations
- Database backup and recovery

**3.2 API Services (REST)**
- Django REST Framework endpoints
- JWT authentication middleware
- CORS handling
- API rate limiting
- Request/response serialization

**3.3 Sync & Offline Services**
- IndexedDB local storage
- Background synchronization
- Service Worker for PWA functionality
- Offline/online state detection
- Conflict resolution

**3.4 Analytics & Reporting**
- Search history tracking
- App usage statistics
- User event analytics
- Popular routes analysis
- Feedback sentiment tracking

---

### CORRECTED Use Case Matrix

The Use Case Matrix identifies the primary and secondary actors of TechnoPath: SEAIT Guide Map and Navigation System and maps each actor to the system functions they interact with.

#### Actor Hierarchy with Generalization

```
                    ┌─────────────────┐
                    │   AdminUser     │
                    │   (Abstract)    │
                    └────────┬────────┘
                             │ <<general>>
        ┌────────────────────┼────────────────────┐
        │                    │                    │
   ┌────▼────┐          ┌────▼────┐          ┌────▼────┐
   │Super    │          │  Dean   │          │Program  │
   │Admin    │          │         │          │Head     │
   └────┬────┘          └────┬────┘          └────┬────┘
                             │                    │
                        ┌────▼────┐               │
                        │Basic Ed │               │
                        │Head     │◄──────────────┘
                        └─────────┘   <<general>>

┌─────────────────┐
│   Guest User    │
│(Students,       │
│Visitors, Faculty)│
└─────────────────┘
```

#### Primary Actor: Guest User

**Description:** Consolidated category encompassing SEAIT students (freshmen, transferees, regular), faculty members, and external visitors who use the system for campus navigation without administrative privileges.

**System Functions:**
- Scan QR code at main gate to access system
- View interactive campus ground layout map
- View building floor maps with labeled rooms
- Search for rooms, facilities, and offices
- Navigate to destinations with visual route display
- Use AI chatbot for location queries (online and offline modes)
- Submit anonymous feedback and ratings
- View in-app notifications
- Save favorite locations
- View building, room, and directory information

#### Secondary Actors (Administrative)

##### Actor: Super Admin (Safety and Security Office)

**Description:** The highest administrative authority responsible for campus safety, structural building information management, and system-wide oversight.

**System Functions:**
- Log in to admin panel with JWT authentication
- Manage all facilities across all departments (CRUD with soft delete)
- Manage all rooms across all departments
- Manage navigation graph (nodes and edges)
- Manage map markers and labels
- Manage FAQ/Chatbot knowledge base
- Generate and manage QR code access points
- Post campus-wide announcements (direct publish)
- **Approve or reject** campus-wide announcement requests from Dean/Heads
- Send system notifications to all users
- Manage admin accounts (create, assign roles, deactivate)
- View **all** feedback and ratings system-wide
- View complete audit log with all administrative actions
- View system dashboard and analytics reports

##### Actor: Dean (College Dean)

**Description:** College-level oversight authority with department-specific management rights and the ability to publish department-scoped announcements directly while requiring approval for campus-wide announcements.

**Inherited from AdminUser:** Login, password management, dashboard access

**System Functions:**
- Log in to admin panel
- Manage own department's rooms and facilities (CRUD)
- **Post department-scoped announcements** (direct publish, no approval needed)
- **Request campus-wide announcement publication** (requires Super Admin approval)
- View own department's feedback and ratings
- View audit log **filtered to own department only**
- View department-level dashboard and reports
- Access all Guest User functions

##### Actor: Program Head (College Program Head)

**Description:** Academic department head managing department-specific classroom assignments and announcements.

**Inherited from AdminUser:** Login, password management, dashboard access

**System Functions:**
- Log in to admin panel
- Manage own department's rooms and classroom assignments (CRUD)
- **Post department-scoped announcements** (direct publish)
- **Request campus-wide announcement publication** (requires Super Admin approval)
- View own department's feedback and ratings
- View audit log **filtered to own department only**
- Access all Guest User functions

##### Actor: Basic Ed Head (Basic Education Head)

**Description:** Head of the Basic Education Department with the same permissions as Program Head for managing Basic Education department data.

**Inherited from AdminUser:** Login, password management, dashboard access

**System Functions:**
- Log in to admin panel
- Manage Basic Education department rooms and facilities (CRUD)
- **Post department-scoped announcements** for Basic Education (direct publish)
- **Request campus-wide announcement publication** (requires Super Admin approval)
- View Basic Education department's feedback and ratings
- View audit log **filtered to Basic Education department only**
- Access all Guest User functions

#### Use Case Relationships

| Use Case | Relationship | Connected Use Case | Description |
|----------|-------------|-------------------|-------------|
| Navigate to Destination | <<include>> | View Campus Map | Navigation requires map display |
| Navigate to Destination | <<include>> | Search Location | Navigation requires search functionality |
| Post Campus Announcement | <<extend>> | Approve Announcement | Campus-wide requires approval for non-Super Admin |
| Post Dept Announcement | <<extend>> | Approve Announcement | Only campus-wide requires approval |

---

[Storyboard section remains similar with updated technology references...]

---

### CORRECTED Database Design

The database design of TechnoPath: SEAIT Guide Map and Navigation System employs a **dual-database architecture**:

- **PostgreSQL** serves as the **primary production database**, managed through Django ORM, providing robust data storage, complex queries, transaction support, and scalability for institutional deployment.
- **SQLite** serves as the **development and testing database** and for lightweight deployments.
- **IndexedDB** serves as the **client-side offline storage** in the browser for PWA functionality.

The database stores all campus navigation data, room and facility information, FAQ entries, feedback records, administrative user accounts, notifications, and system configuration to support both online and offline-first operation.

#### Database Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    TECHNOPATH DATABASES                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────┐    ┌─────────────────────────────┐ │
│  │   PostgreSQL        │    │   IndexedDB (Browser)       │ │
│  │   (Production)      │    │   (Offline Cache)           │ │
│  │                     │◄──►│                             │ │
│  │  • 25+ tables        │    │  • Campus map data          │ │
│  │  • Django ORM        │    │  • FAQ entries              │ │
│  │  • Full ACID         │    │  • User favorites           │ │
│  │  • Scalable          │    │  • Notification cache       │ │
│  └─────────────────────┘    └─────────────────────────────┘ │
│           ▲                                                 │
│           │ Development                                      │
│           ▼                                                 │
│  ┌─────────────────────┐                                    │
│  │   SQLite            │                                    │
│  │   (Development)     │                                    │
│  └─────────────────────┘                                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

The database consists of **25+ tables** organized into the following functional groups:

**1. Core Entity Tables:**
- `admin_users` - Administrative user accounts with role-based access control (Super Admin, Dean, Program Head, Basic Ed Head)
- `departments` - Department registry with head user assignment
- `facilities` - Campus buildings and facilities with department linkage
- `rooms` - Rooms and spaces within facilities with floor, coordinates, and type

**2. Navigation Tables:**
- `navigation_nodes` - Navigable points (rooms, corridors, entrances, staircases) with X/Y coordinates
- `navigation_edges` - Pathway connections between nodes with distance weights for Dijkstra's Algorithm

**3. Map Visualization Tables:**
- `map_markers` - Interactive facility and room markers with position, icon, and color
- `map_labels` - Text annotations on map with positioning and styling

**4. Communication Tables:**
- `announcements` - Department and campus-wide announcements with approval workflow (pending, published, rejected, archived)
- `notifications` - Mobile push notifications with department scoping and priority levels
- `notification_read_status` - Tracks which users have read which notifications
- `notification_types` - Notification type definitions
- `notification_preferences` - User notification settings

**5. Chatbot System Tables:**
- `faq_entries` - FAQ knowledge base for offline chatbot mode with keyword matching
- `ai_chat_logs` - Chat interaction history with mode tracking (online/offline)

**6. Feedback System Tables:**
- `feedback` - Anonymous user feedback submissions with category and flagging
- `ratings` - Star ratings for facilities, rooms, and app experience
- `feedback_flags` - Content moderation flags for ratings

**7. Audit & Analytics Tables:**
- `admin_audit_log` - Complete audit trail of all administrative actions with before/after JSON snapshots
- `search_history` - Search query analytics for popular destinations
- `app_usage` - Daily session usage tracking
- `usage_analytics` - User event tracking for system improvement

**8. System Configuration Tables:**
- `device_preferences` - User device settings (dark mode, language, accessibility)
- `app_config` - System-wide configuration key-value store
- `connectivity_log` - Network status tracking for diagnostics

---

### CORRECTED Entity Relationship Diagram

The Entity Relationship Diagram (ERD) illustrates the data entities and their relationships within the TechnoPath: SEAIT Guide Map and Navigation System database.

#### Key Relationships

| Relationship | Type | Description |
|-------------|------|-------------|
| **departments** → **admin_users** (head_user_id) | Many-to-One (N:1) | A department has one head user; a user can head multiple departments |
| **departments** → **facilities** | One-to-Many (1:N) | A department contains multiple facilities |
| **facilities** → **rooms** | One-to-Many (1:N) | A facility contains multiple rooms |
| **facilities** → **map_markers** | One-to-Many (1:N) | A facility can have multiple map markers |
| **rooms** → **map_markers** | One-to-Many (1:N) | A room can have multiple map markers |
| **facilities** → **navigation_nodes** | One-to-Many (1:N) | A facility maps to multiple navigation nodes |
| **rooms** → **navigation_nodes** | One-to-Many (1:N) | A room maps to multiple navigation nodes |
| **navigation_nodes** → **navigation_edges** (from_node) | One-to-Many (1:N) | A node has multiple outgoing edges |
| **navigation_nodes** → **navigation_edges** (to_node) | One-to-Many (1:N) | A node has multiple incoming edges |
| **facilities** → **feedback** | One-to-Many (1:N) | A facility receives multiple feedback entries |
| **rooms** → **feedback** | One-to-Many (1:N) | A room receives multiple feedback entries |
| **facilities** → **ratings** | One-to-Many (1:N) | A facility receives multiple ratings |
| **rooms** → **ratings** | One-to-Many (1:N) | A room receives multiple ratings |
| **ratings** → **feedback_flags** | One-to-Many (1:N) | A rating can have multiple moderation flags |
| **admin_users** → **announcements** (created_by) | One-to-Many (1:N) | A user creates multiple announcements |
| **admin_users** → **announcements** (approved_by) | One-to-Many (1:N) | A user approves multiple announcements |
| **announcements** → **notifications** | One-to-One (1:1) | A published announcement generates one notification |
| **notifications** → **notification_read_status** | One-to-Many (1:N) | A notification has multiple read statuses |
| **admin_users** → **notification_read_status** | One-to-Many (1:N) | A user has multiple notification read records |
| **faq_entries** → **ai_chat_logs** | One-to-Many (1:N) | A FAQ entry can be matched in multiple chat logs |
| **admin_users** → **admin_audit_log** | One-to-Many (1:N) | A user performs multiple audited actions |
| **admin_users** → **search_history** | One-to-Many (1:N) | A user has multiple search records |

---

### CORRECTED Data Dictionary

[Full data dictionary with all 25+ tables matching the actual database schema would follow here, using the Data_Dictionary.md content as reference]

---

*CHAPTER 3 - CORRECTED VERSION*
*Match actual TechnoPath V4 System Implementation*
*Technology Stack: Vue.js + Django + PostgreSQL + IndexedDB*
