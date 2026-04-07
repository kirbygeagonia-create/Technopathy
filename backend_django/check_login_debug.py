#!/usr/bin/env python
"""Debug login issues"""
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'technopath.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import django
django.setup()

print("=" * 60)
print("LOGIN DEBUG - Checking all components")
print("=" * 60)

# 1. Check admin user exists
print("\n[1] Checking admin user...")
from apps.users.models import AdminUser
user = AdminUser.objects.filter(username='safety_admin').first()
if user:
    print(f"  ✓ User exists: {user.username}")
    print(f"  ✓ Role: {user.role}")
    print(f"  ✓ Active: {user.is_active}")
    print(f"  ✓ Staff: {user.is_staff}")
else:
    print("  ✗ User NOT FOUND")

# 2. Check password hash
print("\n[2] Checking password...")
from django.contrib.auth import authenticate
auth_user = authenticate(username='safety_admin', password='TechnoPath@Safety2024!')
if auth_user:
    print("  ✓ Password is correct")
else:
    print("  ✗ Password authentication failed")

# 3. Check URLs
print("\n[3] Checking URL configuration...")
from django.urls import resolve
try:
    match = resolve('/api/users/login/')
    print(f"  ✓ URL /api/users/login/ resolves to: {match.func.__name__}")
except Exception as e:
    print(f"  ✗ URL error: {e}")

# 4. Check views
print("\n[4] Checking LoginView...")
from apps.users.views import LoginView
print(f"  ✓ LoginView imported successfully")

print("\n" + "=" * 60)
print("If all checks passed, the issue is likely:")
print("  - Django server not running")
print("  - Frontend not connecting to backend")
print("  - Wrong URL in frontend")
print("=" * 60)
