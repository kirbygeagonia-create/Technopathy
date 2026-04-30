#!/usr/bin/env python
"""
Set all admin passwords to 'admin123' after loading fixtures.
Run this in Render Shell after loaddata.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'technopath.settings')
django.setup()

from apps.users.models import AdminUser

# All admin usernames
usernames = [
    'safety_admin',
    'dean_seait',
    'dean_agriculture',
    'dean_criminology',
    'dean_business',
    'dean_ict',
    'dean_civil_eng',
    'dean_teacher_ed',
    'dean_tesda',
    'dean_gen_ed',
    'dean_basic_ed',
    'head_agriculture',
    'head_criminology',
    'head_business',
    'head_ict',
    'head_civil_eng',
    'head_teacher_ed',
    'head_tesda',
    'head_gen_ed',
    'head_basic_ed'
]

count = 0
for username in usernames:
    try:
        user = AdminUser.objects.get(username=username)
        user.set_password('admin123')
        user.save()
        print(f"✓ Set password for {username}")
        count += 1
    except AdminUser.DoesNotExist:
        print(f"✗ User not found: {username}")

print(f"\nDone! Updated {count} users with password: admin123")
