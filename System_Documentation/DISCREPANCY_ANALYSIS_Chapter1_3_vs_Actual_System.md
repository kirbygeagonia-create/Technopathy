# TechnoPath Documentation Discrepancy Analysis
## Chapter 1 & 3 vs. Actual System Comparison

**Date:** April 5, 2026  
**Document Analyzed:** `Technopath -Chapter 1 and Chapter 3 - Check.docx`  
**System Version:** TechnoPath V4 (version4_technopath)

---

## Executive Summary

The Chapter 1 and Chapter 3 document contains **significant discrepancies** with the actual implemented system. The document describes a different technology stack, database schema, and system architecture than what exists in the codebase. This analysis identifies all mismatches and provides recommendations for document updates.

**Severity Levels:**
- 🔴 **CRITICAL** - Major architectural differences that affect system understanding
- 🟡 **HIGH** - Important functional or structural differences
- 🟢 **MEDIUM** - Minor inconsistencies or omissions

---

## 1. TECHNOLOGY STACK DISCREPANCIES 🔴 CRITICAL

| Aspect | Document States | Actual System | Status |
|--------|-----------------|---------------|--------|
| **Frontend Framework** | Flutter (Dart) | Vue.js (JavaScript) | 🔴 CRITICAL |
| **Backend Framework** | Flask (Python) | Django (Python) | 🔴 CRITICAL |
| **Primary Database** | SQLite only | PostgreSQL (Production) / SQLite (Dev) | 🟡 HIGH |
| **ORM** | sqflite (Flutter package) | Django ORM 4.2+ | 🔴 CRITICAL |
| **Authentication** | SHA-256 password hashing | Django Auth (PBKDF2) | 🟡 HIGH |

### Impact:
- The entire development methodology section needs revision
- Technical implementation details are incorrect
- Architecture diagrams need complete redraw

---

## 2. ACTOR/ROLE DEFINITION DISCREPANCIES 🔴 CRITICAL

### Document Actors (Incorrect):
| Actor | Document Description |
|-------|---------------------|
| Student | SEAIT students who use the system |
| Faculty | SEAIT faculty members |
| Visitor | External individuals visiting campus |
| Safety and Security Office | Manages structural building data |
| Program Head | Manages department-specific data |
| Dean | Oversight authority |

### Actual System Actors (Correct):
| Actor | Role | Permissions |
|-------|------|-------------|
| **Super Admin** | Safety and Security Office | Full system access |
| **Dean** | College Dean | Department management, approval workflow |
| **Program Head** | College Program Head | Own department rooms, announcements (requires approval) |
| **Basic Ed Head** | Basic Education Head | Own department rooms, announcements (requires approval) |
| **Guest** | Students, Visitors, Faculty (consolidated) | Read-only public features |

### Key Differences:
1. 🔴 **Document separates Students/Faculty/Visitors** - System consolidates them as "Guest"
2. 🔴 **Document misses Basic Ed Head role entirely**
3. 🟡 **Document describes different permission structure**
4. 🟡 **Approval workflow not mentioned in document**

---

## 3. DATABASE SCHEMA DISCREPANCIES 🔴 CRITICAL

### 3.1 Tables in Document BUT NOT in Actual System

| Table | Document Claim | Actual Status |
|-------|----------------|---------------|
| `buildings` | Separate table for buildings | 🔴 **DOES NOT EXIST** - Facilities link directly to departments |
| `facility_images` | Image gallery table | 🔴 **DOES NOT EXIST** - Single image_path field only |
| `users` | Generic user table | 🟡 **INCORRECT** - Table is `admin_users` with role-based structure |

### 3.2 Tables in Actual System BUT NOT in Document

| Table | Purpose | Severity |
|-------|---------|----------|
| `departments` | Department registry with head assignment | 🔴 CRITICAL |
| `map_markers` | Interactive map markers | 🟡 HIGH |
| `map_labels` | Map text labels | 🟡 HIGH |
| `ratings` | App & location ratings (separate from feedback) | 🟡 HIGH |
| `feedback_flags` | Content moderation system | 🟡 HIGH |
| `notification_read_status` | Read receipts for notifications | 🟢 MEDIUM |
| `notification_preferences` | User notification settings | 🟢 MEDIUM |
| `search_history` | Search analytics | 🟢 MEDIUM |
| `app_usage` | Session tracking | 🟢 MEDIUM |
| `usage_analytics` | Event tracking | 🟢 MEDIUM |
| `app_config` | System configuration | 🟢 MEDIUM |
| `connectivity_log` | Network status tracking | 🟢 MEDIUM |
| `announcements` | Department announcements with approval workflow | 🔴 CRITICAL |

### 3.3 Field Differences

| Table | Document Field | Actual Field | Difference |
|-------|---------------|--------------|------------|
| `admin_users` | `password_hash` (SHA-256) | `password` (Django format) | 🔴 Different hashing |
| `admin_users` | `user_type` | `role` (with specific choices) | 🔴 Different structure |
| `admin_users` | Missing | `department_label`, `login_attempts`, `locked_until` | 🟡 Additional security fields |
| `ai_chat_logs` | `faq_id` | `faq_entry_id` | 🟢 Naming difference |
| `notifications` | `is_read` boolean | Separate `notification_read_status` table | 🔴 Different architecture |
| `rooms` | `facility_id` nullable | `facility_id` NOT NULL | 🔴 Document incorrect |
| All tables | `AUTOINCREMENT` | `SERIAL` / `auto_now_add` | 🟢 Implementation detail |

---

## 4. FUNCTIONAL DECOMPOSITION DIAGRAM (FDD) DISCREPANCIES 🟡 HIGH

### Document FDD Modules (Incorrect):
1. QR Code Access Point
2. Campus Navigation Guide with 2D Floor Maps
3. Building Room Maps with Highlighted Offices
4. Building Classroom and Room Updates Module
5. AI Chatbot / Virtual Guide
6. Admin Panel

### Actual System FDD Modules (Correct):

**1. Mobile User Module**
- Campus Map View (interactive 2D maps, markers, QR codes)
- Search & Discovery (search, autocomplete, recent searches)
- Navigation System (routing, turn-by-turn directions)
- AI Chatbot (online/offline modes, FAQ, quick actions)
- Notifications System (push notifications, department-scoped)
- Information Center (building, room, instructor, employee info)
- User Engagement (favorites, ratings, feedback, profile)

**2. Admin Panel Module**
- Admin Dashboard (statistics, quick actions, pending approvals)
- Map Management (facilities, rooms, navigation graph, FAQ, QR codes)
- Communications (announcements, pending approvals, notifications)
- Administration (admin accounts, feedback, audit log)

**3. System Core Module**
- Database Management (SQLite/PostgreSQL, Django ORM)
- API Services (REST endpoints)
- Sync & Offline Services (IndexedDB, background sync)
- Analytics & Reporting (search history, usage tracking)

### Key Differences:
- 🔴 Document describes features, not functional modules
- 🔴 Missing System Core Module entirely
- 🟡 Admin Panel structure is different
- 🟢 Features are similar but organized differently

---

## 5. USE CASE DIAGRAM (UCD) DISCREPANCIES 🔴 CRITICAL

### Document Use Case Matrix Issues:

1. **Actor Consolidation Problem**
   - Document lists: Student, Faculty, Visitor as separate actors
   - Actual system: Consolidated as "Guest" actor

2. **Missing Use Cases**
   - No mention of **Announcement Approval Workflow**
   - No mention of **Notification Read Status**
   - No mention of **Search History**
   - No mention of **Device Preferences**
   - No mention of **Admin Audit Log** viewing permissions by department

3. **Permission Inaccuracies**
   - Document: "Program Heads manage department-specific data"
   - Actual: Program Heads require approval for campus-wide announcements
   - Document: No mention of Basic Ed Head role
   - Actual: Basic Ed Head has same permissions as Program Head

4. **Missing Actor Generalization**
   - Document: No inheritance structure shown
   - Actual: AdminUser ← SuperAdmin, Dean, ProgramHead, BasicEdHead

---

## 6. ENTITY RELATIONSHIP DIAGRAM (ERD) DISCREPANCIES 🔴 CRITICAL

### Document Relationships (Incorrect/Missing):

| Relationship | Document Claim | Actual System |
|--------------|----------------|---------------|
| buildings → facilities | 1:N | 🔴 **NO buildings table** - facilities link to departments |
| facilities → facility_images | 1:N | 🔴 **NO facility_images table** |
| users → admin_audit_log | 1:N | 🟡 **Table is admin_users** |
| departments → facilities | Not shown | 🔴 **1:N relationship exists** |
| admin_users → departments (head) | Not shown | 🔴 **1:N relationship exists** |
| rooms → ratings | Not shown | 🔴 **1:N relationship exists** |
| facilities → ratings | Not shown | 🔴 **1:N relationship exists** |
| notifications → notification_read_status | Not shown | 🔴 **1:N relationship exists** |
| announcements → notifications | Not shown | 🔴 **1:1 relationship exists** |

### Missing Relationship Categories in Document:
1. **Department Management** relationships
2. **Map Visualization** relationships (markers, labels)
3. **Content Moderation** relationships (feedback_flags)
4. **Notification System** relationships (read_status, preferences)
5. **Analytics** relationships (search_history, usage_analytics)

---

## 7. FEATURE SCOPE DISCREPANCIES

### Features in Document BUT NOT in Actual System:

| Feature | Document Section | Actual Status |
|---------|-----------------|---------------|
| `buildings` as separate entity | Database Design | 🔴 Not implemented |
| `facility_images` gallery | Database Design | 🔴 Not implemented |
| `users` generic table | Data Dictionary | 🔴 Different structure |
| SHA-256 password hashing | Data Dictionary | 🔴 Django PBKDF2 used |
| Student/Faculty/Visitor as separate actors | Use Case Matrix | 🔴 Consolidated as Guest |

### Features in Actual System BUT NOT in Document:

| Feature | Severity | Description |
|---------|----------|-------------|
| **Announcement Approval Workflow** | 🔴 CRITICAL | Campus-wide announcements require approval |
| **Department Management** | 🔴 CRITICAL | Departments table with head assignment |
| **Basic Ed Head Role** | 🔴 CRITICAL | Missing actor entirely |
| **Map Markers System** | 🟡 HIGH | Interactive marker management |
| **Map Labels System** | 🟡 HIGH | Text label management |
| **Ratings System** | 🟡 HIGH | Separate from feedback |
| **Content Moderation** | 🟡 HIGH | feedback_flags table |
| **Notification Read Tracking** | 🟢 MEDIUM | Who read what notification |
| **Search Analytics** | 🟢 MEDIUM | search_history, app_usage, usage_analytics |
| **Device Preferences** | 🟢 MEDIUM | User settings per device |
| **Connectivity Logging** | 🟢 MEDIUM | Network status tracking |
| **App Configuration** | 🟢 MEDIUM | System-wide config |

---

## 8. CORRECTIONS NEEDED - PRIORITIZED LIST

### 🔴 CRITICAL (Must Fix Before Defense)

1. **Technology Stack Correction**
   - Change: Flutter → Vue.js
   - Change: Flask → Django
   - Change: SHA-256 → Django Auth
   - Add: PostgreSQL as production database

2. **Actor/Role Correction**
   - Consolidate Student/Faculty/Visitor → Guest
   - Add Basic Ed Head role
   - Document approval workflow properly

3. **Database Schema Correction**
   - Remove `buildings` table references
   - Remove `facility_images` table references
   - Add missing tables (departments, announcements, etc.)
   - Correct `admin_users` structure

4. **FDD Redesign**
   - Reorganize into 3 main modules
   - Add System Core Module
   - Correct sub-module structure

5. **UCD Redesign**
   - Fix actor hierarchy with generalization
   - Add missing use cases
   - Correct permission mappings

### 🟡 HIGH (Should Fix)

6. **ERD Update**
   - Add all 25+ tables
   - Correct all relationships
   - Show proper cardinalities

7. **Data Dictionary Update**
   - Update all table definitions
   - Correct field names and types
   - Add missing tables

8. **Storyboard Update**
   - Align with actual Vue.js UI components
   - Add missing screens (Announcements, etc.)

### 🟢 MEDIUM (Nice to Have)

9. **Additional Features Documentation**
   - Search analytics
   - Device preferences
   - Connectivity logging
   - Content moderation

10. **API Documentation**
    - REST endpoints (not mentioned in doc)

---

## 9. RECOMMENDED DOCUMENT REVISION STRATEGY

### Phase 1: Critical Fixes (Priority)
1. Update Chapter 3 Technology Stack section
2. Correct all actor/role descriptions
3. Fix database schema sections
4. Redraw FDD and UCD diagrams

### Phase 2: High Priority Fixes
5. Update ERD with correct relationships
6. Revise Data Dictionary
7. Update Storyboard screens

### Phase 3: Enhancement
8. Add missing feature descriptions
9. Document API layer
10. Add deployment architecture

---

## 10. SUPPORTING DOCUMENTATION AVAILABLE

The following corrected documentation exists in `System_Documentation/` folder:

| Document | Status | Purpose |
|----------|--------|---------|
| `FDD_Functional_Design_Document.md` | ✅ Complete | Correct functional decomposition |
| `UCD_Use_Case_Diagram.md` | ✅ Complete | Correct use cases with proper actors |
| `ERD_Entity_Relationship_Diagram.md` | ✅ Complete | All 25+ tables with relationships |
| `Database_Design.md` | ✅ Complete | SQL schema, constraints, indexes |
| `Data_Dictionary.md` | ✅ Complete | All table/column definitions |
| `Storyboarding_Desktop_Mobile_Views.md` | ✅ Complete | Screen mockups |
| `technopath_database_schema.sql` | ✅ Complete | Full PostgreSQL schema |

---

## Conclusion

The Chapter 1 & 3 document requires **significant revisions** to align with the actual implemented system. The most critical issues are:

1. Wrong technology stack (Flutter vs Vue.js)
2. Wrong backend framework (Flask vs Django)
3. Incomplete and incorrect database schema
4. Wrong actor definitions
5. Missing major features (announcements workflow, departments, etc.)

**Recommendation:** Use the corrected documentation in the `System_Documentation/` folder as the source of truth for thesis defense.

---

*Analysis completed: April 5, 2026*
