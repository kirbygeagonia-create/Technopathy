-- ============================================================================
-- TechnoPath: SEAIT Guide Map and Navigation System
-- Complete Database Schema (PostgreSQL Compatible)
-- ============================================================================
-- Version: 1.0
-- Generated: April 2026
-- Total Tables: 25
-- ============================================================================

-- Enable UUID extension (optional, for future use)
-- CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================================
-- 1. CORE ENTITY TABLES
-- ============================================================================

-- Admin Users Table (Custom User Model)
CREATE TABLE admin_users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(150) UNIQUE NOT NULL,
    email VARCHAR(254) NULL,
    display_name VARCHAR(200) NULL,
    password VARCHAR(128) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'program_head',
    department VARCHAR(50) NULL,
    department_label VARCHAR(200) NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_staff BOOLEAN NOT NULL DEFAULT FALSE,
    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
    login_attempts INTEGER NOT NULL DEFAULT 0,
    locked_until TIMESTAMP NULL,
    last_login TIMESTAMP NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_admin_users_role CHECK (role IN ('super_admin', 'dean', 'program_head', 'basic_ed_head'))
);

CREATE INDEX idx_admin_users_username ON admin_users(username);
CREATE INDEX idx_admin_users_role ON admin_users(role);
CREATE INDEX idx_admin_users_department ON admin_users(department);
CREATE INDEX idx_admin_users_active ON admin_users(is_active);

COMMENT ON TABLE admin_users IS 'Administrative user accounts with role-based access control';

-- Departments Table
CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    code VARCHAR(20) UNIQUE NOT NULL,
    description TEXT NULL,
    head_user_id INTEGER NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_departments_head_user 
        FOREIGN KEY (head_user_id) REFERENCES admin_users(id) ON DELETE SET NULL
);

CREATE INDEX idx_departments_code ON departments(code);
CREATE INDEX idx_departments_active ON departments(is_active);

COMMENT ON TABLE departments IS 'Department registry with head assignment';

-- Facilities Table
CREATE TABLE facilities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    code VARCHAR(20) UNIQUE NOT NULL,
    description TEXT NULL,
    building_code VARCHAR(20) NULL,
    department_id INTEGER NULL,
    latitude FLOAT NULL,
    longitude FLOAT NULL,
    image_path VARCHAR(500) NULL,
    map_svg_id VARCHAR(100) NULL,
    total_floors INTEGER NOT NULL DEFAULT 1,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_facilities_department 
        FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE SET NULL
);

CREATE INDEX idx_facilities_code ON facilities(code);
CREATE INDEX idx_facilities_department ON facilities(department_id);
CREATE INDEX idx_facilities_active ON facilities(is_active) WHERE is_deleted = FALSE;

COMMENT ON TABLE facilities IS 'Campus buildings and facilities';

-- Rooms Table
CREATE TABLE rooms (
    id SERIAL PRIMARY KEY,
    facility_id INTEGER NOT NULL,
    name VARCHAR(200) NOT NULL,
    code VARCHAR(50) NOT NULL,
    room_number VARCHAR(50) NULL,
    description TEXT NULL,
    floor INTEGER NOT NULL DEFAULT 1,
    map_svg_id VARCHAR(100) NULL,
    room_type VARCHAR(50) NOT NULL DEFAULT 'classroom',
    capacity INTEGER NOT NULL DEFAULT 30,
    is_office BOOLEAN NOT NULL DEFAULT FALSE,
    is_crucial BOOLEAN NOT NULL DEFAULT FALSE,
    search_count INTEGER NOT NULL DEFAULT 0,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_rooms_facility 
        FOREIGN KEY (facility_id) REFERENCES facilities(id) ON DELETE CASCADE,
    CONSTRAINT chk_rooms_room_type 
        CHECK (room_type IN ('classroom', 'office', 'lab', 'facility', 'staircase', 'restroom', 'other')),
    UNIQUE (facility_id, code)
);

CREATE INDEX idx_rooms_facility ON rooms(facility_id);
CREATE INDEX idx_rooms_floor ON rooms(floor);
CREATE INDEX idx_rooms_room_type ON rooms(room_type);
CREATE INDEX idx_rooms_active ON rooms(is_active) WHERE is_deleted = FALSE;

COMMENT ON TABLE rooms IS 'Rooms and spaces within facilities';

-- ============================================================================
-- 2. NAVIGATION SYSTEM TABLES
-- ============================================================================

-- Navigation Nodes Table
CREATE TABLE navigation_nodes (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    node_type VARCHAR(20) NOT NULL,
    facility_id INTEGER NULL,
    room_id INTEGER NULL,
    map_svg_id VARCHAR(100) NULL,
    x FLOAT NOT NULL,
    y FLOAT NOT NULL,
    floor INTEGER NOT NULL DEFAULT 1,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_nav_nodes_facility 
        FOREIGN KEY (facility_id) REFERENCES facilities(id) ON DELETE SET NULL,
    CONSTRAINT fk_nav_nodes_room 
        FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE SET NULL,
    CONSTRAINT chk_nav_nodes_node_type 
        CHECK (node_type IN ('room', 'facility', 'waypoint', 'entrance', 'staircase', 'elevator', 'junction'))
);

CREATE INDEX idx_nav_nodes_facility ON navigation_nodes(facility_id);
CREATE INDEX idx_nav_nodes_room ON navigation_nodes(room_id);
CREATE INDEX idx_nav_nodes_node_type ON navigation_nodes(node_type);
CREATE INDEX idx_nav_nodes_floor ON navigation_nodes(floor);

COMMENT ON TABLE navigation_nodes IS 'Navigation graph nodes for pathfinding';

-- Navigation Edges Table
CREATE TABLE navigation_edges (
    id SERIAL PRIMARY KEY,
    from_node_id INTEGER NOT NULL,
    to_node_id INTEGER NOT NULL,
    distance INTEGER NOT NULL,
    is_bidirectional BOOLEAN NOT NULL DEFAULT TRUE,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_nav_edges_from_node 
        FOREIGN KEY (from_node_id) REFERENCES navigation_nodes(id) ON DELETE CASCADE,
    CONSTRAINT fk_nav_edges_to_node 
        FOREIGN KEY (to_node_id) REFERENCES navigation_nodes(id) ON DELETE CASCADE,
    UNIQUE (from_node_id, to_node_id)
);

CREATE INDEX idx_nav_edges_from ON navigation_edges(from_node_id);
CREATE INDEX idx_nav_edges_to ON navigation_edges(to_node_id);

COMMENT ON TABLE navigation_edges IS 'Navigation graph edges connecting nodes';

-- ============================================================================
-- 3. MAP VISUALIZATION TABLES
-- ============================================================================

-- Map Markers Table
CREATE TABLE map_markers (
    id SERIAL PRIMARY KEY,
    facility_id INTEGER NULL,
    room_id INTEGER NULL,
    name VARCHAR(200) NOT NULL,
    x_position FLOAT NOT NULL,
    y_position FLOAT NOT NULL,
    marker_type VARCHAR(20) NOT NULL DEFAULT 'facility',
    icon_name VARCHAR(100) NOT NULL DEFAULT 'location_on',
    color_hex VARCHAR(7) NOT NULL DEFAULT '#FF9800',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_map_markers_facility 
        FOREIGN KEY (facility_id) REFERENCES facilities(id) ON DELETE SET NULL,
    CONSTRAINT fk_map_markers_room 
        FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE SET NULL,
    CONSTRAINT chk_map_markers_type 
        CHECK (marker_type IN ('facility', 'room', 'entrance', 'waypoint', 'amenity'))
);

CREATE INDEX idx_map_markers_facility ON map_markers(facility_id);
CREATE INDEX idx_map_markers_room ON map_markers(room_id);
CREATE INDEX idx_map_markers_type ON map_markers(marker_type);

COMMENT ON TABLE map_markers IS 'Interactive map markers for facilities and rooms';

-- Map Labels Table
CREATE TABLE map_labels (
    id SERIAL PRIMARY KEY,
    label_text VARCHAR(200) NOT NULL,
    x_position FLOAT NOT NULL,
    y_position FLOAT NOT NULL,
    font_size INTEGER NOT NULL DEFAULT 14,
    color_hex VARCHAR(7) NOT NULL DEFAULT '#000000',
    rotation FLOAT NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE map_labels IS 'Map text labels with positioning';

-- ============================================================================
-- 4. COMMUNICATION SYSTEM TABLES
-- ============================================================================

-- Announcements Table
CREATE TABLE announcements (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    created_by_id INTEGER NULL,
    source_label VARCHAR(200) NOT NULL,
    source_color VARCHAR(20) NOT NULL DEFAULT 'orange',
    scope VARCHAR(20) NOT NULL DEFAULT 'campus_wide',
    target_department VARCHAR(50) NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending_approval',
    requires_approval BOOLEAN NOT NULL DEFAULT TRUE,
    approved_by_id INTEGER NULL,
    rejected_by_id INTEGER NULL,
    rejection_note TEXT NULL,
    approved_at TIMESTAMP NULL,
    archived_by_id INTEGER NULL,
    archived_at TIMESTAMP NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_announcements_created_by 
        FOREIGN KEY (created_by_id) REFERENCES admin_users(id) ON DELETE SET NULL,
    CONSTRAINT fk_announcements_approved_by 
        FOREIGN KEY (approved_by_id) REFERENCES admin_users(id) ON DELETE SET NULL,
    CONSTRAINT fk_announcements_rejected_by 
        FOREIGN KEY (rejected_by_id) REFERENCES admin_users(id) ON DELETE SET NULL,
    CONSTRAINT fk_announcements_archived_by 
        FOREIGN KEY (archived_by_id) REFERENCES admin_users(id) ON DELETE SET NULL,
    CONSTRAINT chk_announcements_scope 
        CHECK (scope IN ('campus_wide', 'all_college', 'basic_ed_only', 'department')),
    CONSTRAINT chk_announcements_status 
        CHECK (status IN ('pending_approval', 'published', 'rejected', 'archived'))
);

CREATE INDEX idx_announcements_status ON announcements(status);
CREATE INDEX idx_announcements_scope ON announcements(scope);
CREATE INDEX idx_announcements_created_by ON announcements(created_by_id);
CREATE INDEX idx_announcements_created_at ON announcements(created_at DESC);
CREATE INDEX idx_announcements_published ON announcements(created_at) WHERE status = 'published';

COMMENT ON TABLE announcements IS 'Department and campus-wide announcements with approval workflow';

-- Notifications Table
CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    type VARCHAR(30) NOT NULL DEFAULT 'info',
    source_label VARCHAR(200) NOT NULL DEFAULT '',
    source_color VARCHAR(20) NOT NULL DEFAULT 'orange',
    announcement_id INTEGER NULL,
    priority INTEGER NOT NULL DEFAULT 1,
    expires_at TIMESTAMP NULL,
    created_by_id INTEGER NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_notifications_announcement 
        FOREIGN KEY (announcement_id) REFERENCES announcements(id) ON DELETE SET NULL,
    CONSTRAINT fk_notifications_created_by 
        FOREIGN KEY (created_by_id) REFERENCES admin_users(id) ON DELETE SET NULL,
    CONSTRAINT chk_notifications_type 
        CHECK (type IN ('announcement', 'info', 'emergency', 'facility_update', 'room_update', 'system_maintenance', 'app_update')),
    CONSTRAINT chk_notifications_priority 
        CHECK (priority IN (1, 2, 3, 4))
);

CREATE INDEX idx_notifications_type ON notifications(type);
CREATE INDEX idx_notifications_priority ON notifications(priority);
CREATE INDEX idx_notifications_created_at ON notifications(created_at DESC);

COMMENT ON TABLE notifications IS 'Mobile push notifications';

-- Notification Read Status Table
CREATE TABLE notification_read_status (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    notification_id INTEGER NOT NULL,
    read_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_notif_read_user 
        FOREIGN KEY (user_id) REFERENCES admin_users(id) ON DELETE CASCADE,
    CONSTRAINT fk_notif_read_notification 
        FOREIGN KEY (notification_id) REFERENCES notifications(id) ON DELETE CASCADE,
    UNIQUE (user_id, notification_id)
);

CREATE INDEX idx_notif_read_user ON notification_read_status(user_id);
CREATE INDEX idx_notif_read_notification ON notification_read_status(notification_id);

COMMENT ON TABLE notification_read_status IS 'Tracks which users have read notifications';

-- Notification Types Table (Reference)
CREATE TABLE notification_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT NULL,
    icon_name VARCHAR(100) NOT NULL DEFAULT 'notifications',
    color_hex VARCHAR(7) NOT NULL DEFAULT '#FF9800',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE notification_types IS 'Notification type definitions';

-- Notification Preferences Table
CREATE TABLE notification_preferences (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    notification_type_id INTEGER NOT NULL,
    is_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_notif_prefs_user 
        FOREIGN KEY (user_id) REFERENCES admin_users(id) ON DELETE CASCADE,
    CONSTRAINT fk_notif_prefs_type 
        FOREIGN KEY (notification_type_id) REFERENCES notification_types(id) ON DELETE CASCADE,
    UNIQUE (user_id, notification_type_id)
);

COMMENT ON TABLE notification_preferences IS 'User notification preferences by type';

-- ============================================================================
-- 5. CHATBOT SYSTEM TABLES
-- ============================================================================

-- FAQ Entries Table
CREATE TABLE faq_entries (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    category VARCHAR(50) NOT NULL DEFAULT 'general',
    keywords TEXT NOT NULL DEFAULT '',
    usage_count INTEGER NOT NULL DEFAULT 0,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_faq_category 
        CHECK (category IN ('location', 'schedule', 'academic', 'services', 'general'))
);

CREATE INDEX idx_faq_category ON faq_entries(category);
CREATE INDEX idx_faq_usage ON faq_entries(usage_count DESC);

COMMENT ON TABLE faq_entries IS 'FAQ knowledge base for chatbot';

-- AI Chat Logs Table
CREATE TABLE ai_chat_logs (
    id SERIAL PRIMARY KEY,
    user_query TEXT NOT NULL,
    ai_response TEXT NULL,
    mode VARCHAR(10) NOT NULL,
    response_time_ms INTEGER NULL,
    is_successful BOOLEAN NOT NULL DEFAULT TRUE,
    error_message TEXT NULL,
    faq_entry_id INTEGER NULL,
    session_id VARCHAR(100) NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_chat_logs_faq 
        FOREIGN KEY (faq_entry_id) REFERENCES faq_entries(id) ON DELETE SET NULL,
    CONSTRAINT chk_chat_mode 
        CHECK (mode IN ('online', 'offline'))
);

CREATE INDEX idx_chat_logs_session ON ai_chat_logs(session_id);
CREATE INDEX idx_chat_logs_created ON ai_chat_logs(created_at DESC);

COMMENT ON TABLE ai_chat_logs IS 'Chat interaction history';

-- ============================================================================
-- 6. FEEDBACK SYSTEM TABLES
-- ============================================================================

-- Feedback Table
CREATE TABLE feedback (
    id SERIAL PRIMARY KEY,
    rating INTEGER NULL CHECK (rating >= 1 AND rating <= 5),
    comment TEXT NULL,
    category VARCHAR(30) NOT NULL DEFAULT 'general',
    facility_id INTEGER NULL,
    room_id INTEGER NULL,
    is_flagged BOOLEAN NOT NULL DEFAULT FALSE,
    flag_reason TEXT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_feedback_facility 
        FOREIGN KEY (facility_id) REFERENCES facilities(id) ON DELETE SET NULL,
    CONSTRAINT fk_feedback_room 
        FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE SET NULL,
    CONSTRAINT chk_feedback_category 
        CHECK (category IN ('map_accuracy', 'ai_chatbot', 'navigation', 'general', 'bug_report', 'facility', 'room'))
);

CREATE INDEX idx_feedback_category ON feedback(category);
CREATE INDEX idx_feedback_flagged ON feedback(is_flagged) WHERE is_flagged = TRUE;
CREATE INDEX idx_feedback_created ON feedback(created_at DESC);

COMMENT ON TABLE feedback IS 'User feedback submissions';

-- Ratings Table
CREATE TABLE ratings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NULL,
    facility_id INTEGER NULL,
    room_id INTEGER NULL,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    comment TEXT NULL,
    category VARCHAR(20) NOT NULL DEFAULT 'general',
    is_anonymous BOOLEAN NOT NULL DEFAULT TRUE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_ratings_user 
        FOREIGN KEY (user_id) REFERENCES admin_users(id) ON DELETE SET NULL,
    CONSTRAINT fk_ratings_facility 
        FOREIGN KEY (facility_id) REFERENCES facilities(id) ON DELETE SET NULL,
    CONSTRAINT fk_ratings_room 
        FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE SET NULL,
    CONSTRAINT chk_ratings_category 
        CHECK (category IN ('general', 'facility', 'room', 'navigation', 'app'))
);

CREATE INDEX idx_ratings_category ON ratings(category);
CREATE INDEX idx_ratings_active ON ratings(is_active);

COMMENT ON TABLE ratings IS 'App and location ratings';

-- Feedback Flags Table (Content Moderation)
CREATE TABLE feedback_flags (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NULL,
    rating_id INTEGER NOT NULL,
    reason TEXT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    resolved_by_id INTEGER NULL,
    resolved_at TIMESTAMP NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_flags_user 
        FOREIGN KEY (user_id) REFERENCES admin_users(id) ON DELETE SET NULL,
    CONSTRAINT fk_flags_rating 
        FOREIGN KEY (rating_id) REFERENCES ratings(id) ON DELETE CASCADE,
    CONSTRAINT fk_flags_resolved_by 
        FOREIGN KEY (resolved_by_id) REFERENCES admin_users(id) ON DELETE SET NULL,
    CONSTRAINT chk_flags_status 
        CHECK (status IN ('pending', 'reviewed', 'resolved', 'dismissed'))
);

CREATE INDEX idx_flags_status ON feedback_flags(status);
CREATE INDEX idx_flags_rating ON feedback_flags(rating_id);

COMMENT ON TABLE feedback_flags IS 'Content moderation flags for ratings';

-- ============================================================================
-- 7. AUDIT & ANALYTICS TABLES
-- ============================================================================

-- Admin Audit Log Table
CREATE TABLE admin_audit_log (
    id SERIAL PRIMARY KEY,
    admin_id INTEGER NULL,
    action VARCHAR(20) NOT NULL,
    entity_type VARCHAR(50) NULL,
    entity_id INTEGER NULL,
    entity_label VARCHAR(200) NULL,
    old_value_json TEXT NULL,
    new_value_json TEXT NULL,
    ip_address VARCHAR(50) NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_audit_admin 
        FOREIGN KEY (admin_id) REFERENCES admin_users(id) ON DELETE SET NULL,
    CONSTRAINT chk_audit_action 
        CHECK (action IN ('login', 'logout', 'create', 'update', 'soft_delete', 'restore', 'approve', 'reject', 'publish', 'reset_password'))
);

CREATE INDEX idx_audit_admin ON admin_audit_log(admin_id);
CREATE INDEX idx_audit_action ON admin_audit_log(action);
CREATE INDEX idx_audit_entity ON admin_audit_log(entity_type, entity_id);
CREATE INDEX idx_audit_created ON admin_audit_log(created_at DESC);

COMMENT ON TABLE admin_audit_log IS 'Complete activity audit trail';

-- Search History Table
CREATE TABLE search_history (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NULL,
    query VARCHAR(500) NOT NULL,
    results_count INTEGER NOT NULL DEFAULT 0,
    was_clicked BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_search_user 
        FOREIGN KEY (user_id) REFERENCES admin_users(id) ON DELETE SET NULL
);

CREATE INDEX idx_search_user ON search_history(user_id);
CREATE INDEX idx_search_created ON search_history(created_at DESC);

COMMENT ON TABLE search_history IS 'Search query analytics';

-- App Usage Table
CREATE TABLE app_usage (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NULL,
    session_date DATE NOT NULL,
    session_duration INTEGER NOT NULL DEFAULT 0,
    screen_views INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_usage_user 
        FOREIGN KEY (user_id) REFERENCES admin_users(id) ON DELETE CASCADE
);

CREATE INDEX idx_usage_user ON app_usage(user_id);
CREATE INDEX idx_usage_date ON app_usage(session_date);

COMMENT ON TABLE app_usage IS 'Daily session usage tracking';

-- Usage Analytics Table (Event Tracking)
CREATE TABLE usage_analytics (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NULL,
    event_type VARCHAR(50) NOT NULL,
    event_data JSONB NULL,
    screen_name VARCHAR(100) NULL,
    session_id VARCHAR(100) NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_analytics_user 
        FOREIGN KEY (user_id) REFERENCES admin_users(id) ON DELETE SET NULL,
    CONSTRAINT chk_analytics_event 
        CHECK (event_type IN ('screen_view', 'search', 'navigation', 'rating', 'feedback', 'share', 'notification_open'))
);

CREATE INDEX idx_analytics_type ON usage_analytics(event_type);
CREATE INDEX idx_analytics_session ON usage_analytics(session_id);
CREATE INDEX idx_analytics_created ON usage_analytics(created_at DESC);

COMMENT ON TABLE usage_analytics IS 'User event tracking';

-- ============================================================================
-- 8. SYSTEM CONFIGURATION TABLES
-- ============================================================================

-- Device Preferences Table
CREATE TABLE device_preferences (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NULL,
    device_id VARCHAR(200) NOT NULL,
    dark_mode BOOLEAN NOT NULL DEFAULT FALSE,
    language VARCHAR(10) NOT NULL DEFAULT 'en',
    font_scale FLOAT NOT NULL DEFAULT 1.0,
    high_contrast BOOLEAN NOT NULL DEFAULT FALSE,
    reduce_animations BOOLEAN NOT NULL DEFAULT FALSE,
    last_sync TIMESTAMP NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_device_prefs_user 
        FOREIGN KEY (user_id) REFERENCES admin_users(id) ON DELETE SET NULL
);

CREATE INDEX idx_device_prefs_user ON device_preferences(user_id);
CREATE INDEX idx_device_id ON device_preferences(device_id);

COMMENT ON TABLE device_preferences IS 'User device settings and preferences';

-- App Configuration Table
CREATE TABLE app_config (
    id SERIAL PRIMARY KEY,
    config_key VARCHAR(100) UNIQUE NOT NULL,
    config_value TEXT NOT NULL,
    description TEXT NULL,
    updated_by_id INTEGER NULL,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_app_config_updated_by 
        FOREIGN KEY (updated_by_id) REFERENCES admin_users(id) ON DELETE SET NULL
);

CREATE INDEX idx_app_config_key ON app_config(config_key);

COMMENT ON TABLE app_config IS 'System configuration key-value store';

-- Connectivity Log Table
CREATE TABLE connectivity_log (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NULL,
    is_online BOOLEAN NOT NULL,
    connection_type VARCHAR(50) NULL,
    latency_ms INTEGER NULL,
    error_message TEXT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_connectivity_user 
        FOREIGN KEY (user_id) REFERENCES admin_users(id) ON DELETE SET NULL
);

CREATE INDEX idx_connectivity_user ON connectivity_log(user_id);
CREATE INDEX idx_connectivity_created ON connectivity_log(created_at DESC);

COMMENT ON TABLE connectivity_log IS 'Network connectivity status tracking';

-- ============================================================================
-- 9. SEED DATA (Optional)
-- ============================================================================

-- Seed notification types
INSERT INTO notification_types (name, description, icon_name, color_hex) VALUES
('announcement', 'Department Announcements', 'campaign', '#FF9800'),
('info', 'General Information', 'info', '#1976D2'),
('emergency', 'Emergency Alerts', 'warning', '#D32F2F'),
('facility_update', 'Facility Updates', 'business', '#388E3C'),
('room_update', 'Room/Classroom Updates', 'meeting_room', '#7B1FA2'),
('system_maintenance', 'System Maintenance', 'settings', '#607D8B'),
('app_update', 'Application Updates', 'system_update', '#0097A7');

-- Seed app configuration defaults
INSERT INTO app_config (config_key, config_value, description) VALUES
('app_name', 'TechnoPath', 'Application display name'),
('campus_name', 'SEAIT', 'Campus/Institution name'),
('max_login_attempts', '5', 'Maximum failed login attempts before lockout'),
('lockout_duration_minutes', '30', 'Account lockout duration in minutes'),
('announcement_approval_required', 'true', 'Whether campus-wide announcements require approval'),
('default_notification_ttl_days', '30', 'Default notification time-to-live in days'),
('map_default_zoom', '1.0', 'Default map zoom level'),
('chatbot_offline_mode', 'true', 'Enable offline FAQ fallback mode'),
('session_timeout_minutes', '60', 'User session timeout in minutes'),
('sync_interval_seconds', '300', 'Background sync interval in seconds');

-- ============================================================================
-- 10. VIEWS (Optional - for Reporting)
-- ============================================================================

-- View: Active Facilities with Room Count
CREATE VIEW v_active_facilities AS
SELECT 
    f.id,
    f.name,
    f.code,
    f.building_code,
    d.name as department_name,
    f.total_floors,
    COUNT(r.id) as room_count,
    f.is_active
FROM facilities f
LEFT JOIN departments d ON f.department_id = d.id
LEFT JOIN rooms r ON f.id = r.facility_id AND r.is_deleted = FALSE
WHERE f.is_deleted = FALSE
GROUP BY f.id, f.name, f.code, f.building_code, d.name, f.total_floors, f.is_active;

-- View: Published Announcements with Author Info
CREATE VIEW v_published_announcements AS
SELECT 
    a.id,
    a.title,
    a.content,
    a.scope,
    a.source_label,
    a.source_color,
    a.status,
    a.created_at,
    au.display_name as author_name,
    au.department as author_department
FROM announcements a
LEFT JOIN admin_users au ON a.created_by_id = au.id
WHERE a.status = 'published' AND a.is_deleted = FALSE
ORDER BY a.created_at DESC;

-- View: User Activity Summary
CREATE VIEW v_user_activity_summary AS
SELECT 
    au.id as user_id,
    au.username,
    au.display_name,
    au.role,
    COUNT(DISTINCT a.id) as announcements_created,
    COUNT(DISTINCT al.id) as audit_entries,
    au.last_login
FROM admin_users au
LEFT JOIN announcements a ON au.id = a.created_by_id AND a.is_deleted = FALSE
LEFT JOIN admin_audit_log al ON au.id = al.admin_id
WHERE au.is_active = TRUE
GROUP BY au.id, au.username, au.display_name, au.role, au.last_login;

-- ============================================================================
-- END OF SCHEMA
-- ============================================================================
