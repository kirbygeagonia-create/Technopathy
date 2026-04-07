# TechnoPath: SEAIT Guide Map and Navigation System
# WINDSURF KIMI 2.5 — DEFINITIVE ADMIN BACKEND PROMPT
# Version: V4 — Complete SEAIT Department Structure + Role-Based Admin System
# Date: April 2026
# Project: C:\Users\User\Downloads\SAD\version4_technopath\

---

## MANDATORY: READ THIS ENTIRE DOCUMENT BEFORE WRITING A SINGLE LINE OF CODE

This prompt implements the complete administrative backend for TechnoPath.
It supersedes and replaces any previous admin-related instructions.
Apply the Task Safety Protocol: inspect every file before changing it.
Never delete working code. Classify each task as COMPLETE, NEEDS REFINEMENT, or MISSING.

---

## PART 1 — SEAIT INSTITUTIONAL STRUCTURE (Reference — read before coding)

South East Asian Institute of Technology, Inc. (SEAIT) is a private
institution in Barangay Crossing Rubber, National Highway, Tupi,
South Cotabato, Philippines.

### 1A — Academic Divisions

SEAIT has two academic divisions that share a single campus:

**DIVISION A: COLLEGE (Higher Education)**

| Department Code            | Department Name                              | Programs |
|----------------------------|----------------------------------------------|----------|
| college_agriculture        | College of Agriculture and Fisheries         | 5        |
| college_criminology        | College of Criminal Justice Education        | 1        |
| college_business           | College of Business and Good Governance      | 6        |
| college_ict                | College of Information and Communication Technology | 2   |
| dept_civil_engineering     | Department of Civil Engineering              | 1        |
| college_teacher_education  | College of Teacher Education                 | 9        |
| tesda                      | Technical Education and Skills Development Authority | 6  |
| general_education          | General Education Department                 | —        |
| office_of_the_dean         | Office of the Dean                           | —        |

**DIVISION B: BASIC EDUCATION (Pre-College)**

| Department Code            | Department Name                              | Levels   |
|----------------------------|----------------------------------------------|----------|
| basic_education            | Basic Education Department                   | Elementary + JHS + SHS |

### 1B — Key decisions about the structure

**Basic Education is ONE department, ONE admin account.**
Elementary, Junior High School (Grades 7–10), and Senior High School (Grades 11–12)
are all under the same Basic Education Department and share the Basic Education Building.
They do NOT get separate accounts per grade level. The Basic Education Head account
speaks for all three levels. Individual teachers and grade coordinators are public users
with no admin access.

**TESDA gets its own Program Head-equivalent account.**
TESDA operates NC (National Certificate) programs within the campus.
It is treated as a department for announcement purposes, with the same
submission-and-approval flow as any Program Head.

**General Education gets its own Program Head account.**
GE subjects are taken by all college students. The GE department head
posts GE-specific announcements (faculty changes, GE schedule updates, etc.)

**Department of Civil Engineering gets a Program Head account.**
Having only one program does not reduce the need for departmental communications.

---

## PART 2 — ADMIN ROLE HIERARCHY

### Role definitions (5 roles, one panel, login-driven view)

```
┌─────────────────────────────────────────────────────────────────┐
│  LEVEL 1 — super_admin                                          │
│  Safety and Security Office                                     │
│  ONE account only. Full system control.                         │
│  Publishes announcements directly. No approval needed.          │
│  Approves or rejects all pending submissions.                   │
│  Manages buildings, rooms, navigation, FAQ, all admin accounts. │
├─────────────────────────────────────────────────────────────────┤
│  LEVEL 2 — dean                                                 │
│  Office of the Dean                                             │
│  ONE account. College-level oversight.                          │
│  Publishes announcements directly. No approval needed.          │
│  Can approve or reject Program Head submissions.                │
│  Cannot manage buildings, navigation, or admin accounts.        │
├─────────────────────────────────────────────────────────────────┤
│  LEVEL 3 — program_head                                         │
│  One account per college department (8 accounts total)          │
│  Colleges: Agriculture, Criminology, Business, ICT,             │
│            Civil Engineering, Teacher Education, TESDA, GE      │
│  Submits announcements for approval (cannot publish directly).  │
│  Can manage classroom assignments in own department only.       │
│  Cannot manage buildings, navigation, or other departments.     │
├─────────────────────────────────────────────────────────────────┤
│  LEVEL 4 — basic_ed_head                                        │
│  Basic Education Department Head                                │
│  ONE account covering Elementary + JHS + SHS.                   │
│  Same authority as program_head but scoped to Basic Education.  │
│  Submits announcements for approval. Cannot publish directly.   │
├─────────────────────────────────────────────────────────────────┤
│  LEVEL 5 — (no account)                                         │
│  All students, teachers, grade coordinators, visitors           │
│  They are public/guest users. Mobile app only. No admin access. │
└─────────────────────────────────────────────────────────────────┘
```

### Permission matrix

```
Permission                        | super_admin | dean | program_head | basic_ed_head
----------------------------------|-------------|------|--------------|---------------
Manage facilities (CRUD)          | ✓           | ✗    | ✗            | ✗
Manage rooms (all departments)    | ✓           | ✗    | ✗            | ✗
Manage own dept rooms only        | ✓           | ✗    | ✓            | ✓
Manage navigation graph           | ✓           | ✗    | ✗            | ✗
Manage FAQ / chatbot knowledge    | ✓           | ✗    | ✗            | ✗
Create admin accounts             | ✓           | ✗    | ✗            | ✗
Deactivate admin accounts         | ✓           | ✗    | ✗            | ✗
Reset another admin's password    | ✓           | ✗    | ✗            | ✗
View audit log                    | ✓           | ✓    | ✗            | ✗
View all feedback & ratings       | ✓           | ✓    | ✗            | ✗
View dashboard (all stats)        | ✓           | ✓    | ✗            | ✗
View dashboard (own dept only)    | ✓           | ✓    | ✓            | ✓
Publish announcement (direct)     | ✓           | ✓    | ✗            | ✗
Submit announcement (for approval)| ✓           | ✓    | ✓            | ✓
Approve/reject pending announce.  | ✓           | ✓    | ✗            | ✗
Send campus-wide notification     | ✓           | ✓    | ✗            | ✗
View own submissions only         | ✓           | ✓    | ✓            | ✓
```

### The three-tier feature visibility model

Every feature in the admin panel falls into exactly one of these three types:

**TYPE 1 — VISIBLE AND FULLY FUNCTIONAL**
The logged-in admin has full, immediate access. No approval needed.
These sections simply appear in the sidebar and work when clicked.

**TYPE 2 — VISIBLE AS "SUBMIT FOR APPROVAL"**
The admin can see and click the feature, but when they act, a dialog
clearly states: "This will be submitted to the Dean / Safety and Security
Office for approval before it goes live." The button says
"Submit for Approval", not "Save" or "Publish".
The record is saved with status `pending_approval`.
The approver sees it in their "Pending Approvals" section with a badge count.

**TYPE 3 — COMPLETELY HIDDEN**
Sections the role has no authority over do not appear in the sidebar at all.
They are not greyed out. They are not locked. They simply do not exist
in that admin's view. This prevents confusion entirely.

---

## PART 3 — DEPARTMENT COLOR SYSTEM

Each department has a designated color for its announcement labels on mobile.
These colors appear as colored chips on notification cards.

```python
DEPARTMENT_COLORS = {
    'safety_security':        'red',       # Safety and Security Office
    'office_of_the_dean':     'dark_blue', # Office of the Dean
    'college_agriculture':    'green',     # Agriculture and Fisheries
    'college_criminology':    'charcoal',  # Criminal Justice Education
    'college_business':       'purple',    # Business and Good Governance
    'college_ict':            'teal',      # Information and Communication Technology
    'dept_civil_engineering': 'amber',     # Civil Engineering
    'college_teacher_education': 'blue',   # Teacher Education
    'tesda':                  'dark_green',# TESDA
    'general_education':      'indigo',    # General Education
    'basic_education':        'brown',     # Basic Education (Elem + JHS + SHS)
}
```

CSS color values for each (add to `frontend/src/assets/main.css`):
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
```

---

## PART 4 — DJANGO BACKEND IMPLEMENTATION

Apply Task Safety Protocol. Read existing files first. Only add or fix what is needed.

### TASK 4A — Update AdminUser model

Read `backend_django/apps/users/models.py`.
If the `DEPARTMENT_CHOICES` list does not include all SEAIT departments, replace it completely.
If the model has the right structure already, only update the choices lists.

```python
# backend_django/apps/users/models.py

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from datetime import timedelta
import json


class AdminUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('Username is required')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('role', 'super_admin')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)


class AdminUser(AbstractBaseUser, PermissionsMixin):

    ROLE_CHOICES = [
        ('super_admin',   'Safety and Security Office'),
        ('dean',          'College Dean'),
        ('program_head',  'College Program Head'),
        ('basic_ed_head', 'Basic Education Head'),
    ]

    DEPARTMENT_CHOICES = [
        # ── Administrative ────────────────────────────────────
        ('safety_security',          'Safety and Security Office'),
        ('office_of_the_dean',       'Office of the Dean'),
        # ── College departments ───────────────────────────────
        ('college_agriculture',      'College of Agriculture and Fisheries'),
        ('college_criminology',      'College of Criminal Justice Education'),
        ('college_business',         'College of Business and Good Governance'),
        ('college_ict',              'College of Information and Communication Technology'),
        ('dept_civil_engineering',   'Department of Civil Engineering'),
        ('college_teacher_education','College of Teacher Education'),
        ('tesda',                    'Technical Education and Skills Development Authority (TESDA)'),
        ('general_education',        'General Education Department'),
        # ── Basic Education ───────────────────────────────────
        ('basic_education',          'Basic Education Department'),
    ]

    # Department display colors for announcement labels on mobile
    DEPARTMENT_COLORS = {
        'safety_security':          'red',
        'office_of_the_dean':       'dark_blue',
        'college_agriculture':      'green',
        'college_criminology':      'charcoal',
        'college_business':         'purple',
        'college_ict':              'teal',
        'dept_civil_engineering':   'amber',
        'college_teacher_education':'blue',
        'tesda':                    'dark_green',
        'general_education':        'indigo',
        'basic_education':          'brown',
    }

    username         = models.CharField(max_length=150, unique=True)
    email            = models.EmailField(blank=True, null=True)
    display_name     = models.CharField(
        max_length=200, blank=True, null=True,
        help_text='Full name or title shown in audit logs and admin panel'
    )
    role             = models.CharField(max_length=20, choices=ROLE_CHOICES, default='program_head')
    department       = models.CharField(
        max_length=50, choices=DEPARTMENT_CHOICES, blank=True, null=True
    )
    department_label = models.CharField(
        max_length=200, blank=True, null=True,
        help_text='Override label shown on announcements. Auto-filled from department if blank.'
    )

    is_active      = models.BooleanField(default=True)
    is_staff       = models.BooleanField(default=False)
    login_attempts = models.IntegerField(default=0)
    locked_until   = models.DateTimeField(blank=True, null=True)
    last_login     = models.DateTimeField(blank=True, null=True)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    objects = AdminUserManager()
    USERNAME_FIELD  = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'admin_users'

    # ── Label helpers ─────────────────────────────────────────

    def get_department_label(self):
        if self.department_label:
            return self.department_label
        for code, label in self.DEPARTMENT_CHOICES:
            if code == self.department:
                return label
        return self.get_role_display()

    def get_department_color(self):
        return self.DEPARTMENT_COLORS.get(self.department, 'orange')

    # ── Security helpers ──────────────────────────────────────

    def is_locked(self):
        return bool(self.locked_until and timezone.now() < self.locked_until)

    def record_failed_login(self):
        self.login_attempts += 1
        if self.login_attempts >= 5:
            self.locked_until = timezone.now() + timedelta(minutes=30)
        self.save(update_fields=['login_attempts', 'locked_until'])

    def record_successful_login(self):
        self.login_attempts = 0
        self.locked_until   = None
        self.last_login     = timezone.now()
        self.save(update_fields=['login_attempts', 'locked_until', 'last_login'])

    # ── Permission helpers (used by views AND returned to frontend) ──

    def can_manage_facilities(self):
        return self.role == 'super_admin'

    def can_manage_all_rooms(self):
        return self.role == 'super_admin'

    def can_manage_own_rooms(self):
        return self.role in ('program_head', 'basic_ed_head')

    def can_manage_navigation(self):
        return self.role == 'super_admin'

    def can_manage_faq(self):
        return self.role == 'super_admin'

    def can_manage_admin_accounts(self):
        return self.role == 'super_admin'

    def can_view_audit_log(self):
        return self.role in ('super_admin', 'dean')

    def can_view_all_feedback(self):
        return self.role in ('super_admin', 'dean')

    def can_approve_announcements(self):
        return self.role in ('super_admin', 'dean')

    def can_publish_directly(self):
        return self.role in ('super_admin', 'dean')

    def can_post_announcement(self):
        return self.role in ('super_admin', 'dean', 'program_head', 'basic_ed_head')

    def can_send_campus_notification(self):
        return self.role in ('super_admin', 'dean')

    def get_permissions_dict(self):
        """Return all permission flags as a dict for the JWT login response."""
        return {
            'can_manage_facilities':       self.can_manage_facilities(),
            'can_manage_all_rooms':        self.can_manage_all_rooms(),
            'can_manage_own_rooms':        self.can_manage_own_rooms(),
            'can_manage_navigation':       self.can_manage_navigation(),
            'can_manage_faq':              self.can_manage_faq(),
            'can_manage_admin_accounts':   self.can_manage_admin_accounts(),
            'can_view_audit_log':          self.can_view_audit_log(),
            'can_view_all_feedback':       self.can_view_all_feedback(),
            'can_approve_announcements':   self.can_approve_announcements(),
            'can_publish_directly':        self.can_publish_directly(),
            'can_post_announcement':       self.can_post_announcement(),
            'can_send_campus_notification':self.can_send_campus_notification(),
        }

    def __str__(self):
        return f'{self.display_name or self.username} — {self.get_department_label()}'
```

### TASK 4B — Announcement model

Read `backend_django/apps/announcements/models.py`.
If it does not match this spec, replace it entirely.

```python
# backend_django/apps/announcements/models.py

from django.db import models


class Announcement(models.Model):

    STATUS_CHOICES = [
        ('pending_approval', 'Pending Approval'),
        ('published',        'Published'),
        ('rejected',         'Rejected'),
        ('archived',         'Archived'),
    ]

    SCOPE_CHOICES = [
        ('campus_wide',       'Entire Campus (all users)'),
        ('all_college',       'All College Students'),
        ('basic_ed_only',     'Basic Education Only'),
        ('department',        'Specific Department Only'),
    ]

    # Content
    title             = models.CharField(max_length=200)
    content           = models.TextField()

    # Authorship
    created_by        = models.ForeignKey(
        'users.AdminUser', on_delete=models.SET_NULL,
        null=True, related_name='created_announcements'
    )

    # Label shown to mobile users — stored at creation time so it persists
    # even if the admin account is later renamed or deleted
    source_label      = models.CharField(
        max_length=200,
        help_text='Department label shown on the mobile notification card'
    )
    source_color      = models.CharField(
        max_length=20, default='orange',
        help_text='Color key for the department chip on mobile'
    )

    # Scope
    scope             = models.CharField(max_length=20, choices=SCOPE_CHOICES, default='campus_wide')
    target_department = models.CharField(
        max_length=50, blank=True, null=True,
        help_text='Set when scope=department to filter which users see this'
    )

    # Approval workflow
    status            = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending_approval')
    requires_approval = models.BooleanField(default=True)

    approved_by       = models.ForeignKey(
        'users.AdminUser', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='approved_announcements'
    )
    rejected_by       = models.ForeignKey(
        'users.AdminUser', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='rejected_announcements'
    )
    rejection_note    = models.TextField(
        blank=True, null=True,
        help_text='Reason for rejection — shown to the submitting admin'
    )
    approved_at       = models.DateTimeField(blank=True, null=True)

    # Soft delete
    is_deleted        = models.BooleanField(default=False)

    # Timestamps
    created_at        = models.DateTimeField(auto_now_add=True)
    updated_at        = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'announcements'
        ordering = ['-created_at']

    def publish(self, approved_by_user):
        """Approve and publish. Automatically creates a mobile Notification."""
        from django.utils import timezone
        from apps.notifications.models import Notification

        self.status      = 'published'
        self.approved_by = approved_by_user
        self.approved_at = timezone.now()
        self.save()

        Notification.objects.create(
            title        = self.title,
            message      = self.content,
            type         = 'announcement',
            source_label = self.source_label,
            source_color = self.source_color,
            announcement = self,
            created_by   = approved_by_user,
        )

    def reject(self, rejected_by_user, note=''):
        """Reject with optional note to the submitter."""
        self.status       = 'rejected'
        self.rejected_by  = rejected_by_user
        self.rejection_note = note
        self.save()

    def __str__(self):
        return f'[{self.status.upper()}] {self.title} — {self.source_label}'
```

### TASK 4C — Notification model (update to link announcements)

Read `backend_django/apps/notifications/models.py`.
Ensure it includes `source_label`, `source_color`, and `announcement` foreign key.

```python
# backend_django/apps/notifications/models.py

from django.db import models


class Notification(models.Model):

    TYPE_CHOICES = [
        ('announcement',        'Department Announcement'),
        ('info',                'General Info'),
        ('emergency',           'Emergency'),
        ('facility_update',     'Facility Update'),
        ('room_update',         'Room/Classroom Update'),
        ('system_maintenance',  'System Maintenance'),
        ('app_update',          'App Update'),
    ]

    title        = models.CharField(max_length=200)
    message      = models.TextField()
    type         = models.CharField(max_length=30, choices=TYPE_CHOICES, default='info')

    # Department label and color shown on mobile notification card
    source_label = models.CharField(
        max_length=200, blank=True, default='',
        help_text='Department or office name shown on the mobile card'
    )
    source_color = models.CharField(
        max_length=20, default='orange',
        help_text='Color key: red, dark_blue, green, charcoal, purple, teal, amber, blue, dark_green, indigo, brown, orange'
    )

    # Optional link back to the announcement that generated this notification
    announcement = models.ForeignKey(
        'announcements.Announcement', on_delete=models.SET_NULL,
        null=True, blank=True
    )

    priority   = models.IntegerField(
        default=1,
        choices=[(1,'Normal'), (2,'Important'), (3,'Urgent'), (4,'Emergency')]
    )
    is_read    = models.BooleanField(default=False)
    expires_at = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(
        'users.AdminUser', on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f'[{self.type}] {self.title}'
```

### TASK 4D — Audit log (in facilities/models.py, or move to its own file)

Ensure AdminAuditLog exists with these fields:

```python
class AdminAuditLog(models.Model):
    ACTION_CHOICES = [
        ('login',          'Login'),
        ('logout',         'Logout'),
        ('create',         'Create'),
        ('update',         'Update'),
        ('soft_delete',    'Soft Delete'),
        ('restore',        'Restore'),
        ('approve',        'Approve'),
        ('reject',         'Reject'),
        ('publish',        'Publish'),
        ('reset_password', 'Reset Password'),
    ]

    admin         = models.ForeignKey(
        'users.AdminUser', on_delete=models.SET_NULL,
        null=True, related_name='audit_entries'
    )
    action        = models.CharField(max_length=20, choices=ACTION_CHOICES)
    entity_type   = models.CharField(max_length=50, blank=True, null=True)
    entity_id     = models.IntegerField(blank=True, null=True)
    entity_label  = models.CharField(max_length=200, blank=True, null=True)
    old_value_json= models.TextField(blank=True, null=True)
    new_value_json= models.TextField(blank=True, null=True)
    ip_address    = models.CharField(max_length=50, blank=True, null=True)
    created_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'admin_audit_log'
        ordering = ['-created_at']
```

### TASK 4E — Permissions file

Create or replace `backend_django/apps/users/permissions.py`:

```python
from rest_framework.permissions import BasePermission


class IsSuperAdmin(BasePermission):
    message = 'Only the Safety and Security Office (Super Admin) can perform this action.'
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'super_admin'


class IsDeanOrSuperAdmin(BasePermission):
    message = 'Only the Dean or Super Admin can perform this action.'
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ('super_admin', 'dean')


class CanApproveAnnouncements(BasePermission):
    message = 'Only the Dean or Super Admin can approve announcements.'
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.can_approve_announcements()


class CanPostAnnouncement(BasePermission):
    message = 'Admin login required to post announcements.'
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.can_post_announcement()


class IsAnyAdmin(BasePermission):
    message = 'Admin login required.'
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in (
            'super_admin', 'dean', 'program_head', 'basic_ed_head'
        )
```

### TASK 4F — Login view (returns permission flags to frontend)

Replace `backend_django/apps/users/views.py` `LoginView` with this:

```python
import json
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as http_status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import AdminUser
from .permissions import IsSuperAdmin, IsAnyAdmin


def write_audit(admin, action, entity_type=None, entity_id=None,
                entity_label=None, old_val=None, new_val=None, request=None):
    """Write a row to AdminAuditLog. Import here to avoid circular imports."""
    try:
        from apps.facilities.models import AdminAuditLog
        ip = None
        if request:
            x_fwd = request.META.get('HTTP_X_FORWARDED_FOR')
            ip = x_fwd.split(',')[0].strip() if x_fwd else request.META.get('REMOTE_ADDR')
        AdminAuditLog.objects.create(
            admin=admin, action=action,
            entity_type=entity_type, entity_id=entity_id, entity_label=entity_label,
            old_value_json=json.dumps(old_val)  if old_val  else None,
            new_value_json=json.dumps(new_val)  if new_val  else None,
            ip_address=ip,
        )
    except Exception:
        pass  # Audit log failure must never crash the main request


class LoginView(APIView):
    permission_classes = []

    def post(self, request):
        username = request.data.get('username', '').strip()
        password = request.data.get('password', '')

        if not username or not password:
            return Response(
                {'error': 'Username and password are required.'},
                status=http_status.HTTP_400_BAD_REQUEST
            )

        try:
            user = AdminUser.objects.get(username=username, is_active=True)
        except AdminUser.DoesNotExist:
            return Response(
                {'error': 'Invalid username or password.'},
                status=http_status.HTTP_401_UNAUTHORIZED
            )

        if user.is_locked():
            mins = max(1, int((user.locked_until - timezone.now()).total_seconds() / 60) + 1)
            return Response(
                {'error': f'This account is temporarily locked. Try again in {mins} minute(s).'},
                status=http_status.HTTP_403_FORBIDDEN
            )

        if not user.check_password(password):
            user.record_failed_login()
            left = max(0, 5 - user.login_attempts)
            if left > 0:
                msg = f'Invalid username or password. {left} attempt(s) remaining before lockout.'
            else:
                msg = 'Account locked for 30 minutes due to too many failed attempts.'
            return Response({'error': msg}, status=http_status.HTTP_401_UNAUTHORIZED)

        user.record_successful_login()
        write_audit(user, 'login', 'user', user.id,
                    user.display_name or user.username, request=request)

        refresh = RefreshToken.for_user(user)
        return Response({
            'access':  str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id':               user.id,
                'username':         user.username,
                'display_name':     user.display_name or user.username,
                'role':             user.role,
                'role_label':       user.get_role_display(),
                'department':       user.department,
                'department_label': user.get_department_label(),
                'department_color': user.get_department_color(),
                **user.get_permissions_dict(),
            }
        })


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        write_audit(request.user, 'logout', 'user', request.user.id,
                    request.user.display_name or request.user.username, request=request)
        return Response({'message': 'Logged out.'})


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        u = request.user
        return Response({
            'id':               u.id,
            'username':         u.username,
            'display_name':     u.display_name or u.username,
            'role':             u.role,
            'role_label':       u.get_role_display(),
            'department':       u.department,
            'department_label': u.get_department_label(),
            'department_color': u.get_department_color(),
            **u.get_permissions_dict(),
        })


class AdminListCreateView(APIView):
    permission_classes = [IsSuperAdmin]

    def get(self, request):
        users = AdminUser.objects.filter(is_active=True).order_by('role', 'department')
        return Response([{
            'id':               u.id,
            'username':         u.username,
            'display_name':     u.display_name,
            'role':             u.role,
            'role_label':       u.get_role_display(),
            'department':       u.department,
            'department_label': u.get_department_label(),
            'last_login':       u.last_login,
            'created_at':       u.created_at,
        } for u in users])

    def post(self, request):
        d = request.data
        for field in ['username', 'password', 'role', 'department']:
            if not d.get(field):
                return Response({'error': f'"{field}" is required.'},
                                status=http_status.HTTP_400_BAD_REQUEST)
        if AdminUser.objects.filter(username=d['username']).exists():
            return Response({'error': 'That username already exists.'},
                            status=http_status.HTTP_400_BAD_REQUEST)
        user = AdminUser.objects.create_user(
            username      = d['username'],
            password      = d['password'],
            role          = d['role'],
            department    = d['department'],
            display_name  = d.get('display_name', ''),
            department_label = d.get('department_label', ''),
            email         = d.get('email', ''),
            is_staff      = True,
        )
        write_audit(request.user, 'create', 'admin_user', user.id, user.username,
                    new_val={'username': user.username, 'role': user.role,
                             'department': user.department}, request=request)
        return Response({'id': user.id, 'username': user.username},
                        status=http_status.HTTP_201_CREATED)


class AdminDetailView(APIView):
    permission_classes = [IsSuperAdmin]

    def put(self, request, pk):
        try:
            user = AdminUser.objects.get(pk=pk)
        except AdminUser.DoesNotExist:
            return Response({'error': 'Admin not found.'}, status=404)

        old = {'role': user.role, 'department': user.department}
        user.display_name     = request.data.get('display_name', user.display_name)
        user.role             = request.data.get('role', user.role)
        user.department       = request.data.get('department', user.department)
        user.department_label = request.data.get('department_label', user.department_label)
        user.email            = request.data.get('email', user.email)
        if request.data.get('password'):
            user.set_password(request.data['password'])
            write_audit(request.user, 'reset_password', 'admin_user',
                        user.id, user.username, request=request)
        user.save()
        write_audit(request.user, 'update', 'admin_user', user.id, user.username,
                    old_val=old,
                    new_val={'role': user.role, 'department': user.department},
                    request=request)
        return Response({'message': 'Admin account updated.'})

    def delete(self, request, pk):
        try:
            user = AdminUser.objects.get(pk=pk)
        except AdminUser.DoesNotExist:
            return Response({'error': 'Admin not found.'}, status=404)
        if user.role == 'super_admin':
            return Response({'error': 'The Super Admin account cannot be deactivated.'},
                            status=http_status.HTTP_403_FORBIDDEN)
        user.is_active = False
        user.save()
        write_audit(request.user, 'soft_delete', 'admin_user',
                    user.id, user.username, request=request)
        return Response({'message': f'Account for {user.username} deactivated.'})


class AuditLogView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.can_view_audit_log():
            return Response({'error': 'Access denied.'}, status=403)
        from apps.facilities.models import AdminAuditLog
        qs = AdminAuditLog.objects.select_related('admin').order_by('-created_at')[:300]
        if request.query_params.get('entity_type'):
            qs = qs.filter(entity_type=request.query_params['entity_type'])
        if request.query_params.get('action'):
            qs = qs.filter(action=request.query_params['action'])
        return Response([{
            'id':           l.id,
            'admin':        l.admin.display_name if l.admin else 'Unknown',
            'department':   l.admin.get_department_label() if l.admin else '',
            'action':       l.action,
            'entity_type':  l.entity_type,
            'entity_id':    l.entity_id,
            'entity_label': l.entity_label,
            'ip_address':   l.ip_address,
            'created_at':   l.created_at,
        } for l in qs])
```

### TASK 4G — Announcement views

Create or replace `backend_django/apps/announcements/views.py`:

```python
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as http_status
from rest_framework.permissions import IsAuthenticated
from .models import Announcement
from apps.users.permissions import CanApproveAnnouncements, CanPostAnnouncement
from apps.users.views import write_audit


class AnnouncementPublicListView(APIView):
    """Public endpoint — mobile app syncs from here. Returns published only."""
    permission_classes = []

    def get(self, request):
        qs = Announcement.objects.filter(
            status='published', is_deleted=False
        ).order_by('-created_at')[:200]
        return Response([{
            'id':           a.id,
            'title':        a.title,
            'content':      a.content,
            'source_label': a.source_label,
            'source_color': a.source_color,
            'scope':        a.scope,
            'approved_at':  a.approved_at,
            'created_at':   a.created_at,
        } for a in qs])


class AnnouncementCreateView(APIView):
    """Admin creates an announcement. Publishes directly or submits for approval."""
    permission_classes = [CanPostAnnouncement]

    def post(self, request):
        d = request.data
        if not d.get('title') or not d.get('content'):
            return Response({'error': 'Title and content are required.'},
                            status=http_status.HTTP_400_BAD_REQUEST)

        user             = request.user
        publishes_direct = user.can_publish_directly()

        a = Announcement(
            title             = d['title'].strip(),
            content           = d['content'].strip(),
            created_by        = user,
            source_label      = user.get_department_label(),
            source_color      = user.get_department_color(),
            scope             = d.get('scope', 'campus_wide'),
            target_department = d.get('target_department', ''),
            status            = 'published' if publishes_direct else 'pending_approval',
            requires_approval = not publishes_direct,
        )
        a.save()

        if publishes_direct:
            a.publish(approved_by_user=user)
            write_audit(user, 'publish', 'announcement', a.id, a.title, request=request)
            return Response({
                'id':      a.id,
                'status':  'published',
                'message': 'Announcement published and queued for all users.',
            }, status=http_status.HTTP_201_CREATED)
        else:
            write_audit(user, 'create', 'announcement', a.id, a.title, request=request)
            return Response({
                'id':      a.id,
                'status':  'pending_approval',
                'message': 'Announcement submitted for approval.',
            }, status=http_status.HTTP_201_CREATED)


class AnnouncementDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def _get(self, pk):
        try:
            return Announcement.objects.get(pk=pk, is_deleted=False)
        except Announcement.DoesNotExist:
            return None

    def put(self, request, pk):
        a = self._get(pk)
        if not a:
            return Response({'error': 'Not found.'}, status=404)
        user       = request.user
        is_creator = a.created_by_id == user.id
        is_super   = user.role == 'super_admin'
        if not (is_creator or is_super):
            return Response({'error': 'Permission denied.'}, status=403)
        if a.status == 'published' and not is_super:
            return Response({'error': 'Published announcements can only be edited by the Super Admin.'},
                            status=403)
        old = {'title': a.title, 'content': a.content}
        a.title   = request.data.get('title', a.title).strip()
        a.content = request.data.get('content', a.content).strip()
        a.save()
        write_audit(user, 'update', 'announcement', a.id, a.title,
                    old_val=old, new_val={'title': a.title, 'content': a.content},
                    request=request)
        return Response({'message': 'Updated.'})

    def delete(self, request, pk):
        a = self._get(pk)
        if not a:
            return Response({'error': 'Not found.'}, status=404)
        user = request.user
        if not (a.created_by_id == user.id or user.role == 'super_admin'):
            return Response({'error': 'Permission denied.'}, status=403)
        a.is_deleted = True
        a.save()
        write_audit(user, 'soft_delete', 'announcement', a.id, a.title, request=request)
        return Response({'message': 'Deleted.'})


class AnnouncementApproveView(APIView):
    permission_classes = [CanApproveAnnouncements]

    def post(self, request, pk):
        try:
            a = Announcement.objects.get(pk=pk, is_deleted=False)
        except Announcement.DoesNotExist:
            return Response({'error': 'Not found.'}, status=404)
        if a.status != 'pending_approval':
            return Response({'error': f'Cannot approve — status is already "{a.status}".'}, status=400)
        a.publish(approved_by_user=request.user)
        write_audit(request.user, 'approve', 'announcement', a.id, a.title, request=request)
        return Response({'message': 'Approved and published to all users.'})


class AnnouncementRejectView(APIView):
    permission_classes = [CanApproveAnnouncements]

    def post(self, request, pk):
        try:
            a = Announcement.objects.get(pk=pk, is_deleted=False)
        except Announcement.DoesNotExist:
            return Response({'error': 'Not found.'}, status=404)
        if a.status != 'pending_approval':
            return Response({'error': f'Cannot reject — status is already "{a.status}".'}, status=400)
        a.reject(rejected_by_user=request.user, note=request.data.get('note', ''))
        write_audit(request.user, 'reject', 'announcement', a.id, a.title, request=request)
        return Response({'message': 'Announcement rejected.', 'note': request.data.get('note', '')})


class PendingApprovalsView(APIView):
    """Dean and Super Admin see all pending submissions here."""
    permission_classes = [CanApproveAnnouncements]

    def get(self, request):
        qs = Announcement.objects.filter(
            status='pending_approval', is_deleted=False
        ).select_related('created_by').order_by('-created_at')
        return Response([{
            'id':           a.id,
            'title':        a.title,
            'content':      a.content,
            'source_label': a.source_label,
            'source_color': a.source_color,
            'scope':        a.scope,
            'created_by':   a.created_by.display_name if a.created_by else 'Unknown',
            'department':   a.created_by.get_department_label() if a.created_by else '',
            'created_at':   a.created_at,
        } for a in qs])


class MyAnnouncementsView(APIView):
    """Each admin sees their own submissions and their status."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = Announcement.objects.filter(
            created_by=request.user, is_deleted=False
        ).order_by('-created_at')
        return Response([{
            'id':             a.id,
            'title':          a.title,
            'content':        a.content,
            'status':         a.status,
            'scope':          a.scope,
            'rejection_note': a.rejection_note,
            'created_at':     a.created_at,
        } for a in qs])
```

### TASK 4H — URLs

Update `backend_django/apps/users/urls.py`:
```python
from django.urls import path
from .views import (LoginView, LogoutView, MeView,
                    AdminListCreateView, AdminDetailView, AuditLogView)

urlpatterns = [
    path('login/',           LoginView.as_view()),
    path('logout/',          LogoutView.as_view()),
    path('me/',              MeView.as_view()),
    path('admins/',          AdminListCreateView.as_view()),
    path('admins/<int:pk>/', AdminDetailView.as_view()),
    path('audit-log/',       AuditLogView.as_view()),
]
```

Update `backend_django/apps/announcements/urls.py`:
```python
from django.urls import path
from .views import (AnnouncementPublicListView, AnnouncementCreateView,
                    AnnouncementDetailView, AnnouncementApproveView,
                    AnnouncementRejectView, PendingApprovalsView, MyAnnouncementsView)

urlpatterns = [
    path('',                  AnnouncementPublicListView.as_view()),   # GET public
    path('create/',           AnnouncementCreateView.as_view()),        # POST admin
    path('<int:pk>/',         AnnouncementDetailView.as_view()),        # PUT/DELETE
    path('<int:pk>/approve/', AnnouncementApproveView.as_view()),
    path('<int:pk>/reject/',  AnnouncementRejectView.as_view()),
    path('pending/',          PendingApprovalsView.as_view()),
    path('mine/',             MyAnnouncementsView.as_view()),
]
```

### TASK 4I — Seed command with all SEAIT departments

Create `backend_django/apps/users/management/commands/seed_admins.py`.
If it already exists, check if all departments are present. Add any missing ones.

```python
from django.core.management.base import BaseCommand
from apps.users.models import AdminUser

DEFAULT_ADMINS = [
    # ── Super Admin ───────────────────────────────────────────
    {
        'username':       'safety_admin',
        'password':       'TechnoPath@Safety2024!',
        'role':           'super_admin',
        'department':     'safety_security',
        'display_name':   'Safety and Security Office',
        'is_staff':       True,
        'is_superuser':   True,
    },
    # ── Dean ─────────────────────────────────────────────────
    {
        'username':       'dean_seait',
        'password':       'TechnoPath@Dean2024!',
        'role':           'dean',
        'department':     'office_of_the_dean',
        'display_name':   'Office of the Dean',
        'is_staff':       True,
    },
    # ── College Program Heads ─────────────────────────────────
    {
        'username':       'head_agriculture',
        'password':       'TechnoPath@Agri2024!',
        'role':           'program_head',
        'department':     'college_agriculture',
        'display_name':   'Program Head — College of Agriculture and Fisheries',
        'is_staff':       True,
    },
    {
        'username':       'head_criminology',
        'password':       'TechnoPath@Crim2024!',
        'role':           'program_head',
        'department':     'college_criminology',
        'display_name':   'Program Head — College of Criminal Justice Education',
        'is_staff':       True,
    },
    {
        'username':       'head_business',
        'password':       'TechnoPath@Bus2024!',
        'role':           'program_head',
        'department':     'college_business',
        'display_name':   'Program Head — College of Business and Good Governance',
        'is_staff':       True,
    },
    {
        'username':       'head_ict',
        'password':       'TechnoPath@ICT2024!',
        'role':           'program_head',
        'department':     'college_ict',
        'display_name':   'Program Head — College of Information and Communication Technology',
        'is_staff':       True,
    },
    {
        'username':       'head_civil_eng',
        'password':       'TechnoPath@CivEng2024!',
        'role':           'program_head',
        'department':     'dept_civil_engineering',
        'display_name':   'Program Head — Department of Civil Engineering',
        'is_staff':       True,
    },
    {
        'username':       'head_teacher_ed',
        'password':       'TechnoPath@TeachEd2024!',
        'role':           'program_head',
        'department':     'college_teacher_education',
        'display_name':   'Program Head — College of Teacher Education',
        'is_staff':       True,
    },
    {
        'username':       'head_tesda',
        'password':       'TechnoPath@TESDA2024!',
        'role':           'program_head',
        'department':     'tesda',
        'display_name':   'TESDA Coordinator — SEAIT',
        'is_staff':       True,
    },
    {
        'username':       'head_gen_ed',
        'password':       'TechnoPath@GenEd2024!',
        'role':           'program_head',
        'department':     'general_education',
        'display_name':   'Program Head — General Education Department',
        'is_staff':       True,
    },
    # ── Basic Education Head ──────────────────────────────────
    {
        'username':       'head_basic_ed',
        'password':       'TechnoPath@BasicEd2024!',
        'role':           'basic_ed_head',
        'department':     'basic_education',
        'display_name':   'Department Head — Basic Education (Elem / JHS / SHS)',
        'is_staff':       True,
    },
]

class Command(BaseCommand):
    help = 'Seed all default SEAIT admin accounts for TechnoPath'

    def handle(self, *args, **kwargs):
        created = 0
        for d in DEFAULT_ADMINS:
            username = d.pop('username')
            password = d.pop('password')
            if not AdminUser.objects.filter(username=username).exists():
                AdminUser.objects.create_user(username=username, password=password, **d)
                self.stdout.write(self.style.SUCCESS(f'  Created: {username}'))
                created += 1
            else:
                self.stdout.write(f'  Exists:  {username}')
        self.stdout.write(self.style.SUCCESS(f'\nDone. {created} new admin account(s) created.'))
        self.stdout.write('\nDefault credentials are in this seed file.')
        self.stdout.write('IMPORTANT: Change all passwords after first login in production.')
```

After models are ready, run:
```bash
cd backend_django
python manage.py makemigrations
python manage.py migrate
python manage.py seed_admins
python manage.py seed_faq
python manage.py check
```

---

## PART 5 — VUE.JS FRONTEND

Apply Task Safety Protocol. Read every file before modifying it.

### TASK 5A — Auth store (stores all permission flags)

Read `frontend/src/stores/authStore.js`.
If the store does not save all permission flags from the login response, update it.
The login response includes every `can_*` flag as a flat key on the `user` object.
Store the entire `user` object in localStorage and expose each flag as a getter.

```javascript
// frontend/src/stores/authStore.js
import { defineStore } from 'pinia'
import api from '../services/api.js'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user:         JSON.parse(localStorage.getItem('tp_user')  || 'null'),
    token:        localStorage.getItem('tp_token')            || null,
    refreshToken: localStorage.getItem('tp_refresh')          || null,
  }),

  getters: {
    isLoggedIn:                 (s) => !!s.token,
    isSuperAdmin:               (s) => s.user?.role === 'super_admin',
    isDean:                     (s) => s.user?.role === 'dean',
    isProgramHead:              (s) => s.user?.role === 'program_head',
    isBasicEdHead:              (s) => s.user?.role === 'basic_ed_head',
    displayName:                (s) => s.user?.display_name || s.user?.username || '',
    roleLabel:                  (s) => s.user?.role_label || '',
    departmentLabel:            (s) => s.user?.department_label || '',
    departmentColor:            (s) => s.user?.department_color || 'orange',
    department:                 (s) => s.user?.department || '',

    // Permission getters — sourced directly from login response flags
    canManageFacilities:        (s) => s.user?.can_manage_facilities        || false,
    canManageAllRooms:          (s) => s.user?.can_manage_all_rooms         || false,
    canManageOwnRooms:          (s) => s.user?.can_manage_own_rooms         || false,
    canManageNavigation:        (s) => s.user?.can_manage_navigation        || false,
    canManageFAQ:               (s) => s.user?.can_manage_faq               || false,
    canManageAdminAccounts:     (s) => s.user?.can_manage_admin_accounts    || false,
    canViewAuditLog:            (s) => s.user?.can_view_audit_log           || false,
    canViewAllFeedback:         (s) => s.user?.can_view_all_feedback        || false,
    canApproveAnnouncements:    (s) => s.user?.can_approve_announcements    || false,
    canPublishDirectly:         (s) => s.user?.can_publish_directly         || false,
    canPostAnnouncement:        (s) => s.user?.can_post_announcement        || false,
    canSendCampusNotification:  (s) => s.user?.can_send_campus_notification || false,
  },

  actions: {
    async login(username, password) {
      const res = await api.post('/users/login/', { username, password })
      const { access, refresh, user } = res.data
      this.token        = access
      this.refreshToken = refresh
      this.user         = user
      localStorage.setItem('tp_token',   access)
      localStorage.setItem('tp_refresh', refresh)
      localStorage.setItem('tp_user',    JSON.stringify(user))
    },

    logout() {
      api.post('/users/logout/').catch(() => {})
      this.token = this.refreshToken = this.user = null
      localStorage.removeItem('tp_token')
      localStorage.removeItem('tp_refresh')
      localStorage.removeItem('tp_user')
    },
  },
})
```

### TASK 5B — AdminView.vue (one panel, role-driven sidebar)

Read the existing `AdminView.vue`. If it does not match the spec below, replace it.
The critical rules:
- Mobile (< 768px): show a "desktop only" message. No panel at all.
- Desktop (≥ 768px): show the sidebar + main content area.
- Sidebar items are rendered using `v-if` tied to auth store getters.
  Items the user cannot access are simply not rendered — NOT greyed out.
- Pending approval count badge shows next to "Pending Approvals" for Dean/Super Admin.
- Each section is a separate child component imported and rendered in the main area.

```vue
<template>
  <!-- ── Mobile block ── -->
  <div v-if="isMobile" class="tp-mobile-block">
    <div class="tp-mobile-card">
      <span class="tp-mobile-icon">🖥️</span>
      <h2>Admin Panel — Desktop Only</h2>
      <p>The TechnoPath administrative panel is designed for desktop and laptop computers.</p>
      <p>Please open this URL on a desktop browser to manage the system.</p>
    </div>
  </div>

  <!-- ── Desktop admin shell ── -->
  <div v-else class="tp-admin-shell">

    <!-- Sidebar -->
    <aside class="tp-sidebar">

      <div class="tp-sidebar-brand">
        <span class="tp-brand-icon">T</span>
        <div>
          <div class="tp-brand-name">TechnoPath</div>
          <div class="tp-brand-sub">Admin Panel</div>
        </div>
      </div>

      <nav class="tp-sidebar-nav">

        <!-- Dashboard — all roles -->
        <button :class="navCls('dashboard')" @click="go('dashboard')">
          <span class="tp-nav-icon">📊</span>
          <span>Dashboard</span>
        </button>

        <!-- ── Map management group ─────────────── -->
        <div v-if="auth.canManageFacilities || auth.canManageAllRooms || auth.canManageNavigation || auth.canManageFAQ"
             class="tp-nav-group-label">MAP MANAGEMENT</div>

        <button v-if="auth.canManageFacilities"
                :class="navCls('facilities')" @click="go('facilities')">
          <span class="tp-nav-icon">🏢</span>
          <span>Facilities</span>
        </button>

        <button v-if="auth.canManageAllRooms || auth.canManageOwnRooms"
                :class="navCls('rooms')" @click="go('rooms')">
          <span class="tp-nav-icon">🚪</span>
          <span>Rooms</span>
          <span v-if="!auth.canManageAllRooms" class="tp-nav-scope">own dept</span>
        </button>

        <button v-if="auth.canManageNavigation"
                :class="navCls('navigation')" @click="go('navigation')">
          <span class="tp-nav-icon">🗺️</span>
          <span>Navigation Graph</span>
        </button>

        <button v-if="auth.canManageFAQ"
                :class="navCls('faq')" @click="go('faq')">
          <span class="tp-nav-icon">🤖</span>
          <span>FAQ / Chatbot</span>
        </button>

        <!-- ── Communications group ──────────────── -->
        <div class="tp-nav-group-label">COMMUNICATIONS</div>

        <button v-if="auth.canPostAnnouncement"
                :class="navCls('announcements')" @click="go('announcements')">
          <span class="tp-nav-icon">📢</span>
          <span>Announcements</span>
          <span v-if="myPendingCount > 0" class="tp-nav-badge">{{ myPendingCount }}</span>
        </button>

        <button v-if="auth.canApproveAnnouncements"
                :class="navCls('pending')" @click="go('pending')">
          <span class="tp-nav-icon">⏳</span>
          <span>Pending Approvals</span>
          <span v-if="pendingCount > 0" class="tp-nav-badge tp-badge-urgent">{{ pendingCount }}</span>
        </button>

        <button v-if="auth.canSendCampusNotification"
                :class="navCls('notifications')" @click="go('notifications')">
          <span class="tp-nav-icon">🔔</span>
          <span>Send Notification</span>
        </button>

        <!-- ── Administration group ──────────────── -->
        <div v-if="auth.canManageAdminAccounts || auth.canViewAllFeedback || auth.canViewAuditLog"
             class="tp-nav-group-label">ADMINISTRATION</div>

        <button v-if="auth.canManageAdminAccounts"
                :class="navCls('admins')" @click="go('admins')">
          <span class="tp-nav-icon">👥</span>
          <span>Admin Accounts</span>
        </button>

        <button v-if="auth.canViewAllFeedback"
                :class="navCls('feedback')" @click="go('feedback')">
          <span class="tp-nav-icon">⭐</span>
          <span>Feedback & Ratings</span>
        </button>

        <button v-if="auth.canViewAuditLog"
                :class="navCls('auditlog')" @click="go('auditlog')">
          <span class="tp-nav-icon">📋</span>
          <span>Audit Log</span>
        </button>

      </nav>

      <!-- Sidebar footer: current user info + logout -->
      <div class="tp-sidebar-footer">
        <div class="tp-footer-name">{{ auth.displayName }}</div>
        <div class="tp-footer-role">{{ auth.roleLabel }}</div>
        <div class="tp-footer-dept">{{ auth.departmentLabel }}</div>
        <button class="tp-logout-btn" @click="logout">Sign out</button>
      </div>

    </aside>

    <!-- Main content area -->
    <main class="tp-admin-main">

      <AdminDashboard        v-if="section === 'dashboard'" />
      <AdminFacilities       v-else-if="section === 'facilities'  && auth.canManageFacilities" />
      <AdminRooms            v-else-if="section === 'rooms'       && (auth.canManageAllRooms || auth.canManageOwnRooms)"
                             :own-only="!auth.canManageAllRooms"
                             :dept="auth.department" />
      <AdminNavGraph         v-else-if="section === 'navigation'  && auth.canManageNavigation" />
      <AdminFAQ              v-else-if="section === 'faq'         && auth.canManageFAQ" />
      <AdminAnnouncements    v-else-if="section === 'announcements' && auth.canPostAnnouncement"
                             @my-pending="myPendingCount = $event" />
      <AdminPendingApprovals v-else-if="section === 'pending'     && auth.canApproveAnnouncements"
                             @count="pendingCount = $event" />
      <AdminSendNotification v-else-if="section === 'notifications' && auth.canSendCampusNotification" />
      <AdminAccounts         v-else-if="section === 'admins'      && auth.canManageAdminAccounts" />
      <AdminFeedback         v-else-if="section === 'feedback'    && auth.canViewAllFeedback" />
      <AdminAuditLog         v-else-if="section === 'auditlog'    && auth.canViewAuditLog" />

      <div v-else class="tp-access-denied">
        <span>🔒</span>
        <p>You do not have permission to access this section.</p>
      </div>

    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/authStore.js'
import api from '../services/api.js'

import AdminDashboard        from '../components/admin/AdminDashboard.vue'
import AdminFacilities       from '../components/admin/AdminFacilities.vue'
import AdminRooms            from '../components/admin/AdminRooms.vue'
import AdminNavGraph         from '../components/admin/AdminNavGraph.vue'
import AdminFAQ              from '../components/admin/AdminFAQ.vue'
import AdminAnnouncements    from '../components/admin/AdminAnnouncements.vue'
import AdminPendingApprovals from '../components/admin/AdminPendingApprovals.vue'
import AdminSendNotification from '../components/admin/AdminSendNotification.vue'
import AdminAccounts         from '../components/admin/AdminAccounts.vue'
import AdminFeedback         from '../components/admin/AdminFeedback.vue'
import AdminAuditLog         from '../components/admin/AdminAuditLog.vue'

const router        = useRouter()
const auth          = useAuthStore()
const section       = ref('dashboard')
const pendingCount  = ref(0)
const myPendingCount= ref(0)

const isMobile = computed(() => window.innerWidth < 768)

function navCls(name) {
  return ['tp-sidebar-nav-item', section.value === name ? 'active' : '']
}

function go(name) { section.value = name }

async function loadPendingCount() {
  if (!auth.canApproveAnnouncements) return
  try {
    const r = await api.get('/announcements/pending/')
    pendingCount.value = r.data.length
  } catch { pendingCount.value = 0 }
}

function logout() {
  auth.logout()
  router.push('/admin/login')
}

onMounted(() => {
  if (!auth.isLoggedIn) { router.push('/admin/login'); return }
  loadPendingCount()
})
</script>

<style scoped>
/* Mobile block */
.tp-mobile-block {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-surface);
  padding: var(--space-6);
}
.tp-mobile-card {
  background: var(--color-bg);
  border-radius: var(--radius-xl);
  padding: 40px 32px;
  max-width: 420px;
  text-align: center;
  box-shadow: var(--shadow-md);
}
.tp-mobile-icon { font-size: 56px; display: block; margin-bottom: 16px; }
.tp-mobile-card h2 { font-size: var(--text-xl); font-weight: 700; font-family: var(--font-primary); margin-bottom: 12px; }
.tp-mobile-card p { font-size: var(--text-base); font-family: var(--font-primary); color: var(--color-text-secondary); line-height: 1.6; margin-bottom: 8px; }

/* Admin shell */
.tp-admin-shell { display: flex; height: 100vh; overflow: hidden; background: var(--color-surface); font-family: var(--font-primary); }

/* Sidebar */
.tp-sidebar {
  width: 240px;
  min-width: 240px;
  max-width: 240px;
  background: var(--color-bg);
  border-right: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  flex-shrink: 0;
}
.tp-sidebar-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 18px 16px;
  border-bottom: 1px solid var(--color-border);
}
.tp-brand-icon {
  width: 34px; height: 34px;
  background: var(--color-primary);
  color: #fff;
  border-radius: var(--radius-md);
  display: flex; align-items: center; justify-content: center;
  font-size: 17px; font-weight: 700;
  font-family: var(--font-primary);
  flex-shrink: 0;
}
.tp-brand-name { font-size: var(--text-base); font-weight: 700; font-family: var(--font-primary); color: var(--color-text-primary); line-height: 1.2; }
.tp-brand-sub  { font-size: var(--text-xs); font-family: var(--font-primary); color: var(--color-text-hint); }

.tp-sidebar-nav { flex: 1; padding: 6px 0; display: flex; flex-direction: column; }

.tp-nav-group-label {
  font-size: 10px;
  font-family: var(--font-primary);
  font-weight: 700;
  color: var(--color-text-hint);
  letter-spacing: 0.7px;
  text-transform: uppercase;
  padding: 12px 16px 4px;
}

.tp-sidebar-nav-item {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  padding: 9px 16px;
  min-height: 44px;
  border: none;
  background: transparent;
  font-family: var(--font-primary);
  font-size: var(--text-sm);
  color: var(--color-text-secondary);
  cursor: pointer;
  text-align: left;
  transition: background 0.1s, color 0.1s;
  border-left: 3px solid transparent;
}
.tp-sidebar-nav-item:hover { background: var(--color-surface); color: var(--color-text-primary); }
.tp-sidebar-nav-item.active {
  background: var(--color-primary-light);
  color: var(--color-primary-dark);
  font-weight: 600;
  border-left-color: var(--color-primary);
}
.tp-nav-icon { font-size: 15px; width: 18px; text-align: center; flex-shrink: 0; }
.tp-nav-scope {
  margin-left: auto;
  font-size: 10px;
  background: var(--color-surface-2);
  color: var(--color-text-hint);
  padding: 1px 6px;
  border-radius: var(--radius-full);
  font-family: var(--font-primary);
}
.tp-nav-badge {
  margin-left: auto;
  background: var(--color-primary);
  color: #fff;
  border-radius: var(--radius-full);
  font-size: 10px;
  font-weight: 700;
  font-family: var(--font-primary);
  min-width: 18px; height: 18px;
  padding: 0 4px;
  display: inline-flex; align-items: center; justify-content: center;
}
.tp-badge-urgent { background: var(--color-danger); }

/* Sidebar footer */
.tp-sidebar-footer {
  padding: 14px 16px;
  border-top: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.tp-footer-name { font-size: var(--text-sm); font-weight: 600; font-family: var(--font-primary); color: var(--color-text-primary); }
.tp-footer-role { font-size: var(--text-xs); font-family: var(--font-primary); color: var(--color-primary); font-weight: 500; }
.tp-footer-dept { font-size: var(--text-xs); font-family: var(--font-primary); color: var(--color-text-hint); }
.tp-logout-btn {
  margin-top: 8px;
  width: 100%;
  padding: 7px 0;
  background: transparent;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  font-family: var(--font-primary);
  font-size: var(--text-sm);
  color: var(--color-danger);
  cursor: pointer;
  min-height: 36px;
}
.tp-logout-btn:hover { background: var(--color-danger-bg); }

/* Main content */
.tp-admin-main { flex: 1; overflow-y: auto; padding: 28px 32px; }

.tp-access-denied {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 200px;
  gap: 12px;
  color: var(--color-text-hint);
  font-family: var(--font-primary);
  font-size: var(--text-base);
}
.tp-access-denied span { font-size: 40px; }
</style>
```

### TASK 5C — AdminAnnouncements.vue

Read the existing component (if it exists). It must implement:
1. A list of the admin's own announcements (GET `/announcements/mine/`)
2. A "+ New Announcement" button
3. A form with: Title (text input), Content (textarea), Scope (select dropdown)
4. Scope options: Entire Campus, All College, Basic Education Only, My Department Only
5. The submit button says "Submit for Approval" if the user cannot publish directly,
   or "Publish Now" if they can
6. A clearly worded info banner explaining the approval requirement
7. Each submission in the list shows a colored status badge:
   - `pending_approval` → amber/orange "Awaiting Approval"
   - `published` → green "Published"
   - `rejected` → red "Rejected" + show the rejection_note in a red callout box
   - `archived` → gray "Archived"

All fonts must use `var(--font-primary)`. All sizes must use CSS variables from the design system.
All buttons must be min-height 44px.

### TASK 5D — AdminPendingApprovals.vue

Read the existing component (if it exists). It must implement:
1. A list of all pending announcements (GET `/announcements/pending/`)
2. Each card shows: department label (colored chip), submitter name, submission date, title, content, scope
3. "Approve & Publish" button → POST `/announcements/<id>/approve/` → reload list, decrement count
4. "Reject" button → opens a dialog with an optional rejection note textarea → POST `/announcements/<id>/reject/`
5. After every action, emit `count` event so the sidebar badge updates
6. An empty state message when there are no pending items

### TASK 5E — Mobile NotificationsView.vue — Department chip display

Read `frontend/src/views/NotificationsView.vue`.
Each notification item must show the department/office source label as a colored chip.
Add the chip immediately above the notification title in each list item.

The chip CSS (add to the component's `<style scoped>` block if not already present):
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
.chip-red        { background: #FFEBEE; color: #B71C1C; }
.chip-dark_blue  { background: #E8EAF6; color: #1A237E; }
.chip-green      { background: #E8F5E9; color: #1B5E20; }
.chip-charcoal   { background: #ECEFF1; color: #263238; }
.chip-purple     { background: #F3E5F5; color: #4A148C; }
.chip-teal       { background: #E0F2F1; color: #004D40; }
.chip-amber      { background: #FFF8E1; color: #E65100; }
.chip-blue       { background: #E3F2FD; color: #0D47A1; }
.chip-dark_green { background: #E8F5E9; color: #33691E; }
.chip-indigo     { background: #E8EAF6; color: #283593; }
.chip-brown      { background: #EFEBE9; color: #4E342E; }
.chip-orange     { background: #FFF3E0; color: #E65100; }
```

In the notification item template:
```html
<span v-if="n.source_label"
      :class="['source-chip', 'chip-' + (n.source_color || 'orange')]">
  {{ n.source_label }}
</span>
```

### TASK 5F — Update sync.js to include source_label and source_color

Read `frontend/src/services/sync.js`.
Ensure that when notifications are synced from Django into IndexedDB,
the `source_label` and `source_color` fields are preserved in the stored records.
The `bulkPut` call already handles this if the API response includes those fields,
but verify the Dexie schema in `db.js` does not strip those columns.

The notifications table in `db.js` must be:
```javascript
notifications: '++id, type, is_read, source_color, created_at'
```

---

## PART 6 — VERIFICATION

After completing all tasks, run every check below. All must pass.

```bash
cd backend_django

# 1 — Django system check
python manage.py check

# 2 — All migrations applied
python manage.py showmigrations

# 3 — Required tables exist
python -c "
import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'technopath.settings')
django.setup()
from django.db import connection
tables = connection.introspection.table_names()
required = [
    'admin_users', 'announcements', 'notifications',
    'facilities', 'rooms', 'navigation_nodes', 'navigation_edges',
    'faq_entries', 'feedback', 'ai_chat_logs', 'admin_audit_log',
]
for t in required:
    print(f'  {t}: {\"OK\" if t in tables else \"MISSING\"}'  )
"

# 4 — Admin seed accounts exist
python -c "
import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'technopath.settings')
django.setup()
from apps.users.models import AdminUser
for role in ['super_admin', 'dean', 'program_head', 'basic_ed_head']:
    count = AdminUser.objects.filter(role=role, is_active=True).count()
    print(f'  {role}: {count} account(s)')
"

# 5 — Permission flags work correctly
python -c "
import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'technopath.settings')
django.setup()
from apps.users.models import AdminUser
u = AdminUser.objects.filter(role='super_admin').first()
if u:
    p = u.get_permissions_dict()
    assert p['can_manage_facilities']    == True,  'Super admin must manage facilities'
    assert p['can_publish_directly']     == True,  'Super admin must publish directly'
    assert p['can_approve_announcements']== True,  'Super admin must approve'
    print('  super_admin permissions: OK')
u2 = AdminUser.objects.filter(role='program_head').first()
if u2:
    p2 = u2.get_permissions_dict()
    assert p2['can_manage_facilities']   == False, 'Program head must NOT manage facilities'
    assert p2['can_publish_directly']    == False, 'Program head must NOT publish directly'
    assert p2['can_post_announcement']   == True,  'Program head must post (for approval)'
    print('  program_head permissions: OK')
"

# 6 — Frontend build
cd C:\Users\User\Downloads\SAD\version4_technopath\frontend
npm run build
```

---

## PART 7 — MASTER RULES

1. Apply Task Safety Protocol. Read every file before changing it.
   Report COMPLETE / NEEDS REFINEMENT / MISSING before each task.
2. Never delete working code. Never rewrite files that only need small fixes.
3. All deletes are soft deletes (`is_deleted = True`). Never use `.delete()`.
4. Every admin write action must write a row to `AdminAuditLog` via `write_audit()`.
5. Program Heads and Basic Education Head can NEVER publish announcements directly.
   Their submissions always go to `status = 'pending_approval'`.
6. Super Admin and Dean publish directly with no approval step.
7. The admin panel sidebar shows ONLY sections the logged-in role can access.
   Sections are hidden with `v-if`, NOT greyed out or disabled.
8. There is ONE admin panel at `/admin`. The view adapts based on auth store getters.
9. On screens narrower than 768px, the admin panel shows a "desktop only" message.
10. Announcement notification cards on mobile MUST display the `source_label` as a
    colored chip using the department color system defined in Part 3.
11. The Basic Education Department (Elementary + JHS + SHS) has ONE account with
    role `basic_ed_head`. No separate accounts per grade level.
12. All fonts in every Vue component must use `var(--font-primary)`.
    All font sizes must use the CSS variables from the design system.
    All tappable elements must be min-height 44px and min-width 44px.
13. The admin panel is desktop only — it is not responsive for mobile.
    The mobile-block message is the intended behavior on small screens.
14. After every model change: `python manage.py makemigrations && python manage.py migrate`.

---

*TechnoPath: SEAIT Guide Map and Navigation System*
*South East Asian Institute of Technology, Inc.*
*Barangay Crossing Rubber, National Highway, Tupi, South Cotabato, Philippines*
*Prompt Version 4 — Definitive Admin Backend — April 2026*
