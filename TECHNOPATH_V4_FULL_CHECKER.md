# TechnoPath Admin — Full Implementation Checker
# Version: CHECKER-V1
# Purpose: Verify every item specified in PROMPT_TECHNOPATH_ADMIN V4 is actually implemented.
# Run this AFTER V4 has been applied. Report PASS / FAIL / MISSING for every item.

---

## HOW TO USE THIS CHECKER

Read this entire document first.
For every CHECK block, inspect the actual file on disk before reporting.
Do NOT assume anything is done — open and read each file.
Report results in this format at the end:

```
[PASS]    Item was found exactly as specified
[FAIL]    Item exists but is wrong, incomplete, or different from spec
[MISSING] Item does not exist at all
```

Produce a final summary table at the very end.

---

## PART A — DJANGO BACKEND CHECKS

### A1 — AdminUser model (`backend_django/apps/users/models.py`)

Open and read the file. Verify ALL of the following:

**A1.1 — ROLE_CHOICES has exactly 4 roles**
Expected:
```python
ROLE_CHOICES = [
    ('super_admin',   'Safety and Security Office'),
    ('dean',          'College Dean'),
    ('program_head',  'College Program Head'),
    ('basic_ed_head', 'Basic Education Head'),
]
```
CHECK: Is `super_admin` labeled as 'Safety and Security Office' (NOT 'Super Admin')?
CHECK: Are all 4 roles present with those exact display names?

**A1.2 — DEPARTMENT_CHOICES has exactly 11 departments**
Expected departments in order:
1. `safety_security`          → Safety and Security Office
2. `office_of_the_dean`       → Office of the Dean
3. `college_agriculture`      → College of Agriculture and Fisheries
4. `college_criminology`      → College of Criminal Justice Education
5. `college_business`         → College of Business and Good Governance
6. `college_ict`              → College of Information and Communication Technology
7. `dept_civil_engineering`   → Department of Civil Engineering
8. `college_teacher_education`→ College of Teacher Education
9. `tesda`                    → Technical Education and Skills Development Authority (TESDA)
10. `general_education`        → General Education Department
11. `basic_education`          → Basic Education Department

CHECK: Are all 11 present? Any extra or missing?

**A1.3 — DEPARTMENT_COLORS dict has all 11 departments**
Expected mapping:
```python
'safety_security':          'red'
'office_of_the_dean':       'dark_blue'
'college_agriculture':      'green'
'college_criminology':      'charcoal'
'college_business':         'purple'
'college_ict':              'teal'
'dept_civil_engineering':   'amber'
'college_teacher_education':'blue'
'tesda':                    'dark_green'
'general_education':        'indigo'
'basic_education':          'brown'
```
CHECK: Is every department mapped? Any missing or wrong color key?

**A1.4 — Model fields present**
CHECK: `username` (CharField, unique=True)
CHECK: `email` (EmailField, blank=True, null=True)
CHECK: `display_name` (CharField, max_length=200, blank=True, null=True)
CHECK: `role` (CharField, choices=ROLE_CHOICES, default='program_head')
CHECK: `department` (CharField, choices=DEPARTMENT_CHOICES, blank=True, null=True)
CHECK: `department_label` (CharField, blank=True, null=True)
CHECK: `is_active` (BooleanField, default=True)
CHECK: `login_attempts` (IntegerField, default=0)
CHECK: `locked_until` (DateTimeField, blank=True, null=True)
CHECK: `last_login` (DateTimeField, blank=True, null=True)
CHECK: `created_at` (auto_now_add=True)
CHECK: `updated_at` (auto_now=True)
CHECK: `db_table = 'admin_users'`

**A1.5 — Permission methods all present**
CHECK: `can_manage_facilities()` → returns True only for `super_admin`
CHECK: `can_manage_all_rooms()` → returns True only for `super_admin`
CHECK: `can_manage_own_rooms()` → returns True for `program_head` and `basic_ed_head`
CHECK: `can_manage_navigation()` → returns True only for `super_admin`
CHECK: `can_manage_faq()` → returns True only for `super_admin`
CHECK: `can_manage_admin_accounts()` → returns True only for `super_admin`
CHECK: `can_view_audit_log()` → returns True for `super_admin` AND `dean`
CHECK: `can_view_all_feedback()` → returns True for `super_admin` AND `dean`
CHECK: `can_approve_announcements()` → returns True for `super_admin` AND `dean`
CHECK: `can_publish_directly()` → returns True for `super_admin` AND `dean`
CHECK: `can_post_announcement()` → returns True for ALL 4 roles
CHECK: `can_send_campus_notification()` → returns True for `super_admin` AND `dean`

**A1.6 — get_permissions_dict() includes all 12 flags**
CHECK: Returns a dict with these exact keys:
`can_manage_facilities`, `can_manage_all_rooms`, `can_manage_own_rooms`,
`can_manage_navigation`, `can_manage_faq`, `can_manage_admin_accounts`,
`can_view_audit_log`, `can_view_all_feedback`, `can_approve_announcements`,
`can_publish_directly`, `can_post_announcement`, `can_send_campus_notification`

**A1.7 — Security helpers present**
CHECK: `is_locked()` — checks `locked_until` vs `timezone.now()`
CHECK: `record_failed_login()` — increments `login_attempts`, locks at 5 attempts for 30 min
CHECK: `record_successful_login()` — resets attempts, clears lock, sets `last_login`

---

### A2 — Announcement model (`backend_django/apps/announcements/models.py`)

**A2.1 — STATUS_CHOICES**
CHECK: Has exactly: `pending_approval`, `published`, `rejected`, `archived`

**A2.2 — SCOPE_CHOICES**
CHECK: Has exactly: `campus_wide`, `all_college`, `basic_ed_only`, `department`

**A2.3 — Fields**
CHECK: `title`, `content`, `created_by` (FK to AdminUser, SET_NULL)
CHECK: `source_label` (CharField, max_length=200)
CHECK: `source_color` (CharField, default='orange')
CHECK: `scope` (CharField, choices=SCOPE_CHOICES, default='campus_wide')
CHECK: `target_department` (CharField, blank=True, null=True)
CHECK: `status` (CharField, choices=STATUS_CHOICES, default='pending_approval')
CHECK: `requires_approval` (BooleanField, default=True)
CHECK: `approved_by` (FK to AdminUser, null=True, blank=True)
CHECK: `rejected_by` (FK to AdminUser, null=True, blank=True)
CHECK: `rejection_note` (TextField, blank=True, null=True)
CHECK: `approved_at` (DateTimeField, blank=True, null=True)
CHECK: `is_deleted` (BooleanField, default=False)
CHECK: `created_at` (auto_now_add), `updated_at` (auto_now)
CHECK: `db_table = 'announcements'`

**A2.4 — Methods**
CHECK: `publish(approved_by_user)` — sets status='published', sets approved_by/at, creates Notification
CHECK: `reject(rejected_by_user, note='')` — sets status='rejected', sets rejected_by, rejection_note

---

### A3 — Notification model (`backend_django/apps/notifications/models.py`)

CHECK: `source_label` field exists (CharField, blank=True, default='')
CHECK: `source_color` field exists (CharField, default='orange')
CHECK: `announcement` FK exists (to Announcement, null=True, blank=True, SET_NULL)
CHECK: `priority` IntegerField with choices (1–4)
CHECK: `is_read` BooleanField
CHECK: `expires_at` DateTimeField (nullable)
CHECK: `created_by` FK to AdminUser (nullable)
CHECK: `db_table = 'notifications'`

---

### A4 — AdminAuditLog model

CHECK: Model exists (in `apps/facilities/models.py` or its own file)
CHECK: `db_table = 'admin_audit_log'`
CHECK: `admin` FK to AdminUser (SET_NULL, null=True)
CHECK: `action` CharField with these ACTION_CHOICES:
  `login`, `logout`, `create`, `update`, `soft_delete`,
  `restore`, `approve`, `reject`, `publish`, `reset_password`
CHECK: `entity_type` (CharField, blank=True, null=True)
CHECK: `entity_id` (IntegerField, blank=True, null=True)
CHECK: `entity_label` (CharField, blank=True, null=True)
CHECK: `old_value_json` (TextField, blank=True, null=True)
CHECK: `new_value_json` (TextField, blank=True, null=True)
CHECK: `ip_address` (CharField, blank=True, null=True)
CHECK: `created_at` (auto_now_add=True)

---

### A5 — Permissions file (`backend_django/apps/users/permissions.py`)

CHECK: `IsSuperAdmin` — allows only `role == 'super_admin'`
CHECK: `IsDeanOrSuperAdmin` — allows `super_admin` or `dean`
CHECK: `CanApproveAnnouncements` — delegates to `can_approve_announcements()`
CHECK: `CanPostAnnouncement` — delegates to `can_post_announcement()`
CHECK: `IsAnyAdmin` — allows all 4 roles

---

### A6 — Views (`backend_django/apps/users/views.py`)

**A6.1 — write_audit() helper**
CHECK: Function exists at module level
CHECK: Catches all exceptions (never crashes main request)
CHECK: Extracts IP from `HTTP_X_FORWARDED_FOR` or `REMOTE_ADDR`
CHECK: Imports AdminAuditLog inside the function (avoids circular import)

**A6.2 — LoginView**
CHECK: `permission_classes = []` (public endpoint)
CHECK: Validates username + password not empty
CHECK: Returns 401 for wrong credentials
CHECK: Returns 403 for locked accounts with remaining minutes
CHECK: Calls `record_failed_login()` on wrong password, shows remaining attempts
CHECK: Calls `record_successful_login()` on success
CHECK: Calls `write_audit(..., 'login', ...)` on success
CHECK: Returns JWT `access` + `refresh` tokens
CHECK: Returns full user object with ALL `can_*` flags flattened into response

**A6.3 — LogoutView**
CHECK: `permission_classes = [IsAuthenticated]`
CHECK: Calls `write_audit(..., 'logout', ...)`

**A6.4 — MeView**
CHECK: Returns same user structure as login (id, username, display_name, role,
       role_label, department, department_label, department_color + all can_* flags)

**A6.5 — AdminListCreateView**
CHECK: `permission_classes = [IsSuperAdmin]`
CHECK: GET returns list of active admins with id, username, display_name, role,
       role_label, department, department_label, last_login, created_at
CHECK: POST creates user, calls write_audit with action='create'

**A6.6 — AdminDetailView**
CHECK: `permission_classes = [IsSuperAdmin]`
CHECK: PUT updates display_name, role, department, department_label, email
CHECK: PUT handles optional password reset, logs 'reset_password' separately
CHECK: DELETE sets `is_active = False` (soft delete — never calls `.delete()`)
CHECK: DELETE refuses to deactivate `super_admin` account (returns 403)
CHECK: Both PUT and DELETE call write_audit

**A6.7 — AuditLogView**
CHECK: Checks `can_view_audit_log()` — accessible by super_admin AND dean
CHECK: Supports `entity_type` and `action` query params for filtering
CHECK: Returns last 300 entries
CHECK: Returned rows include: id, admin name, department, action,
       entity_type, entity_id, entity_label, ip_address, created_at

---

### A7 — Announcement views (`backend_django/apps/announcements/views.py`)

**A7.1 — AnnouncementPublicListView**
CHECK: `permission_classes = []` (public, no auth required)
CHECK: Only returns `status='published'` and `is_deleted=False`
CHECK: Returns: id, title, content, source_label, source_color, scope, approved_at, created_at

**A7.2 — AnnouncementCreateView**
CHECK: `permission_classes = [CanPostAnnouncement]`
CHECK: If `can_publish_directly()` → sets status='published', calls `a.publish()`, logs 'publish'
CHECK: If NOT `can_publish_directly()` → sets status='pending_approval', logs 'create'
CHECK: `source_label` and `source_color` are pulled from the creating user's department

**A7.3 — AnnouncementDetailView (PUT/DELETE)**
CHECK: PUT — only creator OR super_admin can edit
CHECK: PUT — published announcements can only be edited by super_admin
CHECK: DELETE — sets `is_deleted = True` (soft delete)
CHECK: Both call write_audit

**A7.4 — AnnouncementApproveView**
CHECK: `permission_classes = [CanApproveAnnouncements]` (dean + super_admin)
CHECK: Calls `a.publish(approved_by_user=request.user)`
CHECK: Returns 400 if status is not 'pending_approval'
CHECK: Calls write_audit with action='approve'

**A7.5 — AnnouncementRejectView**
CHECK: `permission_classes = [CanApproveAnnouncements]`
CHECK: Accepts optional `note` from request.data
CHECK: Calls `a.reject(rejected_by_user, note=...)`
CHECK: Calls write_audit with action='reject'

**A7.6 — PendingApprovalsView**
CHECK: `permission_classes = [CanApproveAnnouncements]`
CHECK: Returns all `status='pending_approval'` and `is_deleted=False`
CHECK: Returns: id, title, content, source_label, source_color, scope,
       created_by name, department, created_at

**A7.7 — MyAnnouncementsView**
CHECK: `permission_classes = [IsAuthenticated]`
CHECK: Filters by `created_by=request.user`
CHECK: Returns: id, title, content, status, scope, rejection_note, created_at

---

### A8 — URL routing

**A8.1 — users/urls.py**
CHECK: `login/`           → LoginView
CHECK: `logout/`          → LogoutView
CHECK: `me/`              → MeView
CHECK: `admins/`          → AdminListCreateView
CHECK: `admins/<int:pk>/` → AdminDetailView
CHECK: `audit-log/`       → AuditLogView

**A8.2 — announcements/urls.py**
CHECK: `` (empty)             → AnnouncementPublicListView (GET)
CHECK: `create/`              → AnnouncementCreateView (POST)
CHECK: `<int:pk>/`            → AnnouncementDetailView (PUT/DELETE)
CHECK: `<int:pk>/approve/`    → AnnouncementApproveView (POST)
CHECK: `<int:pk>/reject/`     → AnnouncementRejectView (POST)
CHECK: `pending/`             → PendingApprovalsView (GET)
CHECK: `mine/`                → MyAnnouncementsView (GET)

---

### A9 — Seed command (`backend_django/apps/users/management/commands/seed_admins.py`)

CHECK: File exists at correct path (including `__init__.py` in management/ and commands/)

**A9.1 — Super Admin account**
CHECK: username=`safety_admin`, role=`super_admin`, department=`safety_security`
CHECK: display_name=`Safety and Security Office`
CHECK: `is_superuser=True`

**A9.2 — Dean account**
CHECK: username=`dean_seait`, role=`dean`, department=`office_of_the_dean`
CHECK: display_name=`Office of the Dean`

**A9.3 — Program Head accounts (8 required)**
Verify ALL 8 are present:
1. `head_agriculture`  → department=`college_agriculture`
2. `head_criminology`  → department=`college_criminology`
3. `head_business`     → department=`college_business`
4. `head_ict`          → department=`college_ict`
5. `head_civil_eng`    → department=`dept_civil_engineering`
6. `head_teacher_ed`   → department=`college_teacher_education`
7. `head_tesda`        → department=`tesda`
8. `head_gen_ed`       → department=`general_education`

**A9.4 — Basic Education Head account**
CHECK: username=`head_basic_ed`, role=`basic_ed_head`, department=`basic_education`
CHECK: display_name covers Elem + JHS + SHS

**A9.5 — Seed command behavior**
CHECK: Does NOT re-create existing accounts (checks `if not exists`)
CHECK: Uses `create_user()` (not `create()`) so passwords are hashed

**TOTAL EXPECTED ACCOUNTS: 11**
(1 super_admin + 1 dean + 8 program_heads + 1 basic_ed_head)

---

### A10 — Database tables

Run this check script:
```bash
cd backend_django
python -c "
import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'technopath.settings')
django.setup()
from django.db import connection
tables = connection.introspection.table_names()
required = [
    'admin_users',
    'announcements',
    'notifications',
    'facilities',
    'rooms',
    'navigation_nodes',
    'navigation_edges',
    'faq_entries',
    'feedback',
    'ai_chat_logs',
    'admin_audit_log',
]
for t in required:
    status = 'PASS' if t in tables else 'MISSING'
    print(f'  [{status}] {t}')
"
```

CHECK: All 11 tables exist. Any MISSING table must be created via migration.

---

### A11 — Migrations

```bash
cd backend_django
python manage.py showmigrations
```

CHECK: All apps show `[X]` on their latest migration (no unapplied migrations)
CHECK: `python manage.py check` produces no errors

---

### A12 — Seeded accounts in database

```bash
cd backend_django
python -c "
import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'technopath.settings')
django.setup()
from apps.users.models import AdminUser

print('=== ACCOUNT AUDIT ===')

# Check super_admin
sa = AdminUser.objects.filter(role='super_admin', is_active=True)
print(f'super_admin accounts: {sa.count()} (expected: 1)')
for u in sa:
    print(f'  username={u.username}  dept={u.department}  display={u.display_name}  superuser={u.is_superuser}')

# Check dean
dean = AdminUser.objects.filter(role='dean', is_active=True)
print(f'dean accounts: {dean.count()} (expected: 1)')
for u in dean:
    print(f'  username={u.username}  dept={u.department}')

# Check program_heads
ph = AdminUser.objects.filter(role='program_head', is_active=True)
print(f'program_head accounts: {ph.count()} (expected: 8)')
for u in ph.order_by('department'):
    print(f'  username={u.username}  dept={u.department}')

# Check basic_ed_head
beh = AdminUser.objects.filter(role='basic_ed_head', is_active=True)
print(f'basic_ed_head accounts: {beh.count()} (expected: 1)')
for u in beh:
    print(f'  username={u.username}  dept={u.department}')

# Check no program_head for basic_education (must be basic_ed_head)
wrong = AdminUser.objects.filter(role='program_head', department='basic_education')
if wrong.exists():
    print('ERROR: basic_education must use role=basic_ed_head, not program_head!')
"
```

---

### A13 — Permission flag correctness

```bash
cd backend_django
python -c "
import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'technopath.settings')
django.setup()
from apps.users.models import AdminUser

print('=== PERMISSION MATRIX CHECK ===')

checks = [
    ('super_admin', {
        'can_manage_facilities': True,
        'can_manage_all_rooms': True,
        'can_manage_own_rooms': True,
        'can_manage_navigation': True,
        'can_manage_faq': True,
        'can_manage_admin_accounts': True,
        'can_view_audit_log': True,
        'can_view_all_feedback': True,
        'can_approve_announcements': True,
        'can_publish_directly': True,
        'can_post_announcement': True,
        'can_send_campus_notification': True,
    }),
    ('dean', {
        'can_manage_facilities': False,
        'can_manage_all_rooms': False,
        'can_manage_own_rooms': False,
        'can_manage_navigation': False,
        'can_manage_faq': False,
        'can_manage_admin_accounts': False,
        'can_view_audit_log': True,
        'can_view_all_feedback': True,
        'can_approve_announcements': True,
        'can_publish_directly': True,
        'can_post_announcement': True,
        'can_send_campus_notification': True,
    }),
    ('program_head', {
        'can_manage_facilities': False,
        'can_manage_all_rooms': False,
        'can_manage_own_rooms': True,
        'can_manage_navigation': False,
        'can_manage_faq': False,
        'can_manage_admin_accounts': False,
        'can_view_audit_log': False,
        'can_view_all_feedback': False,
        'can_approve_announcements': False,
        'can_publish_directly': False,
        'can_post_announcement': True,
        'can_send_campus_notification': False,
    }),
    ('basic_ed_head', {
        'can_manage_facilities': False,
        'can_manage_all_rooms': False,
        'can_manage_own_rooms': True,
        'can_manage_navigation': False,
        'can_manage_faq': False,
        'can_manage_admin_accounts': False,
        'can_view_audit_log': False,
        'can_view_all_feedback': False,
        'can_approve_announcements': False,
        'can_publish_directly': False,
        'can_post_announcement': True,
        'can_send_campus_notification': False,
    }),
]

all_pass = True
for role, expected in checks:
    user = AdminUser.objects.filter(role=role, is_active=True).first()
    if not user:
        print(f'  [MISSING] No active {role} account found')
        all_pass = False
        continue
    perms = user.get_permissions_dict()
    role_pass = True
    for perm, val in expected.items():
        actual = perms.get(perm)
        if actual != val:
            print(f'  [FAIL] {role}.{perm}: expected={val}, got={actual}')
            role_pass = False
            all_pass = False
    if role_pass:
        print(f'  [PASS] {role} — all {len(expected)} permission flags correct')

if all_pass:
    print()
    print('ALL PERMISSION CHECKS PASSED')
"
```

---

## PART B — VUE.JS FRONTEND CHECKS

### B1 — Auth store (`frontend/src/stores/authStore.js`)

CHECK: State stores `user`, `token`, `refreshToken`
CHECK: All three are initialized from localStorage on startup:
  - `tp_user` → user
  - `tp_token` → token
  - `tp_refresh` → refreshToken

CHECK: Getters expose ALL of the following:
  `isLoggedIn`, `isSuperAdmin`, `isDean`, `isProgramHead`, `isBasicEdHead`,
  `displayName`, `roleLabel`, `departmentLabel`, `departmentColor`, `department`

CHECK: Permission getters (sourced from `user.can_*` flags):
  `canManageFacilities`, `canManageAllRooms`, `canManageOwnRooms`,
  `canManageNavigation`, `canManageFAQ`, `canManageAdminAccounts`,
  `canViewAuditLog`, `canViewAllFeedback`, `canApproveAnnouncements`,
  `canPublishDirectly`, `canPostAnnouncement`, `canSendCampusNotification`

CHECK: `login()` action stores all three values in localStorage
CHECK: `logout()` action removes all three from localStorage and clears state

---

### B2 — AdminView.vue (`frontend/src/views/AdminView.vue`)

**B2.1 — Mobile block**
CHECK: `v-if="isMobile"` (window.innerWidth < 768) shows a "desktop only" message
CHECK: Message does NOT show the admin panel — just a card with explanation text

**B2.2 — Sidebar brand**
CHECK: TechnoPath logo/name visible
CHECK: "Admin Panel" subtitle visible

**B2.3 — Sidebar navigation items and v-if guards**
Verify each nav item and its exact `v-if` condition:

| Nav item           | v-if condition                                            |
|--------------------|-----------------------------------------------------------|
| Dashboard          | Always visible (no v-if, all roles)                       |
| Facilities         | `auth.canManageFacilities`                                |
| Rooms              | `auth.canManageAllRooms \|\| auth.canManageOwnRooms`      |
| Navigation Graph   | `auth.canManageNavigation`                                |
| FAQ / Chatbot      | `auth.canManageFAQ`                                       |
| Announcements      | `auth.canPostAnnouncement`                                |
| Pending Approvals  | `auth.canApproveAnnouncements`                            |
| Send Notification  | `auth.canSendCampusNotification`                          |
| Admin Accounts     | `auth.canManageAdminAccounts`                             |
| Feedback & Ratings | `auth.canViewAllFeedback`                                 |
| Audit Log          | `auth.canViewAuditLog`                                    |

CHECK: Items use `v-if`, NOT `v-show`, NOT disabled/greyed classes

**B2.4 — Pending approval badge**
CHECK: Badge with count shows next to "Pending Approvals" when `pendingCount > 0`
CHECK: Badge uses a different/urgent color (e.g. red/danger)
CHECK: Badge next to "Announcements" shows `myPendingCount` when > 0

**B2.5 — Main content area — child components**
CHECK: Each section renders a dedicated child component, NOT inline template code:
  `AdminDashboard`, `AdminFacilities`, `AdminRooms`, `AdminNavGraph`,
  `AdminFAQ`, `AdminAnnouncements`, `AdminPendingApprovals`,
  `AdminSendNotification`, `AdminAccounts`, `AdminFeedback`, `AdminAuditLog`

CHECK: All 11 components are imported at the top of the script block
CHECK: Each component is gated with both section check AND permission check, e.g.:
  `v-else-if="section === 'facilities' && auth.canManageFacilities"`

**B2.6 — Access denied fallback**
CHECK: A `v-else` block shows a "no permission" message if no section matches

**B2.7 — Sidebar footer**
CHECK: Shows `auth.displayName`
CHECK: Shows `auth.roleLabel`
CHECK: Shows `auth.departmentLabel`
CHECK: Has a logout button that calls `auth.logout()` then `router.push('/admin/login')`

**B2.8 — onMounted behavior**
CHECK: Redirects to `/admin/login` if not authenticated
CHECK: Calls `loadPendingCount()` on mount

**B2.9 — Sidebar CSS**
CHECK: Sidebar width is fixed (240px or 248px)
CHECK: Active nav item has left border accent (`border-left-color: var(--color-primary)`)
CHECK: Active nav item has background highlight
CHECK: Group labels (MAP MANAGEMENT, COMMUNICATIONS, ADMINISTRATION) are present
CHECK: All fonts use `var(--font-primary)`
CHECK: All nav buttons are `min-height: 44px`

---

### B3 — AdminAnnouncements.vue

CHECK: Fetches from GET `/announcements/mine/` on mount
CHECK: Shows a list of the admin's own announcements
CHECK: Has a "+ New Announcement" button
CHECK: Form has: Title (text input), Content (textarea), Scope (select)
CHECK: Scope options: campus_wide, all_college, basic_ed_only, department
CHECK: Submit button text changes based on `auth.canPublishDirectly`:
  - TRUE → "Publish Now"
  - FALSE → "Submit for Approval"
CHECK: Info banner explains approval workflow when user cannot publish directly
CHECK: Status badges per announcement:
  - `pending_approval` → amber/orange "Awaiting Approval"
  - `published` → green "Published"
  - `rejected` → red "Rejected"
  - `archived` → gray "Archived"
CHECK: Rejected announcements show `rejection_note` in a red callout box
CHECK: Emits `my-pending` event with count of pending announcements
CHECK: All fonts use `var(--font-primary)`, all buttons min-height 44px

---

### B4 — AdminPendingApprovals.vue

CHECK: Fetches from GET `/announcements/pending/` on mount
CHECK: Each card shows: department chip (colored), submitter name, date, title, content, scope
CHECK: Department chip uses the correct color from the department color system
CHECK: "Approve & Publish" button → POST `/announcements/<id>/approve/` → reloads list
CHECK: "Reject" button → opens dialog with optional rejection note textarea
CHECK: Reject dialog → POST `/announcements/<id>/reject/` with note
CHECK: After every approve/reject: emits `count` event with new pending count
CHECK: Empty state message when no pending items
CHECK: All fonts use `var(--font-primary)`, all buttons min-height 44px

---

### B5 — Department color display in admin panel

**B5.1 — Department color circle/avatar indicator**
CHECK: In the Admin Accounts list (`AdminAccounts.vue`), each admin account row
       shows a colored circle/dot/avatar that uses the admin's `department_color`.
       The circle should be a solid filled circle with the department's accent color.
       This visually identifies which department each admin belongs to at a glance.

Expected implementation pattern:
```vue
<span
  class="dept-color-dot"
  :style="{ background: deptColorMap[admin.department] }"
  :title="admin.department_label"
/>
```
Or as an outlined circle with colored border:
```vue
<span
  class="dept-color-ring"
  :style="{ borderColor: deptColorMap[admin.department] }"
/>
```

The color map in the component must match:
```javascript
const deptColorMap = {
  safety_security:          '#B71C1C',  // red
  office_of_the_dean:       '#1A237E',  // dark_blue
  college_agriculture:      '#1B5E20',  // green
  college_criminology:      '#263238',  // charcoal
  college_business:         '#4A148C',  // purple
  college_ict:              '#004D40',  // teal
  dept_civil_engineering:   '#E65100',  // amber
  college_teacher_education:'#0D47A1',  // blue
  tesda:                    '#33691E',  // dark_green
  general_education:        '#283593',  // indigo
  basic_education:          '#4E342E',  // brown
}
```

CHECK: The colored indicator appears in the Admin Accounts list
CHECK: The colored indicator appears in the Pending Approvals card (matches submitter's dept)
CHECK: The color matches the department color system from Part 3 of the prompt

**B5.2 — Department chip colors in notification cards (mobile)**
CHECK: In `NotificationsView.vue`, each notification shows a colored chip
CHECK: Chip uses `source_label` as text content
CHECK: Chip uses `chip-{source_color}` CSS class
CHECK: Chip is positioned above the notification title
CHECK: All chip CSS classes are present (chip-red, chip-dark_blue, chip-green, etc.)

---

### B6 — Mobile NotificationsView.vue

CHECK: Each notification item has a `source_label` chip rendered above the title
CHECK: Chip uses class pattern: `['source-chip', 'chip-' + (n.source_color || 'orange')]`
CHECK: These CSS classes exist in the component's `<style scoped>` OR in `main.css`:
  `.chip-red`, `.chip-dark_blue`, `.chip-green`, `.chip-charcoal`,
  `.chip-purple`, `.chip-teal`, `.chip-amber`, `.chip-blue`,
  `.chip-dark_green`, `.chip-indigo`, `.chip-brown`, `.chip-orange`

---

### B7 — sync.js and db.js (IndexedDB schema)

CHECK: `frontend/src/services/sync.js` — when syncing notifications, preserves
       `source_label` and `source_color` in the stored record
CHECK: `frontend/src/db.js` (or wherever Dexie is configured) — the notifications
       table schema includes `source_color`:
```javascript
notifications: '++id, type, is_read, source_color, created_at'
```

---

### B8 — CSS color system (`frontend/src/assets/main.css`)

CHECK: All 11 chip color classes are present:
```css
.chip-red        { background: #FFEBEE; color: #B71C1C; }
.chip-dark_blue  { background: #E8EAF6; color: #1A237E; }
.chip-green      { background: #E8F5E9; color: #1B5E20; }
.chip-charcoal   { background: #ECEFF1; color: #263238; }
.chip-purple     { background: #F3E5F5; color: #4A148C; }
.chip-teal       { background: #E0F2F1; color: #004D40; }
.chip-amber      { background: #FFF8E1; color: #E65100; }
.chip-blue       { background: #E3F2FD; color: #0D47A1; }
.chip-dark_green { background: #E8F5E9; color: #33691E; border: 1px solid #AED581; }
.chip-indigo     { background: #E8EAF6; color: #283593; }
.chip-brown      { background: #EFEBE9; color: #4E342E; }
.chip-orange     { background: #FFF3E0; color: #E65100; }
```

CHECK: `.source-chip` base class exists:
```css
.source-chip {
  display: inline-block;
  font-size: var(--text-xs);
  font-family: var(--font-primary);
  font-weight: 600;
  padding: 2px 8px;
  border-radius: var(--radius-full);
  margin-bottom: 4px;
}
```

---

## PART C — INSTITUTIONAL DATA CHECKS

### C1 — Academic Programs completeness

The system must know about all academic programs across all departments.
Wherever programs are listed (in the app's About, Department pages, or chatbot FAQ),
verify ALL of the following programs are present:

**College of Agriculture and Fisheries (5 programs)**
1. Bachelor of Science in Agriculture major in Animal Science
2. Bachelor of Science in Agriculture major in Crop Science
3. Bachelor of Science in Agriculture major in Horticulture
4. Bachelor of Science in Agriculture major in Plant Breeding and Genetics
5. Bachelor of Science in Fisheries

**College of Criminal Justice Education (1 program)**
1. Bachelor of Science in Criminology

**College of Business and Good Governance (6 programs)**
1. Bachelor of Public Administration
2. Bachelor of Science in Accounting Information Systems
3. Bachelor of Science in Hospitality Management
4. Bachelor of Science in Social Work
5. Bachelor of Science in Business Administration major in Marketing Management
6. Bachelor of Science in Tourism Management

**College of Information and Communication Technology (2 programs)**
1. Bachelor of Science in Information Technology
2. Bachelor of Science in Information Technology - Business Analytics

**Department of Civil Engineering (1 program)**
1. Bachelor of Science in Civil Engineering, specialized in Structural Engineering

**College of Teacher Education (9 programs)**
1. Bachelor of Secondary Education major in English
2. Bachelor of Secondary Education major in Filipino
3. Bachelor of Secondary Education major in Mathematics
4. Bachelor of Secondary Education major in Science
5. Bachelor of Secondary Education major in Social Studies
6. Bachelor of Technology and Livelihood Education major in ICT
7. Bachelor of Elementary Education
8. Bachelor of Secondary Education
9. Bachelor of Early Childhood Education

**Technical Education and Skills Development Authority / TESDA (6 programs)**
1. Cookery National Certificate II
2. Driving National Certificate II
3. Electrical Installation and Maintenance National Certificate II
4. Heavy Equipment Operation – Hydraulic Excavator National Certificate II
5. Heavy Equipment Operation – Wheel Loader National Certificate II
6. Shielded Metal Arc Welding National Certificate II

**K–12 / Basic Education (4 levels)**
1. Senior High School
2. Junior High School
3. Elementary
4. Kindergarten

CHECK: If programs are stored in the database (e.g. as FAQ entries or department data),
       count that all 30 college programs + 4 K-12 levels are present.
CHECK: If programs appear in the chatbot FAQ, verify all are listed under their
       correct department.
CHECK: If there is a seed command for FAQ/programs (`seed_faq`), verify it includes
       all of the above.

---

### C2 — Department-to-admin account mapping

Every department that has academic programs MUST have a corresponding admin account.
Run this check:

```bash
cd backend_django
python -c "
import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'technopath.settings')
django.setup()
from apps.users.models import AdminUser

REQUIRED_DEPT_ACCOUNTS = {
    'safety_security':          'super_admin',
    'office_of_the_dean':       'dean',
    'college_agriculture':      'program_head',
    'college_criminology':      'program_head',
    'college_business':         'program_head',
    'college_ict':              'program_head',
    'dept_civil_engineering':   'program_head',
    'college_teacher_education':'program_head',
    'tesda':                    'program_head',
    'general_education':        'program_head',
    'basic_education':          'basic_ed_head',
}

print('=== DEPARTMENT ACCOUNT COVERAGE ===')
all_ok = True
for dept, expected_role in REQUIRED_DEPT_ACCOUNTS.items():
    acct = AdminUser.objects.filter(
        department=dept, role=expected_role, is_active=True
    ).first()
    if acct:
        print(f'  [PASS] {dept} → {acct.username} ({acct.role})')
    else:
        print(f'  [MISSING] {dept} — no active {expected_role} account found')
        all_ok = False

if all_ok:
    print()
    print('All department accounts are present.')
"
```

---

## PART D — FULL RUN CHECKLIST

Run all of these in sequence and record the output:

```bash
cd backend_django

# D1 — Django system check (must be zero errors)
python manage.py check

# D2 — Migration status (all must be [X])
python manage.py showmigrations

# D3 — Table existence check (from A10)
python -c "
import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'technopath.settings')
django.setup()
from django.db import connection
tables = connection.introspection.table_names()
required = ['admin_users','announcements','notifications','facilities',
            'rooms','navigation_nodes','navigation_edges','faq_entries',
            'feedback','ai_chat_logs','admin_audit_log']
for t in required:
    print(f'  [{\"PASS\" if t in tables else \"MISSING\"}] {t}')
"

# D4 — Account audit (from A12)
# (paste A12 script here)

# D5 — Permission matrix (from A13)
# (paste A13 script here)

# D6 — Department coverage (from C2)
# (paste C2 script here)

# D7 — Frontend build
cd C:\Users\User\Downloads\SAD\version4_technopath\frontend
npm run build
```

---

## PART E — FINAL SUMMARY TABLE

After running all checks above, fill in this table:

```
SECTION  | CHECK                                      | RESULT
---------|--------------------------------------------|--------
A1.1     | ROLE_CHOICES — 4 roles, correct labels     |
A1.2     | DEPARTMENT_CHOICES — 11 departments        |
A1.3     | DEPARTMENT_COLORS — 11 colors mapped       |
A1.4     | AdminUser model fields complete            |
A1.5     | All 12 permission methods present          |
A1.6     | get_permissions_dict() has 12 keys         |
A1.7     | Security helpers (lock/unlock logic)       |
A2       | Announcement model complete                |
A3       | Notification model has source fields       |
A4       | AdminAuditLog model exists, 10 action types|
A5       | Permissions file — 5 classes               |
A6.1     | write_audit() helper                       |
A6.2     | LoginView — full spec                      |
A6.3     | LogoutView                                 |
A6.4     | MeView                                     |
A6.5     | AdminListCreateView                        |
A6.6     | AdminDetailView (soft delete, 403 guard)   |
A6.7     | AuditLogView (dean + super_admin)          |
A7.1     | AnnouncementPublicListView                 |
A7.2     | AnnouncementCreateView (publish vs submit) |
A7.3     | AnnouncementDetailView                     |
A7.4     | AnnouncementApproveView                    |
A7.5     | AnnouncementRejectView                     |
A7.6     | PendingApprovalsView                       |
A7.7     | MyAnnouncementsView                        |
A8.1     | users/urls.py — 6 routes                   |
A8.2     | announcements/urls.py — 7 routes           |
A9.1     | Seed: super_admin account                  |
A9.2     | Seed: dean account                         |
A9.3     | Seed: 8 program_head accounts              |
A9.4     | Seed: basic_ed_head account                |
A9.5     | Seed: idempotent (no duplicates)           |
A10      | 11 DB tables exist                         |
A11      | Migrations clean, manage.py check passes   |
A12      | 11 live accounts in DB                     |
A13      | Permission matrix 100% correct             |
B1       | authStore — 12 permission getters          |
B2.1     | AdminView mobile block                     |
B2.3     | Sidebar v-if guards correct for all items  |
B2.4     | Pending badge shows correct count          |
B2.5     | All 11 child components imported           |
B2.6     | Access denied fallback                     |
B2.7     | Footer: name, role, dept, logout           |
B2.9     | Sidebar CSS (fonts, min-height, active)    |
B3       | AdminAnnouncements full spec               |
B4       | AdminPendingApprovals full spec            |
B5.1     | Dept color circle in admin accounts list  |
B5.2     | Dept color chip in notification cards     |
B6       | Mobile NotificationsView chip display      |
B7       | sync.js + db.js source_color preserved     |
B8       | CSS chip classes all 12 present            |
C1       | All 30 programs + 4 K-12 levels present    |
C2       | All 11 department accounts covered         |
D7       | Frontend build passes                      |
```

---

## PART F — ITEMS NOT IN THE ORIGINAL PROMPT (NEW REQUIREMENTS)

The following items were NOT specified in V4 of the prompt but are required
based on the project's actual needs. Report these as MISSING unless they have
been separately implemented:

**F1 — Department color indicator in Admin Accounts list**
The Admin Accounts management screen must show a colored circle/ring next to each
admin's name. The circle color maps to their department using the exact hex values
from the department color system. This allows the Super Admin to identify department
ownership at a glance without reading the department name text.

Implementation required in `AdminAccounts.vue`:
```vue
<!-- Colored department ring beside each admin row -->
<span
  class="dept-ring"
  :style="{
    width: '12px',
    height: '12px',
    borderRadius: '50%',
    border: '2.5px solid ' + getDeptColor(admin.department),
    display: 'inline-block',
    flexShrink: 0
  }"
  :title="admin.department_label"
/>
```

Department color hex values (solid color version for dot, or border color for ring):
```javascript
function getDeptColor(dept) {
  const MAP = {
    safety_security:          '#B71C1C',
    office_of_the_dean:       '#1A237E',
    college_agriculture:      '#1B5E20',
    college_criminology:      '#263238',
    college_business:         '#4A148C',
    college_ict:              '#004D40',
    dept_civil_engineering:   '#E65100',
    college_teacher_education:'#0D47A1',
    tesda:                    '#33691E',
    general_education:        '#283593',
    basic_education:          '#4E342E',
  }
  return MAP[dept] || '#9E9E9E'
}
```

CHECK: Does `AdminAccounts.vue` show a colored ring/dot per admin row? [PASS/MISSING]

**F2 — Dean and Program Head have same announcement authority**
CLARIFICATION: The Dean (role=`dean`) and Program Heads (role=`program_head`) both
represent departments. The distinction is:
- Dean: publishes directly, approves others' submissions
- Program Heads: submit for approval, cannot publish directly

This is already in the permission matrix. Verify no code path accidentally gives
a program_head the ability to publish directly.

CHECK: No `program_head` account has `can_publish_directly = True`
CHECK: No `basic_ed_head` account has `can_publish_directly = True`

**F3 — Super Admin is specifically the Safety and Security Office**
The `super_admin` role label must display as "Safety and Security Office" in all UI,
not "Super Admin", "Administrator", or any other label.

CHECK: In `ROLE_CHOICES`: `('super_admin', 'Safety and Security Office')`
CHECK: In the admin panel sidebar footer: shows "Safety and Security Office" as role label
CHECK: In the audit log: admin's role label shows "Safety and Security Office"
CHECK: In the seed file: `display_name = 'Safety and Security Office'`

---

*TechnoPath Full Implementation Checker*
*SEAIT — South East Asian Institute of Technology, Inc.*
*Checker Version 1 — April 2026*
*Use against: PROMPT_TECHNOPATH_ADMIN V4 implementation*
