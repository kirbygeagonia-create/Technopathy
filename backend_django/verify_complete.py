#!/usr/bin/env python
"""
Comprehensive TechnoPath Admin Backend Verification Script
"""
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'technopath.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import django
django.setup()

print("=" * 70)
print("TECHNOPATH ADMIN BACKEND - COMPREHENSIVE VERIFICATION")
print("=" * 70)

# ============================================================================
# 1. CHECK INSTALLED APPS
# ============================================================================
print("\n[1] CHECKING INSTALLED APPS...")
from django.conf import settings
required_apps = [
    'apps.users', 'apps.facilities', 'apps.rooms', 'apps.navigation',
    'apps.chatbot', 'apps.notifications', 'apps.feedback', 'apps.core',
    'apps.announcements'
]
missing = [a for a in required_apps if a not in settings.INSTALLED_APPS]
if missing:
    print(f"  ✗ Missing apps: {missing}")
else:
    print(f"  ✓ All required apps installed ({len(required_apps)} apps)")

# ============================================================================
# 2. CHECK DATABASE TABLES
# ============================================================================
print("\n[2] CHECKING DATABASE TABLES...")
from django.db import connection
cursor = connection.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [t[0] for t in cursor.fetchall()]

required_tables = [
    'admin_users', 'announcements', 'notifications', 'admin_audit_log',
    'facilities_facility', 'rooms_room', 'navigation_navnode',
    'chatbot_faqentry', 'feedback_feedback'
]
for table in required_tables:
    status = "✓" if table in tables else "✗"
    print(f"  {status} {table}")

# ============================================================================
# 3. CHECK ADMIN USER MODEL
# ============================================================================
print("\n[3] CHECKING ADMIN USER MODEL...")
from apps.users.models import AdminUser

# Check ROLE_CHOICES
roles = dict(AdminUser.ROLE_CHOICES)
expected_roles = ['super_admin', 'dean', 'program_head', 'basic_ed_head']
for role in expected_roles:
    if role in roles:
        print(f"  ✓ Role: {role} -> {roles[role]}")
    else:
        print(f"  ✗ Missing role: {role}")

# Check department colors
dept_colors = AdminUser.DEPARTMENT_COLORS
print(f"  ✓ Department colors defined: {len(dept_colors)} departments")

# Check methods
methods = ['get_permissions_dict', 'can_publish_directly', 'get_department_color', 'get_department_label']
for method in methods:
    if hasattr(AdminUser, method):
        print(f"  ✓ Method: {method}()")
    else:
        print(f"  ✗ Missing method: {method}()")

# ============================================================================
# 4. CHECK ANNOUNCEMENT MODEL
# ============================================================================
print("\n[4] CHECKING ANNOUNCEMENT MODEL...")
from apps.announcements.models import Announcement

# Check STATUS_CHOICES
statuses = dict(Announcement.STATUS_CHOICES)
expected_statuses = ['pending_approval', 'published', 'rejected', 'archived']
for status in expected_statuses:
    if status in statuses:
        print(f"  ✓ Status: {status}")
    else:
        print(f"  ✗ Missing status: {status}")

# Check methods
ann_methods = ['publish', 'reject', 'archive']
for method in ann_methods:
    if hasattr(Announcement, method):
        print(f"  ✓ Method: {method}()")
    else:
        print(f"  ✗ Missing method: {method}()")

# ============================================================================
# 5. CHECK NOTIFICATION MODEL
# ============================================================================
print("\n[5] CHECKING NOTIFICATION MODEL...")
from apps.notifications.models import Notification

# Check fields exist
fields = ['source_label', 'source_color', 'announcement', 'created_by']
for field in fields:
    if hasattr(Notification, field):
        print(f"  ✓ Field: {field}")
    else:
        print(f"  ✗ Missing field: {field}")

# ============================================================================
# 6. CHECK PERMISSIONS
# ============================================================================
print("\n[6] CHECKING PERMISSIONS...")
from apps.users.permissions import IsSuperAdmin, IsDeanOrSuperAdmin, CanApproveAnnouncements, CanPostAnnouncement

perm_classes = [
    'IsSuperAdmin', 'IsDeanOrSuperAdmin', 'CanApproveAnnouncements',
    'CanPostAnnouncement', 'IsAnyAdmin'
]
import apps.users.permissions as perm_module
for cls_name in perm_classes:
    if hasattr(perm_module, cls_name):
        print(f"  ✓ Permission class: {cls_name}")
    else:
        print(f"  ✗ Missing permission class: {cls_name}")

# ============================================================================
# 7. CHECK ADMIN ACCOUNTS
# ============================================================================
print("\n[7] CHECKING SEEDED ADMIN ACCOUNTS...")
role_counts = {}
for role in expected_roles:
    count = AdminUser.objects.filter(role=role, is_active=True).count()
    role_counts[role] = count
    print(f"  ✓ {role}: {count} account(s)")

total = sum(role_counts.values())
print(f"  Total: {total} admin accounts")

# ============================================================================
# 8. TEST PERMISSION LOGIC
# ============================================================================
print("\n[8] TESTING PERMISSION LOGIC...")

# Super Admin
super_admin = AdminUser.objects.filter(role='super_admin').first()
if super_admin:
    perms = super_admin.get_permissions_dict()
    checks = [
        ('can_manage_admin_accounts', True),
        ('can_approve_announcements', True),
        ('can_publish_directly', True),
    ]
    for key, expected in checks:
        actual = perms.get(key, False)
        status = "✓" if actual == expected else "✗"
        print(f"  {status} Super Admin {key}: {actual} (expected {expected})")

# Program Head
ph = AdminUser.objects.filter(role='program_head').first()
if ph:
    perms = ph.get_permissions_dict()
    checks = [
        ('can_post_announcement', True),
        ('can_publish_directly', False),
        ('can_approve_announcements', False),
    ]
    for key, expected in checks:
        actual = perms.get(key, False)
        status = "✓" if actual == expected else "✗"
        print(f"  {status} Program Head {key}: {actual} (expected {expected})")

# Dean
dean = AdminUser.objects.filter(role='dean').first()
if dean:
    perms = dean.get_permissions_dict()
    checks = [
        ('can_approve_announcements', True),
        ('can_publish_directly', True),
        ('can_manage_own_rooms', True),
    ]
    for key, expected in checks:
        actual = perms.get(key, False)
        status = "✓" if actual == expected else "✗"
        print(f"  {status} Dean {key}: {actual} (expected {expected})")

# ============================================================================
# 9. CHECK URLS
# ============================================================================
print("\n[9] CHECKING URL CONFIGURATION...")
from django.urls import resolve

test_urls = [
    '/api/users/login/',
    '/api/users/logout/',
    '/api/users/me/',
    '/api/users/admins/',
    '/api/users/audit-log/',
    '/api/announcements/',
    '/api/announcements/create/',
    '/api/announcements/pending/',
    '/api/announcements/mine/',
]

for url in test_urls:
    try:
        resolve(url)
        print(f"  ✓ URL: {url}")
    except Exception as e:
        print(f"  ✗ URL: {url} - {str(e)[:50]}")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 70)
print("VERIFICATION COMPLETE")
print("=" * 70)
print(f"Admin accounts: {total} (super_admin: {role_counts.get('super_admin', 0)}, dean: {role_counts.get('dean', 0)}, program_head: {role_counts.get('program_head', 0)}, basic_ed_head: {role_counts.get('basic_ed_head', 0)})")
print("Key files implemented:")
print("  - apps/users/models.py (AdminUser with roles/permissions)")
print("  - apps/announcements/models.py (Announcement workflow)")
print("  - apps/notifications/models.py (with source_label/source_color)")
print("  - apps/users/permissions.py (role-based permissions)")
print("  - apps/users/views.py (login/admin/audit views)")
print("  - apps/announcements/views.py (CRUD + approval)")
print("  - apps/users/management/commands/seed_admins.py")
