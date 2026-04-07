# TechnoPath: SEAIT Guide Map and Navigation System
## Database Design Document

---

## 1. DATABASE ARCHITECTURE OVERVIEW

### 1.1 Technology Stack
- **Primary Database**: PostgreSQL 14+ (Production)
- **Development/Fallback**: SQLite 3 (Development & Testing)
- **ORM**: Django ORM 4.2+
- **API Layer**: Django REST Framework
- **Caching**: Redis (Optional for production)
- **Offline Storage**: IndexedDB (Browser-side)

### 1.2 Database Schema Design Principles
1. **Normalization**: 3NF (Third Normal Form) for core entities
2. **Soft Deletes**: `is_deleted` flag pattern for data integrity
3. **Audit Trail**: Complete change tracking via `admin_audit_log`
4. **Multi-tenancy**: Department-scoped data access
5. **Offline-First**: IndexedDB synchronization support

### 1.3 Schema Diagram (High-Level)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                           TECHNOPATH DATABASE SCHEMA                                     │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                          │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐           │
│  │ departments  │◄───┤  facilities  │◄───┤    rooms     │◄───┤ map_markers  │           │
│  └──────┬───────┘    └──────────────┘    └──────────────┘    └──────────────┘           │
│         │                                                                                │
│         │         ┌──────────────┐    ┌──────────────────┐                              │
│         └────────►│ admin_users  │◄───┤  announcements   │                              │
│                   └──────┬───────┘    └──────────────────┘                              │
│                          │                                                              │
│  ┌──────────────┐       │         ┌──────────────┐    ┌──────────────┐                  │
│  │ nav_nodes    │       │         │ notifications│◄───┤ notif_read   │                  │
│  └──────┬───────┘       │         └──────────────┘    └──────────────┘                  │
│         │               │                                                              │
│  ┌──────▼───────┐       │         ┌──────────────┐    ┌──────────────┐                  │
│  │ nav_edges    │       └────────►│  audit_log   │    │   ratings    │                  │
│  └──────────────┘                 └──────────────┘    └──────┬───────┘                  │
│                                                              │                          │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐     │                          │
│  │faq_entries   │◄───┤ ai_chat_logs │    │   feedback   │◄────┘                          │
│  └──────────────┘    └──────────────┘    └──────────────┘                              │
│                                                                                          │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. TABLE SPECIFICATIONS

### 2.1 Core Entities

#### 2.1.1 `departments` - Department Registry
```sql
CREATE TABLE departments (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(200) NOT NULL,
    code            VARCHAR(20) UNIQUE NOT NULL,
    description     TEXT,
    head_user_id    INTEGER REFERENCES admin_users(id) ON DELETE SET NULL,
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_departments_code ON departments(code);
CREATE INDEX idx_departments_active ON departments(is_active);
```

#### 2.1.2 `admin_users` - Administrative User Accounts
```sql
CREATE TABLE admin_users (
    id              SERIAL PRIMARY KEY,
    username        VARCHAR(150) UNIQUE NOT NULL,
    email           VARCHAR(254),
    display_name    VARCHAR(200),
    role            VARCHAR(20) NOT NULL DEFAULT 'program_head',
    department      VARCHAR(50),
    department_label VARCHAR(200),
    is_active       BOOLEAN DEFAULT TRUE,
    is_staff        BOOLEAN DEFAULT FALSE,
    is_superuser    BOOLEAN DEFAULT FALSE,
    password        VARCHAR(128) NOT NULL,
    login_attempts  INTEGER DEFAULT 0,
    locked_until    TIMESTAMP,
    last_login      TIMESTAMP,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_role CHECK (role IN ('super_admin', 'dean', 'program_head', 'basic_ed_head'))
);

CREATE INDEX idx_admin_users_username ON admin_users(username);
CREATE INDEX idx_admin_users_role ON admin_users(role);
CREATE INDEX idx_admin_users_dept ON admin_users(department);
CREATE INDEX idx_admin_users_active ON admin_users(is_active);
```

#### 2.1.3 `facilities` - Campus Buildings
```sql
CREATE TABLE facilities (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(200) NOT NULL,
    code            VARCHAR(20) UNIQUE NOT NULL,
    description     TEXT,
    building_code   VARCHAR(20),
    department_id   INTEGER REFERENCES departments(id) ON DELETE SET NULL,
    latitude        FLOAT,
    longitude       FLOAT,
    image_path      VARCHAR(500),
    map_svg_id      VARCHAR(100),
    total_floors    INTEGER DEFAULT 1,
    is_deleted      BOOLEAN DEFAULT FALSE,
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_facilities_code ON facilities(code);
CREATE INDEX idx_facilities_dept ON facilities(department_id);
CREATE INDEX idx_facilities_active ON facilities(is_active) WHERE is_deleted = FALSE;
```

#### 2.1.4 `rooms` - Rooms and Spaces
```sql
CREATE TABLE rooms (
    id              SERIAL PRIMARY KEY,
    facility_id     INTEGER NOT NULL REFERENCES facilities(id) ON DELETE CASCADE,
    name            VARCHAR(200) NOT NULL,
    code            VARCHAR(50) NOT NULL,
    room_number     VARCHAR(50),
    description     TEXT,
    floor           INTEGER DEFAULT 1,
    map_svg_id      VARCHAR(100),
    room_type       VARCHAR(50) DEFAULT 'classroom',
    capacity        INTEGER DEFAULT 30,
    is_office       BOOLEAN DEFAULT FALSE,
    is_crucial      BOOLEAN DEFAULT FALSE,
    search_count    INTEGER DEFAULT 0,
    is_deleted      BOOLEAN DEFAULT FALSE,
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_room_type CHECK (room_type IN ('classroom', 'office', 'lab', 'facility', 'staircase', 'restroom', 'other')),
    UNIQUE(facility_id, code)
);

CREATE INDEX idx_rooms_facility ON rooms(facility_id);
CREATE INDEX idx_rooms_floor ON rooms(floor);
CREATE INDEX idx_rooms_type ON rooms(room_type);
CREATE INDEX idx_rooms_active ON rooms(is_active) WHERE is_deleted = FALSE;
```

---

### 2.2 Navigation System

#### 2.2.1 `navigation_nodes` - Navigation Graph Nodes
```sql
CREATE TABLE navigation_nodes (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(200) NOT NULL,
    node_type       VARCHAR(20) NOT NULL,
    facility_id     INTEGER REFERENCES facilities(id) ON DELETE SET NULL,
    room_id         INTEGER REFERENCES rooms(id) ON DELETE SET NULL,
    map_svg_id      VARCHAR(100),
    x               FLOAT NOT NULL,
    y               FLOAT NOT NULL,
    floor           INTEGER DEFAULT 1,
    is_deleted      BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_node_type CHECK (node_type IN ('room', 'facility', 'waypoint', 'entrance', 'staircase', 'elevator', 'junction'))
);

CREATE INDEX idx_nav_nodes_facility ON navigation_nodes(facility_id);
CREATE INDEX idx_nav_nodes_room ON navigation_nodes(room_id);
CREATE INDEX idx_nav_nodes_type ON navigation_nodes(node_type);
CREATE INDEX idx_nav_nodes_floor ON navigation_nodes(floor);
```

#### 2.2.2 `navigation_edges` - Navigation Graph Connections
```sql
CREATE TABLE navigation_edges (
    id              SERIAL PRIMARY KEY,
    from_node_id    INTEGER NOT NULL REFERENCES navigation_nodes(id) ON DELETE CASCADE,
    to_node_id      INTEGER NOT NULL REFERENCES navigation_nodes(id) ON DELETE CASCADE,
    distance        INTEGER NOT NULL,
    is_bidirectional BOOLEAN DEFAULT TRUE,
    is_deleted      BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(from_node_id, to_node_id)
);

CREATE INDEX idx_nav_edges_from ON navigation_edges(from_node_id);
CREATE INDEX idx_nav_edges_to ON navigation_edges(to_node_id);
```

---

### 2.3 Map Visualization

#### 2.3.1 `map_markers` - Interactive Map Markers
```sql
CREATE TABLE map_markers (
    id              SERIAL PRIMARY KEY,
    facility_id     INTEGER REFERENCES facilities(id) ON DELETE SET NULL,
    room_id         INTEGER REFERENCES rooms(id) ON DELETE SET NULL,
    name            VARCHAR(200) NOT NULL,
    x_position      FLOAT NOT NULL,
    y_position      FLOAT NOT NULL,
    marker_type     VARCHAR(20) DEFAULT 'facility',
    icon_name       VARCHAR(100) DEFAULT 'location_on',
    color_hex       VARCHAR(7) DEFAULT '#FF9800',
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_marker_type CHECK (marker_type IN ('facility', 'room', 'entrance', 'waypoint', 'amenity'))
);

CREATE INDEX idx_markers_facility ON map_markers(facility_id);
CREATE INDEX idx_markers_room ON map_markers(room_id);
CREATE INDEX idx_markers_type ON map_markers(marker_type);
```

#### 2.3.2 `map_labels` - Map Text Labels
```sql
CREATE TABLE map_labels (
    id              SERIAL PRIMARY KEY,
    label_text      VARCHAR(200) NOT NULL,
    x_position      FLOAT NOT NULL,
    y_position      FLOAT NOT NULL,
    font_size       INTEGER DEFAULT 14,
    color_hex       VARCHAR(7) DEFAULT '#000000',
    rotation        FLOAT DEFAULT 0,
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### 2.4 Communication System

#### 2.4.1 `announcements` - Department Announcements
```sql
CREATE TABLE announcements (
    id                  SERIAL PRIMARY KEY,
    title               VARCHAR(200) NOT NULL,
    content             TEXT NOT NULL,
    created_by_id       INTEGER REFERENCES admin_users(id) ON DELETE SET NULL,
    source_label        VARCHAR(200) NOT NULL,
    source_color        VARCHAR(20) DEFAULT 'orange',
    scope               VARCHAR(20) DEFAULT 'campus_wide',
    target_department   VARCHAR(50),
    status              VARCHAR(20) DEFAULT 'pending_approval',
    requires_approval   BOOLEAN DEFAULT TRUE,
    approved_by_id      INTEGER REFERENCES admin_users(id) ON DELETE SET NULL,
    rejected_by_id      INTEGER REFERENCES admin_users(id) ON DELETE SET NULL,
    rejection_note      TEXT,
    approved_at         TIMESTAMP,
    archived_by_id      INTEGER REFERENCES admin_users(id) ON DELETE SET NULL,
    archived_at         TIMESTAMP,
    is_deleted          BOOLEAN DEFAULT FALSE,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_scope CHECK (scope IN ('campus_wide', 'all_college', 'basic_ed_only', 'department')),
    CONSTRAINT chk_status CHECK (status IN ('pending_approval', 'published', 'rejected', 'archived'))
);

CREATE INDEX idx_announcements_status ON announcements(status);
CREATE INDEX idx_announcements_scope ON announcements(scope);
CREATE INDEX idx_announcements_created_by ON announcements(created_by_id);
CREATE INDEX idx_announcements_created_at ON announcements(created_at DESC);
```

#### 2.4.2 `notifications` - Mobile Push Notifications
```sql
CREATE TABLE notifications (
    id              SERIAL PRIMARY KEY,
    title           VARCHAR(200) NOT NULL,
    message         TEXT NOT NULL,
    type            VARCHAR(30) DEFAULT 'info',
    source_label    VARCHAR(200) DEFAULT '',
    source_color    VARCHAR(20) DEFAULT 'orange',
    announcement_id INTEGER REFERENCES announcements(id) ON DELETE SET NULL,
    priority        INTEGER DEFAULT 1,
    expires_at      TIMESTAMP,
    created_by_id   INTEGER REFERENCES admin_users(id) ON DELETE SET NULL,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_notif_type CHECK (type IN ('announcement', 'info', 'emergency', 'facility_update', 'room_update', 'system_maintenance', 'app_update')),
    CONSTRAINT chk_priority CHECK (priority IN (1, 2, 3, 4))
);

CREATE INDEX idx_notifications_type ON notifications(type);
CREATE INDEX idx_notifications_priority ON notifications(priority);
CREATE INDEX idx_notifications_created_at ON notifications(created_at DESC);
```

#### 2.4.3 `notification_read_status` - Read Receipts
```sql
CREATE TABLE notification_read_status (
    id              SERIAL PRIMARY KEY,
    user_id         INTEGER NOT NULL REFERENCES admin_users(id) ON DELETE CASCADE,
    notification_id INTEGER NOT NULL REFERENCES notifications(id) ON DELETE CASCADE,
    read_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(user_id, notification_id)
);

CREATE INDEX idx_notif_read_user ON notification_read_status(user_id);
CREATE INDEX idx_notif_read_notif ON notification_read_status(notification_id);
```

---

### 2.5 Chatbot System

#### 2.5.1 `faq_entries` - FAQ Knowledge Base
```sql
CREATE TABLE faq_entries (
    id              SERIAL PRIMARY KEY,
    question        TEXT NOT NULL,
    answer          TEXT NOT NULL,
    category        VARCHAR(50) DEFAULT 'general',
    keywords        TEXT DEFAULT '',
    usage_count     INTEGER DEFAULT 0,
    is_deleted      BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_faq_category CHECK (category IN ('location', 'schedule', 'academic', 'services', 'general'))
);

CREATE INDEX idx_faq_category ON faq_entries(category);
CREATE INDEX idx_faq_usage ON faq_entries(usage_count DESC);
```

#### 2.5.2 `ai_chat_logs` - Chat Interaction History
```sql
CREATE TABLE ai_chat_logs (
    id              SERIAL PRIMARY KEY,
    user_query      TEXT NOT NULL,
    ai_response     TEXT,
    mode            VARCHAR(10) NOT NULL,
    response_time_ms INTEGER,
    is_successful   BOOLEAN DEFAULT TRUE,
    error_message   TEXT,
    faq_entry_id    INTEGER REFERENCES faq_entries(id) ON DELETE SET NULL,
    session_id      VARCHAR(100),
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_mode CHECK (mode IN ('online', 'offline'))
);

CREATE INDEX idx_chat_logs_session ON ai_chat_logs(session_id);
CREATE INDEX idx_chat_logs_created ON ai_chat_logs(created_at DESC);
```

---

### 2.6 Feedback & Rating System

#### 2.6.1 `feedback` - User Feedback Submissions
```sql
CREATE TABLE feedback (
    id              SERIAL PRIMARY KEY,
    rating          INTEGER CHECK (rating >= 1 AND rating <= 5),
    comment         TEXT,
    category        VARCHAR(30) DEFAULT 'general',
    facility_id     INTEGER REFERENCES facilities(id) ON DELETE SET NULL,
    room_id         INTEGER REFERENCES rooms(id) ON DELETE SET NULL,
    is_flagged      BOOLEAN DEFAULT FALSE,
    flag_reason     TEXT,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_feedback_category CHECK (category IN ('map_accuracy', 'ai_chatbot', 'navigation', 'general', 'bug_report', 'facility', 'room'))
);

CREATE INDEX idx_feedback_category ON feedback(category);
CREATE INDEX idx_feedback_flagged ON feedback(is_flagged) WHERE is_flagged = TRUE;
CREATE INDEX idx_feedback_created ON feedback(created_at DESC);
```

#### 2.6.2 `ratings` - App & Location Ratings
```sql
CREATE TABLE ratings (
    id              SERIAL PRIMARY KEY,
    user_id         INTEGER REFERENCES admin_users(id) ON DELETE SET NULL,
    facility_id     INTEGER REFERENCES facilities(id) ON DELETE SET NULL,
    room_id         INTEGER REFERENCES rooms(id) ON DELETE SET NULL,
    rating          INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    comment         TEXT,
    category        VARCHAR(20) DEFAULT 'general',
    is_anonymous    BOOLEAN DEFAULT TRUE,
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_rating_category CHECK (category IN ('general', 'facility', 'room', 'navigation', 'app'))
);

CREATE INDEX idx_ratings_category ON ratings(category);
CREATE INDEX idx_ratings_active ON ratings(is_active);
```

#### 2.6.3 `feedback_flags` - Content Moderation
```sql
CREATE TABLE feedback_flags (
    id              SERIAL PRIMARY KEY,
    user_id         INTEGER REFERENCES admin_users(id) ON DELETE SET NULL,
    rating_id       INTEGER NOT NULL REFERENCES ratings(id) ON DELETE CASCADE,
    reason          TEXT NOT NULL,
    status          VARCHAR(20) DEFAULT 'pending',
    resolved_by_id  INTEGER REFERENCES admin_users(id) ON DELETE SET NULL,
    resolved_at     TIMESTAMP,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_flag_status CHECK (status IN ('pending', 'reviewed', 'resolved', 'dismissed'))
);

CREATE INDEX idx_flags_status ON feedback_flags(status);
CREATE INDEX idx_flags_rating ON feedback_flags(rating_id);
```

---

### 2.7 Audit & Analytics

#### 2.7.1 `admin_audit_log` - Complete Activity Audit Trail
```sql
CREATE TABLE admin_audit_log (
    id              SERIAL PRIMARY KEY,
    admin_id        INTEGER REFERENCES admin_users(id) ON DELETE SET NULL,
    action          VARCHAR(20) NOT NULL,
    entity_type     VARCHAR(50),
    entity_id       INTEGER,
    entity_label    VARCHAR(200),
    old_value_json  TEXT,
    new_value_json  TEXT,
    ip_address      VARCHAR(50),
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_action CHECK (action IN ('login', 'logout', 'create', 'update', 'soft_delete', 'restore', 'approve', 'reject', 'publish', 'reset_password'))
);

CREATE INDEX idx_audit_admin ON admin_audit_log(admin_id);
CREATE INDEX idx_audit_action ON admin_audit_log(action);
CREATE INDEX idx_audit_entity ON admin_audit_log(entity_type, entity_id);
CREATE INDEX idx_audit_created ON admin_audit_log(created_at DESC);
```

#### 2.7.2 `search_history` - Search Analytics
```sql
CREATE TABLE search_history (
    id              SERIAL PRIMARY KEY,
    user_id         INTEGER REFERENCES admin_users(id) ON DELETE SET NULL,
    query           VARCHAR(500) NOT NULL,
    results_count   INTEGER DEFAULT 0,
    was_clicked     BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_search_user ON search_history(user_id);
CREATE INDEX idx_search_created ON search_history(created_at DESC);
```

#### 2.7.3 `app_usage` - Session Tracking
```sql
CREATE TABLE app_usage (
    id              SERIAL PRIMARY KEY,
    user_id         INTEGER REFERENCES admin_users(id) ON DELETE CASCADE,
    session_date    DATE NOT NULL,
    session_duration INTEGER DEFAULT 0,
    screen_views    INTEGER DEFAULT 0,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_usage_user ON app_usage(user_id);
CREATE INDEX idx_usage_date ON app_usage(session_date);
```

#### 2.7.4 `usage_analytics` - Event Tracking
```sql
CREATE TABLE usage_analytics (
    id              SERIAL PRIMARY KEY,
    user_id         INTEGER REFERENCES admin_users(id) ON DELETE SET NULL,
    event_type      VARCHAR(50) NOT NULL,
    event_data      JSONB,
    screen_name     VARCHAR(100),
    session_id      VARCHAR(100),
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_event_type CHECK (event_type IN ('screen_view', 'search', 'navigation', 'rating', 'feedback', 'share', 'notification_open'))
);

CREATE INDEX idx_analytics_type ON usage_analytics(event_type);
CREATE INDEX idx_analytics_session ON usage_analytics(session_id);
CREATE INDEX idx_analytics_created ON usage_analytics(created_at DESC);
```

---

### 2.8 System Configuration

#### 2.8.1 `device_preferences` - User Device Settings
```sql
CREATE TABLE device_preferences (
    id              SERIAL PRIMARY KEY,
    user_id         INTEGER REFERENCES admin_users(id) ON DELETE SET NULL,
    device_id       VARCHAR(200) NOT NULL,
    dark_mode       BOOLEAN DEFAULT FALSE,
    language        VARCHAR(10) DEFAULT 'en',
    font_scale      FLOAT DEFAULT 1.0,
    high_contrast   BOOLEAN DEFAULT FALSE,
    reduce_animations BOOLEAN DEFAULT FALSE,
    last_sync       TIMESTAMP,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_device_prefs_user ON device_preferences(user_id);
CREATE INDEX idx_device_id ON device_preferences(device_id);
```

#### 2.8.2 `app_config` - System Configuration
```sql
CREATE TABLE app_config (
    id              SERIAL PRIMARY KEY,
    config_key      VARCHAR(100) UNIQUE NOT NULL,
    config_value    TEXT NOT NULL,
    description     TEXT,
    updated_by_id   INTEGER REFERENCES admin_users(id) ON DELETE SET NULL,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_app_config_key ON app_config(config_key);
```

#### 2.8.3 `connectivity_log` - Network Status Tracking
```sql
CREATE TABLE connectivity_log (
    id              SERIAL PRIMARY KEY,
    user_id         INTEGER REFERENCES admin_users(id) ON DELETE SET NULL,
    is_online       BOOLEAN NOT NULL,
    connection_type VARCHAR(50),
    latency_ms      INTEGER,
    error_message   TEXT,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_connectivity_user ON connectivity_log(user_id);
CREATE INDEX idx_connectivity_created ON connectivity_log(created_at DESC);
```

---

## 3. DATABASE CONSTRAINTS & INDEXING STRATEGY

### 3.1 Unique Constraints
| Table | Constraint | Columns |
|-------|-----------|---------|
| departments | UNIQUE | code |
| admin_users | UNIQUE | username |
| facilities | UNIQUE | code |
| rooms | UNIQUE | facility_id, code |
| navigation_edges | UNIQUE | from_node_id, to_node_id |
| notification_read_status | UNIQUE | user_id, notification_id |
| notification_preferences | UNIQUE | user_id, notification_type_id |
| app_config | UNIQUE | config_key |

### 3.2 Foreign Key Relationships
| Child Table | Column | Parent Table | On Delete |
|-------------|--------|--------------|-----------|
| departments | head_user_id | admin_users | SET NULL |
| facilities | department_id | departments | SET NULL |
| rooms | facility_id | facilities | CASCADE |
| navigation_nodes | facility_id | facilities | SET NULL |
| navigation_nodes | room_id | rooms | SET NULL |
| announcements | created_by_id | admin_users | SET NULL |
| announcements | approved_by_id | admin_users | SET NULL |
| notifications | created_by_id | admin_users | SET NULL |
| map_markers | facility_id | facilities | SET NULL |
| ratings | user_id | admin_users | SET NULL |
| admin_audit_log | admin_id | admin_users | SET NULL |

### 3.3 Index Strategy

**B-Tree Indexes (Default)**:
- Primary keys (automatic)
- Foreign keys (automatic)
- Search fields: username, code, name
- Date fields: created_at, updated_at
- Status fields: is_active, is_deleted, status

**Partial Indexes**:
```sql
-- Active facilities only
CREATE INDEX idx_facilities_active ON facilities(code) WHERE is_active = TRUE AND is_deleted = FALSE;

-- Published announcements
CREATE INDEX idx_announcements_published ON announcements(created_at) WHERE status = 'published';

-- Pending feedback flags
CREATE INDEX idx_flags_pending ON feedback_flags(created_at) WHERE status = 'pending';
```

---

## 4. DATA RETENTION & ARCHIVAL POLICY

| Data Type | Retention Period | Archival Action |
|-----------|-----------------|-----------------|
| Audit Logs | 2 years | Archive to cold storage |
| Search History | 6 months | Delete after retention |
| Chat Logs | 1 year | Anonymize and archive |
| Connectivity Logs | 3 months | Delete after retention |
| Usage Analytics | 1 year | Aggregate and archive |
| Notifications | 90 days | Soft delete after expiry |
| Deleted Entities | Indefinite | Soft delete retained |

---

## 5. BACKUP & RECOVERY

### 5.1 Backup Schedule
- **Full Backup**: Daily at 02:00 UTC
- **Incremental**: Every 4 hours
- **Transaction Logs**: Continuous

### 5.2 Point-in-Time Recovery
- RPO (Recovery Point Objective): 15 minutes
- RTO (Recovery Time Objective): 30 minutes

---

*Document Version: 1.0*
*Generated from TechnoPath V4 Codebase Analysis*
