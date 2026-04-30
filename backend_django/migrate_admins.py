#!/usr/bin/env python
"""Migrate all 20 admin accounts to PostgreSQL database."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'technopath.settings')
django.setup()

from apps.users.models import AdminUser

# Admin data: (username, password, role, department)
# All passwords set to admin123 for easy access
ADMINS = [
    ('safety_admin', 'admin123', 'super_admin', 'safety_security'),
    ('dean_seait', 'admin123', 'dean', 'office_of_the_dean'),
    ('dean_agriculture', 'admin123', 'dean', 'college_agriculture'),
    ('dean_criminology', 'admin123', 'dean', 'college_criminology'),
    ('dean_business', 'admin123', 'dean', 'college_business'),
    ('dean_ict', 'admin123', 'dean', 'college_ict'),
    ('dean_civil_eng', 'admin123', 'dean', 'dept_civil_engineering'),
    ('dean_teacher_ed', 'admin123', 'dean', 'college_teacher_education'),
    ('dean_tesda', 'admin123', 'dean', 'tesda'),
    ('dean_gen_ed', 'admin123', 'dean', 'general_education'),
    ('dean_basic_ed', 'admin123', 'dean', 'basic_education'),
    ('head_agriculture', 'admin123', 'program_head', 'college_agriculture'),
    ('head_criminology', 'admin123', 'program_head', 'college_criminology'),
    ('head_business', 'admin123', 'program_head', 'college_business'),
    ('head_ict', 'admin123', 'program_head', 'college_ict'),
    ('head_civil_eng', 'admin123', 'program_head', 'dept_civil_engineering'),
    ('head_teacher_ed', 'admin123', 'program_head', 'college_teacher_education'),
    ('head_tesda', 'admin123', 'program_head', 'tesda'),
    ('head_gen_ed', 'admin123', 'program_head', 'general_education'),
    ('head_basic_ed', 'admin123', 'basic_ed_head', 'basic_education'),
]

def migrate():
    created = 0
    updated = 0
    
    for username, password, role, department in ADMINS:
        display_name = username.replace('_', ' ').title()
        
        # Check if user exists
        user, was_created = AdminUser.objects.get_or_create(
            username=username,
            defaults={
                'role': role,
                'department': department,
                'display_name': display_name,
                'is_active': True,
                'is_staff': True,
            }
        )
        
        # Always update password (in case it changed)
        user.set_password(password)
        user.role = role
        user.department = department
        user.display_name = display_name
        user.is_active = True
        user.is_staff = True
        
        if role == 'super_admin':
            user.is_superuser = True
            
        user.save()
        
        if was_created:
            created += 1
            print(f"✓ Created: {username} ({role})")
        else:
            updated += 1
            print(f"✓ Updated: {username} ({role})")
    
    print(f"\n{'='*50}")
    print(f"Total: {created} created, {updated} updated")
    print(f"All 20 admin accounts migrated successfully!")
    print(f"{'='*50}")

if __name__ == '__main__':
    migrate()
