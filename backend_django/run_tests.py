#!/usr/bin/env python
"""Run Django tests for TechnoPath Admin Backend"""
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'technopath.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import django
django.setup()

from django.core.management import call_command

print("=" * 70)
print("DJANGO BACKEND TESTS")
print("=" * 70)

# Run Django system check
print("\n[1] Running Django system checks...")
try:
    call_command('check', verbosity=2)
    print("✓ System check passed")
except Exception as e:
    print(f"✗ System check failed: {e}")

# Check if we can import all models
print("\n[2] Testing model imports...")
try:
    from apps.users.models import AdminUser
    from apps.announcements.models import Announcement
    from apps.notifications.models import Notification
    from apps.core.models import AdminAuditLog
    print("✓ All model imports successful")
except Exception as e:
    print(f"✗ Model import failed: {e}")

# Check database connectivity
print("\n[3] Testing database connectivity...")
try:
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        if result[0] == 1:
            print("✓ Database connection successful")
except Exception as e:
    print(f"✗ Database connection failed: {e}")

# Check if admin users exist
print("\n[4] Checking seeded admin accounts...")
try:
    count = AdminUser.objects.filter(is_active=True).count()
    print(f"✓ Found {count} active admin accounts")
    roles = ['super_admin', 'dean', 'program_head', 'basic_ed_head']
    for role in roles:
        role_count = AdminUser.objects.filter(role=role).count()
        print(f"  - {role}: {role_count}")
except Exception as e:
    print(f"✗ Admin account check failed: {e}")

# Test permission methods
print("\n[5] Testing permission methods...")
try:
    super_admin = AdminUser.objects.filter(role='super_admin').first()
    if super_admin:
        perms = super_admin.get_permissions_dict()
        print("✓ Super Admin permissions:")
        for k, v in perms.items():
            print(f"    - {k}: {v}")
except Exception as e:
    print(f"✗ Permission test failed: {e}")

# Test Announcement model methods
print("\n[6] Testing Announcement model methods...")
try:
    from apps.announcements.models import Announcement
    methods = ['publish', 'reject', 'archive']
    for method in methods:
        if hasattr(Announcement, method):
            print(f"✓ Announcement.{method}() exists")
        else:
            print(f"✗ Announcement.{method}() missing")
except Exception as e:
    print(f"✗ Announcement model test failed: {e}")

print("\n" + "=" * 70)
print("DJANGO TESTS COMPLETE")
print("=" * 70)
