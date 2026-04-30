from django.core.management.base import BaseCommand
from apps.users.models import AdminUser


class Command(BaseCommand):
    help = 'Create all 20 TechnoPath admin accounts with password admin123'

    def handle(self, *args, **options):
        admins = [
            ('safety_admin', 'safety@seait.edu.ph', 'SUPER_ADMIN', 'Safety and Security Office'),
            ('dean_seait', 'dean@seait.edu.ph', 'DEAN', 'Office of the Dean'),
            ('dean_agriculture', 'agri.dean@seait.edu.ph', 'DEAN', 'College of Agriculture'),
            ('dean_criminology', 'crim.dean@seait.edu.ph', 'DEAN', 'College of Criminology'),
            ('dean_business', 'business.dean@seait.edu.ph', 'DEAN', 'College of Business'),
            ('dean_ict', 'ict.dean@seait.edu.ph', 'DEAN', 'College of ICT'),
            ('dean_civil_eng', 'civil.dean@seait.edu.ph', 'DEAN', 'Civil Engineering'),
            ('dean_teacher_ed', 'teached.dean@seait.edu.ph', 'DEAN', 'Teacher Education'),
            ('dean_tesda', 'tesda.dean@seait.edu.ph', 'DEAN', 'TESDA'),
            ('dean_gen_ed', 'gened.dean@seait.edu.ph', 'DEAN', 'General Education'),
            ('dean_basic_ed', 'basiced.dean@seait.edu.ph', 'DEAN', 'Basic Education'),
            ('head_agriculture', 'agri.head@seait.edu.ph', 'PROGRAM_HEAD', 'College of Agriculture'),
            ('head_criminology', 'crim.head@seait.edu.ph', 'PROGRAM_HEAD', 'College of Criminology'),
            ('head_business', 'business.head@seait.edu.ph', 'PROGRAM_HEAD', 'College of Business'),
            ('head_ict', 'ict.head@seait.edu.ph', 'PROGRAM_HEAD', 'College of ICT'),
            ('head_civil_eng', 'civil.head@seait.edu.ph', 'PROGRAM_HEAD', 'Civil Engineering'),
            ('head_teacher_ed', 'teached.head@seait.edu.ph', 'PROGRAM_HEAD', 'Teacher Education'),
            ('head_tesda', 'tesda.head@seait.edu.ph', 'PROGRAM_HEAD', 'TESDA'),
            ('head_gen_ed', 'gened.head@seait.edu.ph', 'PROGRAM_HEAD', 'General Education'),
            ('head_basic_ed', 'basiced.head@seait.edu.ph', 'PROGRAM_HEAD', 'Basic Education'),
        ]

        created = 0
        updated = 0

        for username, email, role, department in admins:
            try:
                user, was_created = AdminUser.objects.get_or_create(
                    username=username,
                    defaults={
                        'email': email,
                        'role': role,
                        'department': department,
                        'is_active': True,
                        'is_staff': True,
                    }
                )
                user.set_password('admin123')
                user.save()

                if was_created:
                    created += 1
                    self.stdout.write(self.style.SUCCESS(f'Created: {username} ({role})'))
                else:
                    updated += 1
                    self.stdout.write(self.style.WARNING(f'Updated password: {username}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error with {username}: {e}'))

        self.stdout.write(self.style.SUCCESS(f'\nDone! Created {created} users, updated {updated} passwords.'))
        self.stdout.write(self.style.SUCCESS('All accounts now have password: admin123'))
