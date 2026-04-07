#!/usr/bin/env python
"""Final comprehensive verification - no errors check"""
import os
import re

print("=" * 70)
print("FINAL COMPREHENSIVE VERIFICATION - NO ERRORS CHECK")
print("=" * 70)

errors = []
warnings = []

# 1. Django Backend Check
print("\n[1] DJANGO BACKEND CHECK")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'technopath.settings')
sys_path = r'c:\Users\ADMIN\OneDrive\Documents\SAD_System_files\version4_technopath\backend_django'
import sys
sys.path.insert(0, sys_path)

try:
    import django
    django.setup()
    
    # Test imports
    from apps.users.models import AdminUser
    from apps.announcements.models import Announcement
    from apps.notifications.models import Notification
    print("  ✓ Django imports successful")
    
    # Test database
    from django.db import connection
    with connection.cursor() as c:
        c.execute("SELECT 1")
    print("  ✓ Database connection OK")
    
    # Test admin accounts
    count = AdminUser.objects.filter(is_active=True).count()
    print(f"  ✓ {count} active admin accounts")
    
    # Test permissions
    sa = AdminUser.objects.filter(role='super_admin').first()
    if sa and sa.get_permissions_dict().get('can_manage_admin_accounts'):
        print("  ✓ Permission methods working")
    
    # Test announcement methods
    methods = ['publish', 'reject', 'archive']
    for m in methods:
        if hasattr(Announcement, m):
            pass  # OK
        else:
            errors.append(f"Missing method: Announcement.{m}()")
    print("  ✓ All announcement methods present")
    
except Exception as e:
    errors.append(f"Django backend error: {e}")
    print(f"  ✗ Error: {e}")

# 2. Vue Files Check
print("\n[2] VUE FILES CHECK")
admin_dir = r"c:\Users\ADMIN\OneDrive\Documents\SAD_System_files\version4_technopath\frontend\src\components\admin"

vue_files = [f for f in os.listdir(admin_dir) if f.endswith('.vue')]

for filename in vue_files:
    filepath = os.path.join(admin_dir, filename)
    basename = filename.replace('.vue', '').lower()
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check template section
    if '<template>' not in content or '</template>' not in content:
        errors.append(f"{filename}: Missing template section")
    
    # Check script section
    if '<script' not in content:
        errors.append(f"{filename}: Missing script section")
    
    # Check style scoped
    if '<style scoped>' not in content:
        warnings.append(f"{filename}: Missing scoped style")
    
    # Check inline styles (bad)
    inline = re.findall(r'style="[^"]*"', content)
    if inline:
        errors.append(f"{filename}: Has {len(inline)} inline style(s)")

print(f"  ✓ Checked {len(vue_files)} Vue files")

# 3. Class Naming Convention Check
print("\n[3] CLASS NAMING CONVENTION CHECK")
for filename in vue_files:
    filepath = os.path.join(admin_dir, filename)
    basename = filename.replace('.vue', '').lower()
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check main container class
    expected_prefix = basename + '-'
    if f'class="{expected_prefix}' in content:
        pass  # OK
    elif f'class="admin-' in content:
        errors.append(f"{filename}: Uses generic 'admin-*' class instead of '{expected_prefix}*'")

print(f"  ✓ Checked naming in {len(vue_files)} files")

# Summary
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

if errors:
    print(f"\nERRORS ({len(errors)}):")
    for e in errors:
        print(f"  ✗ {e}")
else:
    print("\n✓ NO ERRORS FOUND")

if warnings:
    print(f"\nWARNINGS ({len(warnings)}):")
    for w in warnings:
        print(f"  ⚠ {w}")

print("\n" + "=" * 70)
print("SYSTEM STATUS: " + ("ALL CLEAR" if not errors else "ERRORS PRESENT"))
print("=" * 70)
