# TechnoPath: SEAIT Guide Map and Navigation System - Data Dictionary

## Table of Contents
1. [Core Entities](#1-core-entities)
2. [Navigation System](#2-navigation-system)
3. [Map Visualization](#3-map-visualization)
4. [Communication System](#4-communication-system)
5. [Chatbot System](#5-chatbot-system)
6. [Feedback System](#6-feedback-system)
7. [Audit & Analytics](#7-audit--analytics)
8. [System Configuration](#8-system-configuration)
9. [Enumeration Values](#9-enumeration-values)

---

## Overview

This data dictionary documents all tables, columns, data types, constraints, and relationships for the TechnoPath SEAIT Campus Guide system.

**Database Systems:**
- **Main Database**: PostgreSQL (Production) / SQLite (Development) - Django Backend
- **Chatbot Database**: SQLite - Flask Service
- **ORM**: Django ORM 4.2+
- **Total Tables**: 25+

---

## Core Tables

### 1. admin_users
**Purpose**: Stores administrator accounts with role-based access control

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique identifier |
| username | VARCHAR(150) | UNIQUE, NOT NULL | Login username |
| email | VARCHAR(254) | NULL | Email address |
| display_name | VARCHAR(200) | NULL | Full name or title |
| password | VARCHAR(128) | NOT NULL | Hashed password |
| role | VARCHAR(20) | NOT NULL, DEFAULT 'program_head' | User role (super_admin, dean, program_head, basic_ed_head) |
| department | VARCHAR(50) | NULL | Department code |
| department_label | VARCHAR(200) | NULL | Override label for announcements |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | Account active status |
| is_staff | BOOLEAN | NOT NULL, DEFAULT FALSE | Django admin access |
| is_superuser | BOOLEAN | NOT NULL, DEFAULT FALSE | Superuser privileges |
| login_attempts | INTEGER | NOT NULL, DEFAULT 0 | Failed login count |
| locked_until | DATETIME | NULL | Account lockout expiry |
| last_login | DATETIME | NULL | Last successful login |
| created_at | DATETIME | NOT NULL, AUTO | Account creation timestamp |
| updated_at | DATETIME | NOT NULL, AUTO | Last update timestamp |

**Indexes**: username (unique)

---

### 2. departments
**Purpose**: Organization units within SEAIT

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique identifier |
| name | VARCHAR(200) | NOT NULL | Department name |
| code | VARCHAR(20) | UNIQUE, NOT NULL | Department code |
| description | TEXT | NULL | Department description |
| head_user_id | INTEGER | FK → admin_users.id, NULL | Department head |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | Active status |
| created_at | DATETIME | NOT NULL, AUTO | Creation timestamp |

**Indexes**: code (unique), head_user_id

---

## Campus Data Tables

### 3. facilities
**Purpose**: Campus buildings and structures

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique identifier |
| name | VARCHAR(200) | NOT NULL | Building name |
| code | VARCHAR(20) | UNIQUE, NOT NULL | Building code (e.g., RST, MST, JST) |
| description | TEXT | NULL | Building description |
| building_code | VARCHAR(20) | NULL | Alternative code |
| department_id | INTEGER | FK → departments.id, NULL | Owning department |
| latitude | FLOAT | NULL | GPS latitude |
| longitude | FLOAT | NULL | GPS longitude |
| image_path | VARCHAR(500) | NULL | Building image URL |
| map_svg_id | VARCHAR(100) | NULL | SVG element ID (e.g., building-RST) |
| total_floors | INTEGER | NOT NULL, DEFAULT 1 | Number of floors |
| is_deleted | BOOLEAN | NOT NULL, DEFAULT FALSE | Soft delete flag |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | Active status |
| created_at | DATETIME | NOT NULL, AUTO | Creation timestamp |
| updated_at | DATETIME | NOT NULL, AUTO | Update timestamp |

**Indexes**: code (unique), department_id

---

### 4. rooms
**Purpose**: Rooms, classrooms, offices within facilities

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique identifier |
| facility_id | INTEGER | FK → facilities.id, NOT NULL | Parent building |
| name | VARCHAR(200) | NOT NULL | Room name |
| code | VARCHAR(50) | NOT NULL | Room code |
| room_number | VARCHAR(50) | NULL | Room number |
| description | TEXT | NULL | Room description |
| floor | INTEGER | NOT NULL, DEFAULT 1 | Floor number (1-4) |
| map_svg_id | VARCHAR(100) | NULL | SVG element ID (e.g., RST-F1-CL1) |
| room_type | VARCHAR(50) | NOT NULL, DEFAULT 'classroom' | Type: classroom, office, lab, facility, staircase, restroom, other |
| capacity | INTEGER | NOT NULL, DEFAULT 30 | Seating capacity |
| is_office | BOOLEAN | NOT NULL, DEFAULT FALSE | Is an office |
| is_crucial | BOOLEAN | NOT NULL, DEFAULT FALSE | Critical facility room |
| search_count | INTEGER | NOT NULL, DEFAULT 0 | Search frequency counter |
| is_deleted | BOOLEAN | NOT NULL, DEFAULT FALSE | Soft delete flag |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | Active status |
| created_at | DATETIME | NOT NULL, AUTO | Creation timestamp |
| updated_at | DATETIME | NOT NULL, AUTO | Update timestamp |

**Indexes**: facility_id, code

---

### 5. map_markers
**Purpose**: Visual markers on the interactive map

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique identifier |
| facility_id | INTEGER | FK → facilities.id, NULL | Associated facility |
| room_id | INTEGER | FK → rooms.id, NULL | Associated room |
| name | VARCHAR(200) | NOT NULL | Marker label |
| x_position | FLOAT | NOT NULL | X coordinate (0-1) |
| y_position | FLOAT | NOT NULL | Y coordinate (0-1) |
| marker_type | VARCHAR(20) | NOT NULL, DEFAULT 'facility' | Type: facility, room, entrance, waypoint, amenity |
| icon_name | VARCHAR(100) | NOT NULL, DEFAULT 'location_on' | Material icon name |
| color_hex | VARCHAR(7) | NOT NULL, DEFAULT '#FF9800' | Marker color (orange) |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | Active status |
| created_at | DATETIME | NOT NULL, AUTO | Creation timestamp |

**Indexes**: facility_id, room_id

---

### 6. map_labels
**Purpose**: Text labels on the campus map

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique identifier |
| label_text | VARCHAR(200) | NOT NULL | Text content |
| x_position | FLOAT | NOT NULL | X coordinate |
| y_position | FLOAT | NOT NULL | Y coordinate |
| font_size | INTEGER | NOT NULL, DEFAULT 14 | Font size in pixels |
| color_hex | VARCHAR(7) | NOT NULL, DEFAULT '#000000' | Text color (black) |
| rotation | FLOAT | NOT NULL, DEFAULT 0 | Rotation angle in degrees |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | Active status |
| created_at | DATETIME | NOT NULL, AUTO | Creation timestamp |

---

## Navigation Tables

### 7. navigation_nodes
**Purpose**: Waypoints for pathfinding algorithm

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique identifier |
| name | VARCHAR(200) | NOT NULL | Node name |
| node_type | VARCHAR(20) | NOT NULL | Type: room, facility, waypoint, entrance, staircase, elevator, junction |
| facility_id | INTEGER | FK → facilities.id, NULL | Associated facility |
| room_id | INTEGER | FK → rooms.id, NULL | Associated room |
| map_svg_id | VARCHAR(100) | NULL | SVG element reference |
| x | FLOAT | NOT NULL | X coordinate |
| y | FLOAT | NOT NULL | Y coordinate |
| floor | INTEGER | NOT NULL, DEFAULT 1 | Floor level |
| is_deleted | BOOLEAN | NOT NULL, DEFAULT FALSE | Soft delete flag |
| created_at | DATETIME | NOT NULL, AUTO | Creation timestamp |
| updated_at | DATETIME | NOT NULL, AUTO | Update timestamp |

**Indexes**: facility_id, room_id

---

### 8. navigation_edges
**Purpose**: Connections between navigation nodes (graph edges)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique identifier |
| from_node_id | INTEGER | FK → navigation_nodes.id, NOT NULL | Source node |
| to_node_id | INTEGER | FK → navigation_nodes.id, NOT NULL | Destination node |
| distance | INTEGER | NOT NULL | Distance in meters/units |
| is_bidirectional | BOOLEAN | NOT NULL, DEFAULT TRUE | Two-way connection |
| is_deleted | BOOLEAN | NOT NULL, DEFAULT FALSE | Soft delete flag |
| created_at | DATETIME | NOT NULL, AUTO | Creation timestamp |
| updated_at | DATETIME | NOT NULL, AUTO | Update timestamp |

**Indexes**: from_node_id, to_node_id

---

## Communication Tables

### 9. announcements
**Purpose**: Department announcements with approval workflow

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique identifier |
| title | VARCHAR(200) | NOT NULL | Announcement title |
| content | TEXT | NOT NULL | Announcement body |
| created_by_id | INTEGER | FK → admin_users.id, NULL | Author |
| source_label | VARCHAR(200) | NOT NULL | Department label for display |
| source_color | VARCHAR(20) | NOT NULL, DEFAULT 'orange' | Color code for mobile |
| scope | VARCHAR(20) | NOT NULL, DEFAULT 'campus_wide' | Target audience: campus_wide, all_college, basic_ed_only, department |
| target_department | VARCHAR(50) | NULL | Specific department (when scope=department) |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'pending_approval' | Status: pending_approval, published, rejected, archived |
| requires_approval | BOOLEAN | NOT NULL, DEFAULT TRUE | Needs approval flag |
| approved_by_id | INTEGER | FK → admin_users.id, NULL | Approver |
| rejected_by_id | INTEGER | FK → admin_users.id, NULL | Rejector |
| rejection_note | TEXT | NULL | Rejection reason |
| approved_at | DATETIME | NULL | Approval timestamp |
| archived_by_id | INTEGER | FK → admin_users.id, NULL | Archiver |
| archived_at | DATETIME | NULL | Archive timestamp |
| is_deleted | BOOLEAN | NOT NULL, DEFAULT FALSE | Soft delete flag |
| created_at | DATETIME | NOT NULL, AUTO | Creation timestamp |
| updated_at | DATETIME | NOT NULL, AUTO | Update timestamp |

**Indexes**: created_by_id, approved_by_id, rejected_by_id, archived_by_id, status

---

### 10. notifications
**Purpose**: Push notifications to mobile users

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique identifier |
| title | VARCHAR(200) | NOT NULL | Notification title |
| message | TEXT | NOT NULL | Notification body |
| type | VARCHAR(30) | NOT NULL, DEFAULT 'info' | Type: announcement, info, emergency, facility_update, room_update, system_maintenance, app_update |
| source_label | VARCHAR(200) | NULL | Department source label |
| source_color | VARCHAR(20) | NOT NULL, DEFAULT 'orange' | Color code |
| announcement_id | INTEGER | FK → announcements.id, NULL | Linked announcement |
| priority | INTEGER | NOT NULL, DEFAULT 1 | Priority: 1=Normal, 2=Important, 3=Urgent, 4=Emergency |
| is_read | BOOLEAN | NOT NULL, DEFAULT FALSE | Read status |
| expires_at | DATETIME | NULL | Expiration timestamp |
| created_by_id | INTEGER | FK → admin_users.id, NULL | Sender |
| created_at | DATETIME | NOT NULL, AUTO | Creation timestamp |

**Indexes**: announcement_id, created_by_id, type, is_read

---

### 11. faq_entries
**Purpose**: Chatbot knowledge base entries

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique identifier |
| question | TEXT | NOT NULL | FAQ question |
| answer | TEXT | NOT NULL | FAQ answer |
| category | VARCHAR(50) | NOT NULL, DEFAULT 'general' | Category: location, schedule, academic, services, general |
| keywords | TEXT | NOT NULL, DEFAULT '' | Comma-separated search keywords |
| usage_count | INTEGER | NOT NULL, DEFAULT 0 | Usage frequency |
| is_deleted | BOOLEAN | NOT NULL, DEFAULT FALSE | Soft delete flag |
| created_at | DATETIME | NOT NULL, AUTO | Creation timestamp |
| updated_at | DATETIME | NOT NULL, AUTO | Update timestamp |

**Indexes**: category

---

### 12. ai_chat_logs
**Purpose**: Chatbot conversation history

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique identifier |
| user_query | TEXT | NOT NULL | User message |
| ai_response | TEXT | NULL | Bot reply |
| mode | VARCHAR(10) | NOT NULL | Mode: online, offline |
| response_time_ms | INTEGER | NULL | Response time in milliseconds |
| is_successful | BOOLEAN | NOT NULL, DEFAULT TRUE | Success flag |
| error_message | TEXT | NULL | Error details if failed |
| faq_entry_id | INTEGER | FK → faq_entries.id, NULL | Matched FAQ entry |
| session_id | VARCHAR(100) | NULL | User session identifier |
| created_at | DATETIME | NOT NULL, AUTO | Creation timestamp |

**Indexes**: faq_entry_id, session_id, created_at

---

### 13. ratings
**Purpose**: User ratings for facilities and rooms

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique identifier |
| user_id | INTEGER | FK → admin_users.id, NULL | Rater (optional) |
| facility_id | INTEGER | FK → facilities.id, NULL | Rated facility |
| room_id | INTEGER | FK → rooms.id, NULL | Rated room |
| rating | INTEGER | NOT NULL | Rating value 1-5 |
| comment | TEXT | NULL | Optional comment |
| category | VARCHAR(20) | NOT NULL, DEFAULT 'general' | Category: general, facility, room, navigation, app |
| is_anonymous | BOOLEAN | NOT NULL, DEFAULT TRUE | Anonymous flag |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | Active status |
| created_at | DATETIME | NOT NULL, AUTO | Creation timestamp |

**Indexes**: user_id, facility_id, room_id, category

---

### 14. feedback
**Purpose**: User feedback submissions

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique identifier |
| rating | INTEGER | NULL | Rating 1-5 |
| comment | TEXT | NULL | Feedback text |
| category | VARCHAR(30) | NOT NULL, DEFAULT 'general' | Category: map_accuracy, ai_chatbot, navigation, general, bug_report, facility, room |
| facility_id | INTEGER | FK → facilities.id, NULL | Related facility |
| room_id | INTEGER | FK → rooms.id, NULL | Related room |
| is_flagged | BOOLEAN | NOT NULL, DEFAULT FALSE | Flagged for review |
| flag_reason | TEXT | NULL | Flag reason |
| created_at | DATETIME | NOT NULL, AUTO | Creation timestamp |

**Indexes**: facility_id, room_id, category, is_flagged

---

### 15. feedback_flags
**Purpose**: Flagged feedback for admin review

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique identifier |
| user_id | INTEGER | FK → admin_users.id, NULL | User who flagged |
| rating_id | INTEGER | FK → ratings.id, NOT NULL | Flagged rating |
| reason | TEXT | NOT NULL | Flag reason |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'pending' | Status: pending, reviewed, resolved, dismissed |
| resolved_by_id | INTEGER | FK → admin_users.id, NULL | Admin who resolved |
| resolved_at | DATETIME | NULL | Resolution timestamp |
| created_at | DATETIME | NOT NULL, AUTO | Creation timestamp |

**Indexes**: user_id, rating_id, resolved_by_id, status

---

## Analytics & Audit Tables

### 16. admin_audit_log
**Purpose**: Complete audit trail of admin actions

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique identifier |
| admin_id | INTEGER | FK → admin_users.id, NULL | Acting admin |
| action | VARCHAR(20) | NOT NULL | Action: login, logout, create, update, soft_delete, restore, approve, reject, publish, reset_password |
| entity_type | VARCHAR(50) | NULL | Affected entity type |
| entity_id | INTEGER | NULL | Affected entity ID |
| entity_label | VARCHAR(200) | NULL | Entity name/label |
| old_value_json | TEXT | NULL | Previous state (JSON) |
| new_value_json | TEXT | NULL | New state (JSON) |
| ip_address | VARCHAR(50) | NULL | Client IP address |
| created_at | DATETIME | NOT NULL, AUTO | Action timestamp |

**Indexes**: admin_id, action, entity_type, created_at

---

### 17. search_history
**Purpose**: Track user search queries

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique identifier |
| user_id | INTEGER | FK → admin_users.id, NULL | Searching user |
| query | VARCHAR(500) | NOT NULL | Search text |
| results_count | INTEGER | NOT NULL, DEFAULT 0 | Number of results |
| was_clicked | BOOLEAN | NOT NULL, DEFAULT FALSE | Result clicked flag |
| created_at | DATETIME | NOT NULL, AUTO | Search timestamp |

**Indexes**: user_id, query, created_at

---

### 18. app_usage
**Purpose**: Daily app usage statistics

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique identifier |
| user_id | INTEGER | FK → admin_users.id, NULL | User (NULL = anonymous) |
| session_date | DATE | NOT NULL | Date of session |
| session_duration | INTEGER | NOT NULL, DEFAULT 0 | Duration in seconds |
| screen_views | INTEGER | NOT NULL, DEFAULT 0 | Screen view count |
| created_at | DATETIME | NOT NULL, AUTO | Record timestamp |

**Indexes**: user_id, session_date

---

### 19. usage_analytics
**Purpose**: Detailed event tracking

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique identifier |
| user_id | INTEGER | FK → admin_users.id, NULL | User |
| event_type | VARCHAR(50) | NOT NULL | Type: screen_view, search, navigation, rating, feedback, share, notification_open |
| event_data | JSON | NULL | Additional event data |
| screen_name | VARCHAR(100) | NULL | Screen where event occurred |
| session_id | VARCHAR(100) | NULL | Session identifier |
| created_at | DATETIME | NOT NULL, AUTO | Event timestamp |

**Indexes**: user_id, event_type, screen_name, session_id, created_at

---

### 20. device_preferences
**Purpose**: Per-device user settings

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique identifier |
| user_id | INTEGER | FK → admin_users.id, NULL | User |
| device_id | VARCHAR(200) | NOT NULL | Device identifier |
| dark_mode | BOOLEAN | NOT NULL, DEFAULT FALSE | Dark theme enabled |
| language | VARCHAR(10) | NOT NULL, DEFAULT 'en' | Language code |
| font_scale | FLOAT | NOT NULL, DEFAULT 1.0 | Font size multiplier |
| high_contrast | BOOLEAN | NOT NULL, DEFAULT FALSE | High contrast mode |
| reduce_animations | BOOLEAN | NOT NULL, DEFAULT FALSE | Reduced motion |
| last_sync | DATETIME | NULL | Last sync timestamp |
| created_at | DATETIME | NOT NULL, AUTO | Creation timestamp |

**Indexes**: user_id, device_id

---

### 21. notification_types
**Purpose**: Configurable notification categories

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique identifier |
| name | VARCHAR(100) | UNIQUE, NOT NULL | Type name |
| description | TEXT | NULL | Type description |
| icon_name | VARCHAR(100) | NOT NULL, DEFAULT 'notifications' | Material icon |
| color_hex | VARCHAR(7) | NOT NULL, DEFAULT '#FF9800' | Type color |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | Active status |
| created_at | DATETIME | NOT NULL, AUTO | Creation timestamp |

**Indexes**: name (unique)

---

### 22. notification_preferences
**Purpose**: User notification settings per type

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique identifier |
| user_id | INTEGER | FK → admin_users.id, NOT NULL | User |
| notification_type_id | INTEGER | FK → notification_types.id, NOT NULL | Notification type |
| is_enabled | BOOLEAN | NOT NULL, DEFAULT TRUE | Enabled flag |
| created_at | DATETIME | NOT NULL, AUTO | Creation timestamp |

**Indexes**: user_id, notification_type_id (unique together)

---

### 23. app_config
**Purpose**: System configuration settings

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique identifier |
| config_key | VARCHAR(100) | UNIQUE, NOT NULL | Setting key |
| config_value | TEXT | NOT NULL | Setting value |
| description | TEXT | NULL | Setting description |
| updated_by_id | INTEGER | FK → admin_users.id, NULL | Last updater |
| updated_at | DATETIME | NOT NULL, AUTO | Update timestamp |

**Indexes**: config_key (unique), updated_by_id

---

### 24. connectivity_log
**Purpose**: Network connectivity tracking

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique identifier |
| user_id | INTEGER | FK → admin_users.id, NULL | User |
| is_online | BOOLEAN | NOT NULL | Online status |
| connection_type | VARCHAR(50) | NULL | Connection type (wifi, cellular, etc.) |
| latency_ms | INTEGER | NULL | Ping latency |
| error_message | TEXT | NULL | Error details |
| created_at | DATETIME | NOT NULL, AUTO | Log timestamp |

**Indexes**: user_id, is_online, created_at

---

## Chatbot Tables

### 25. chat_history (Flask Database)
**Purpose**: Chatbot conversation history (separate SQLite DB)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique identifier |
| user_message | TEXT | NOT NULL | User input |
| bot_reply | TEXT | NOT NULL | Bot response |

---

## Enumeration Values

### User Roles (admin_users.role)
| Value | Label | Permissions |
|-------|-------|-------------|
| super_admin | Safety and Security Office | Full system access |
| dean | College Dean | Approve announcements, view analytics |
| program_head | College Program Head | Create announcements, manage own rooms |
| basic_ed_head | Basic Education Head | Create announcements, manage own rooms |

### Departments (admin_users.department / departments.code)
| Code | Full Name |
|------|-----------|
| safety_security | Safety and Security Office |
| office_of_the_dean | Office of the Dean |
| college_agriculture | College of Agriculture and Fisheries |
| college_criminology | College of Criminal Justice Education |
| college_business | College of Business and Good Governance |
| college_ict | College of Information and Communication Technology |
| dept_civil_engineering | Department of Civil Engineering |
| college_teacher_education | College of Teacher Education |
| tesda | Technical Education and Skills Development Authority |
| general_education | General Education Department |
| basic_education | Basic Education Department |

### Department Colors (for mobile UI)
| Department | Color Key |
|------------|-----------|
| safety_security | red |
| office_of_the_dean | dark_blue |
| college_agriculture | green |
| college_criminology | charcoal |
| college_business | purple |
| college_ict | teal |
| dept_civil_engineering | amber |
| college_teacher_education | blue |
| tesda | dark_green |
| general_education | indigo |
| basic_education | brown |

### Room Types (rooms.room_type)
| Value | Label |
|-------|-------|
| classroom | Classroom |
| office | Office |
| lab | Laboratory |
| facility | Facility |
| staircase | Staircase |
| restroom | Restroom |
| other | Other |

### Announcement Status (announcements.status)
| Value | Label |
|-------|-------|
| pending_approval | Pending Approval |
| published | Published |
| rejected | Rejected |
| archived | Archived |

### Announcement Scope (announcements.scope)
| Value | Target Audience |
|-------|-----------------|
| campus_wide | Entire Campus (all users) |
| all_college | All College Students |
| basic_ed_only | Basic Education Only |
| department | Specific Department Only |

### Notification Types (notifications.type)
| Value | Description |
|-------|-------------|
| announcement | Department Announcement |
| info | General Info |
| emergency | Emergency Alert |
| facility_update | Facility Update |
| room_update | Room/Classroom Update |
| system_maintenance | System Maintenance |
| app_update | App Update |

### FAQ Categories (faq_entries.category)
| Value | Description |
|-------|-------------|
| location | Location questions |
| schedule | Schedule queries |
| academic | Academic information |
| services | Campus services |
| general | General inquiries |

### Feedback Categories (feedback.category)
| Value | Description |
|-------|-------------|
| map_accuracy | Map accuracy issues |
| ai_chatbot | Chatbot feedback |
| navigation | Navigation problems |
| general | General feedback |
| bug_report | Bug reports |
| facility | Facility-related |
| room | Room-related |

### Audit Actions (admin_audit_log.action)
| Value | Description |
|-------|-------------|
| login | User login |
| logout | User logout |
| create | Entity creation |
| update | Entity update |
| soft_delete | Soft delete |
| restore | Entity restoration |
| approve | Approval action |
| reject | Rejection action |
| publish | Publishing action |
| reset_password | Password reset |

---

## Database Statistics

| Metric | Value |
|--------|-------|
| Total Tables (Main DB) | 24 |
| Total Tables (Chatbot DB) | 1 |
| Total Tables (Combined) | 25 |
| Core Entities | 4 (users, facilities, rooms, navigation) |
| Communication Tables | 4 (announcements, notifications, faq, chat_logs) |
| Feedback Tables | 3 (ratings, feedback, feedback_flags) |
| Analytics Tables | 6 (audit_log, search_history, app_usage, usage_analytics, connectivity_log) |
| Config Tables | 4 (departments, notification_types, notification_preferences, app_config, device_preferences) |
| Map Tables | 2 (map_markers, map_labels) |

---

## Key Relationships Summary

```
DEPARTMENTS (1) ────< (N) FACILITIES
    │                    │
    │                    ├─< (N) ROOMS
    │                    │      │
    │                    │      └─< (N) NAVIGATION_NODES
    │                    │             │
    │                    │             └─< (N) NAVIGATION_EDGES
    │                    │
    │                    └─< (N) MAP_MARKERS
    │
    └─< (1) HEAD_USER (ADMIN_USERS)

ADMIN_USERS (1) ────< (N) ANNOUNCEMENTS (created)
    │                    │
    │                    ├─< (N) ANNOUNCEMENTS (approved)
    │                    ├─< (N) ANNOUNCEMENTS (rejected)
    │                    └─< (N) ANNOUNCEMENTS (archived)
    │
    ├─< (N) NOTIFICATIONS
    ├─< (N) RATINGS
    ├─< (N) ADMIN_AUDIT_LOG
    ├─< (N) SEARCH_HISTORY
    └─< (N) FEEDBACK_FLAGS

ANNOUNCEMENTS (1) ────< (N) NOTIFICATIONS

FAQ_ENTRIES (1) ────< (N) AI_CHAT_LOGS

RATING (1) ────< (N) FEEDBACK_FLAGS
```

---

*Generated for TechnoPath SEAIT Campus Guide v4*
*Date: April 2026*
