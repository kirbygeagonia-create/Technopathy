# TechnoPath: SEAIT Guide Map and Navigation System
## Use Case Diagram (UCD)

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                                      USE CASE DIAGRAM                                                         │
│                                    TechnoPath: SEAIT Guide Map and Navigation System                                        │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘


                              ┌───────────────────┐
                              │     SUPER ADMIN   │
                              │ (Safety & Security│
                              │      Office)      │
                              └─────────┬─────────┘
                                        │
           ┌────────────────────────────┼────────────────────────────┐
           │                            │                            │
           ▼                            ▼                            ▼
┌────────────────────┐      ┌────────────────────┐      ┌────────────────────┐
│   Manage System    │      │   Approve Content  │      │  View All Analytics│
│   Configuration    │      │                    │      │                    │
│ • Manage Facilities │      │ • Approve Campus   │      │ • View Audit Logs  │
│ • Manage All Rooms │      │   Announcements    │      │ • View All Feedback│
│ • Manage Navigation│      │ • Reject with Notes│      │ • System Reports   │
│ • Manage FAQ       │      │ • Bulk Approvals   │      │ • Usage Statistics │
│ • Generate QR Codes│      │                    │      │                    │
└────────────────────┘      └────────────────────┘      └────────────────────┘
           │                            │                            │
           ▼                            ▼                            ▼
┌────────────────────┐      ┌────────────────────┐      ┌────────────────────┐
│  Manage Admin Users│      │  Send Notifications│      │  Manage Departments│
│                    │      │                    │      │                    │
│ • Create Accounts  │      │ • Campus-Wide Push │      │ • Create/Edit Depts│
│ • Assign Roles     │      │ • Emergency Alerts │      │ • Assign Heads     │
│ • Deactivate Users │      │ • Target by Dept   │      │ • Department Config│
│ • Reset Passwords  │      │ • Priority Levels  │      │                    │
└────────────────────┘      └────────────────────┘      └────────────────────┘


                              ┌───────────────────┐
                              │       DEAN       │
                              │  (College Dean)   │
                              └─────────┬─────────┘
                                        │
                    ┌───────────────────┼───────────────────┐
                    │                   │                   │
                    ▼                   ▼                   ▼
         ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
         │ Post Department  │  │ View Dept Data   │  │  Manage Own Dept │
         │ Announcements    │  │                  │  │    Rooms         │
         │                  │  │ • View Feedback  │  │                  │
         │ • Direct Publish │  │ • View Audit Log │  │ • CRUD Operations│
         │ (Dept Scope)     │  │   (Dept Only)    │  │ • Room Assignment│
         │ • Campus-Wide    │  │                  │  │ • Room Activation│
         │   (Needs Appr)   │  │                  │  │                  │
         └──────────────────┘  └──────────────────┘  └──────────────────┘


          ┌───────────────────┐               ┌───────────────────┐
          │  PROGRAM HEAD     │               │ BASIC ED HEAD     │
          │                   │               │                   │
          └─────────┬─────────┘               └─────────┬─────────┘
                    │                                   │
                    ▼                                   ▼
         ┌──────────────────┐               ┌──────────────────┐
         │ Post Dept Rooms  │               │ Post Dept Rooms  │
         │ Announcements    │               │ Announcements    │
         │                  │               │                  │
         │ • Requires       │               │ • Requires       │
         │   Approval       │               │   Approval       │
         │ • Dept-Scoped    │               │ • Dept-Scoped    │
         └──────────────────┘               └──────────────────┘
                    │                                   │
                    ▼                                   ▼
         ┌──────────────────┐               ┌──────────────────┐
         │ Manage Own Dept   │               │ Manage Own Dept  │
         │ Rooms (Limited)   │               │ Rooms (Limited)  │
         └──────────────────┘               └──────────────────┘


                    ┌───────────────────────────────────────────┐
                    │                GUEST USER                   │
                    │     (Students, Visitors, Faculty)         │
                    └─────────────────────┬─────────────────────┘
                                          │
     ┌────────────────────────────────────┼────────────────────────────────────┐
     │                                    │                                    │
     ▼                                    ▼                                    ▼
┌──────────────────┐            ┌──────────────────┐            ┌──────────────────┐
│   Campus Map     │            │   Navigate       │            │   Search &       │
│   Interaction    │            │   Campus         │            │   Discovery      │
│                  │            │                  │            │                  │
│ • View Campus    │            │ • Set Start      │            │ • Search         │
│   Map            │            │   Point          │            │   Locations      │
│ • View Markers   │            │ • Set            │            │ • Filter         │
│ • Zoom & Pan     │            │   Destination    │            │   Results        │
│ • QR Code Scan   │            │ • Get Route      │            │ • Recent         │
│ • View Building  │            │ • Turn-by-Turn   │            │   Searches       │
│   Info           │            │   Directions     │            │ • Auto-complete  │
└────────┬─────────┘            └────────┬─────────┘            └────────┬─────────┘
         │                              │                              │
         └──────────────────────────────┼──────────────────────────────┘
                                        │
                                        ▼
                           ┌──────────────────────────┐
                           │      AI Chatbot          │
                           │                          │
                           │ • Ask Questions          │
                           │ • Get Location Info      │
                           │ • Offline FAQ Mode       │
                           │ • Online AI Mode         │
                           └────────────┬─────────────┘
                                        │
         ┌──────────────────────────────┼──────────────────────────────┐
         │                              │                              │
         ▼                              ▼                              ▼
┌──────────────────┐            ┌──────────────────┐            ┌──────────────────┐
│ Notifications    │            │  Information     │            │  User Engagement │
│                  │            │  Center          │            │                  │
│ • View Campus    │            │                  │            │ • Rate App       │
│   Announcements  │            │ • Building       │            │ • Submit         │
│ • Read Dept      │            │   Information    │            │   Feedback       │
│   Notices        │            │ • Room Details   │            │ • Add Favorites  │
│ • Emergency      │            │ • Instructor     │            │ • Manage Profile │
│   Alerts         │            │   Directory      │            │ • App Settings   │
│ • Mark as Read   │            │ • Employee List  │            │ • Accessibility  │
└──────────────────┘            └──────────────────┘            └──────────────────┘


═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
                                                  USE CASE RELATIONSHIPS & EXTENSIONS
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                                    INCLUDE RELATIONSHIPS                                                    │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                             │
│   UC: Navigate Campus                                                                                                        │
│   ├─ <<include>> View Campus Map                                                                                            │
│   ├─ <<include>> Search & Discovery                                                                                         │
│   └─ <<include>> Get Route                                                                                                  │
│                                                                                                                             │
│   UC: Post Announcement                                                                                                     │
│   ├─ <<include>> Authentication (all admin roles)                                                                            │
│   └─ <<extend>>  Approve Content (for campus-wide or non-super-admin posts)                                                 │
│                                                                                                                             │
│   UC: Send Notification                                                                                                     │
│   ├─ <<include>> Authentication                                                                                              │
│   └─ <<include>> Create Announcement (optional link)                                                                        │
│                                                                                                                             │
│   UC: Manage Rooms                                                                                                          │
│   ├─ <<include>> View Facility Data                                                                                        │
│   └─ <<include>> Authentication                                                                                              │
│                                                                                                                             │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                                    EXTEND RELATIONSHIPS                                                     │
├─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                             │
│   UC: View Campus Map                                                                                                        │
│   └─ <<extend>> Scan QR Code (when QR is available)                                                                          │
│                                                                                                                             │
│   UC: Post Announcement                                                                                                       │
│   └─ <<extend>> Approve Content [when requires_approval = true]                                                              │
│       ┌─ Condition: Campus-wide scope by non-Super Admin                                                                    │
│       └─ Condition: Any post by Program Head or Basic Ed Head                                                               │
│                                                                                                                             │
│   UC: Submit Feedback                                                                                                       │
│   └─ <<extend>> Flag Feedback [when inappropriate]                                                                           │
│       └─ Performed by: Super Admin or Dean                                                                                    │
│                                                                                                                             │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
                                                       ACTOR HIERARCHY
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

                        ┌───────────────────────┐
                        │      <<actor>>         │
                        │     AdminUser         │
                        │   (Abstract Base)     │
                        └───────────┬───────────┘
                                    │
            ┌───────────────────────┼───────────────────────┐
            │                       │                       │
            ▼                       ▼                       ▼
   ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
   │   <<actor>>     │     │   <<actor>>     │     │   <<actor>>     │
   │   SuperAdmin    │     │     Dean        │     │ DepartmentHead  │
   │                 │     │                 │     │   (Abstract)    │
   │ Safety &        │     │ College Dean    │     │                 │
   │ Security Office │     │                 │     └────────┬────────┘
   └─────────────────┘     └─────────────────┘              │
                                                              │
                                          ┌───────────────────┴───────────────────┐
                                          │                                       │
                                          ▼                                       ▼
                                 ┌─────────────────┐                     ┌─────────────────┐
                                 │   <<actor>>     │                     │   <<actor>>     │
                                 │  ProgramHead    │                     │  BasicEdHead    │
                                 │                 │                     │                 │
                                 │ College Program │                     │ Basic Education │
                                 │     Head        │                     │     Head        │
                                 └─────────────────┘                     └─────────────────┘

                                          ┌─────────────────────────────────────┐
                                          │         <<actor>>                   │
                                          │         GuestUser                   │
                                          │   (Students, Visitors, Faculty)     │
                                          └─────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
                                                    ACTOR DESCRIPTIONS
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

┌────────────────────┬────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ ACTOR              │ DESCRIPTION & RESPONSIBILITIES                                                                        │
├────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ SUPER ADMIN        │ Safety and Security Office personnel with full system access. Can manage all aspects of the system       │
│                    │ including user accounts, all content, system configuration, and emergency notifications.                │
├────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ DEAN               │ College Dean with department management capabilities. Can manage their own department's rooms,          │
│                    │ post department-scoped announcements directly, and view department-specific analytics. Campus-wide      │
│                    │ announcements require Super Admin approval.                                                            │
├────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ PROGRAM HEAD       │ College Program Head with limited room management for their department only. All announcements          │
│                    │ require Super Admin approval. Cannot manage other departments' data.                                   │
├────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ BASIC ED HEAD      │ Basic Education Head with similar permissions to Program Head but for Basic Education Department.     │
│                    │ All announcements require Super Admin approval.                                                         │
├────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ GUEST USER         │ General users including students, visitors, and faculty. Can access all public-facing features        │
│                    │ including map navigation, chatbot, information center, and feedback submission. No admin access.       │
└────────────────────┴────────────────────────────────────────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
                                                    USE CASE PRIORITY MATRIX
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ PRIORITY  │ USE CASE                                    │ ACTORS                          │ STATUS                      │
├───────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ CRITICAL  │ Navigate Campus                             │ Guest                           │ Implemented                 │
│ CRITICAL  │ View Campus Map                             │ Guest                           │ Implemented                 │
│ CRITICAL  │ AI Chatbot Assistant                        │ Guest                           │ Implemented                 │
│ CRITICAL  │ View Announcements                          │ Guest, All Admins               │ Implemented                 │
│ HIGH      │ Search & Discovery                          │ Guest                           │ Implemented                 │
│ HIGH      │ Post Announcement                           │ Super Admin, Dean, Prog/Basic   │ Implemented                 │
│ HIGH      │ Manage Facilities                           │ Super Admin                     │ Implemented                 │
│ HIGH      │ Manage Rooms                                │ Super Admin, Dean (dept only)   │ Implemented                 │
│ MEDIUM    │ Approve Content                             │ Super Admin                     │ Implemented                 │
│ MEDIUM    │ Send Notifications                          │ Super Admin                     │ Implemented                 │
│ MEDIUM    │ Manage Admin Accounts                       │ Super Admin                     │ Implemented                 │
│ MEDIUM    │ Manage Navigation Graph                     │ Super Admin                     │ Implemented                 │
│ MEDIUM    │ Feedback & Ratings                          │ Guest, Super Admin              │ Implemented                 │
│ MEDIUM    │ View Audit Log                              │ Super Admin, Dean (dept only)   │ Implemented                 │
│ LOW       │ QR Code Management                          │ Super Admin                     │ Implemented                 │
│ LOW       │ Manage FAQ                                  │ Super Admin                     │ Implemented                 │
│ LOW       │ App Settings                                │ Guest                           │ Implemented                 │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘


*Document Version: 1.0*
*Generated from TechnoPath V4 Codebase Analysis*
