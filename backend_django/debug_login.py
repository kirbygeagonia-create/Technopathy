#!/usr/bin/env python
"""Test login without requests module"""
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'technopath.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import django
django.setup()

from apps.users.models import AdminUser
from django.contrib.auth import authenticate

print("=" * 60)
print("LOGIN DEBUG TEST")
print("=" * 60)

# Check if admin exists
print("\n[1] Checking admin user...")
try:
    user = AdminUser.objects.filter(username='safety_admin').first()
    if user:
        print(f"  ✓ Found user: {user.username}")
        print(f"  ✓ Role: {user.role}")
        print(f"  ✓ Is active: {user.is_active}")
        print(f"  ✓ Is staff: {user.is_staff}")
    else:
        print("  ✗ User 'safety_admin' NOT FOUND")
        print("  Run: python manage.py seed_admins")
except Exception as e:
    print(f"  ✗ Error: {e}")

# Test authentication
print("\n[2] Testing password authentication...")
try:
    user = authenticate(username='safety_admin', password='TechnoPath@Safety2024!')
    if user:
        print(f"  ✓ Authentication SUCCESS for {user.username}")
    else:
        print("  ✗ Authentication FAILED - wrong password")
        print("  Default password: TechnoPath@Safety2024!")
except Exception as e:
    print(f"  ✗ Error: {e}")

# Test wrong password
print("\n[3] Testing wrong password...")
try:
    user = authenticate(username='safety_admin', password='wrongpassword')
    if user:
        print("  ? Unexpected: auth succeeded with wrong password")
    else:
        print("  ✓ Wrong password correctly rejected")
except Exception as e:
    print(f"  ✗ Error: {e}")

print("\n" + "=" * 60)
