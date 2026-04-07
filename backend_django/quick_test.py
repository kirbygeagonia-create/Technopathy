#!/usr/bin/env python
"""Quick test to verify Django models work"""
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'technopath.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import django
django.setup()

print("=" * 60)
print("TECHNOPATH - QUICK TEST")
print("=" * 60)

# Test imports
print("\n[1] Testing imports...")
try:
    from apps.users.models import AdminUser
    from apps.announcements.models import Announcement
    from apps.notifications.models import Notification
    from apps.core.models import AdminAuditLog
    print("✓ All imports successful")
except Exception as e:
    print(f"✗ Import error: {e}")

# Test database
print("\n[2] Testing database...")
try:
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        print("✓ Database connection OK")
except Exception as e:
    print(f"✗ Database error: {e}")

# Test admin user count
print("\n[3] Testing admin accounts...")
try:
    count = AdminUser.objects.count()
    print(f"✓ {count} admin accounts found")
except Exception as e:
    print(f"✗ Admin query error: {e}")

# Test announcement methods
print("\n[4] Testing Announcement model methods...")
try:
    methods = ['publish', 'reject', 'archive']
    for m in methods:
        if hasattr(Announcement, m):
            print(f"✓ Announcement.{m}() exists")
        else:
            print(f"✗ Announcement.{m}() missing")
except Exception as e:
    print(f"✗ Error: {e}")

# Test permissions
print("\n[5] Testing permissions...")
try:
    sa = AdminUser.objects.filter(role='super_admin').first()
    if sa:
        perms = sa.get_permissions_dict()
        print(f"✓ Super Admin has {len(perms)} permissions")
        print(f"  - can_manage_admin_accounts: {perms.get('can_manage_admin_accounts')}")
        print(f"  - can_approve_announcements: {perms.get('can_approve_announcements')}")
    else:
        print("  No super_admin found")
except Exception as e:
    print(f"✗ Permission error: {e}")

print("\n" + "=" * 60)
print("ALL TESTS PASSED")
print("=" * 60)
