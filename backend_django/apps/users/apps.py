from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'

    def ready(self):
        # Auto-create admin accounts on startup
        from .models import AdminUser

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

        logger.info(f"Starting to create {len(admins)} admin accounts...")
        created_count = 0

        for username, email, role, department in admins:
            try:
                user, created = AdminUser.objects.get_or_create(
                    username=username,
                    defaults={
                        'email': email,
                        'role': role,
                        'department': department,
                        'is_active': True,
                        'is_staff': True,
                    }
                )
                # Always reset password to admin123 on startup
                user.set_password('admin123')
                user.save()
                created_count += 1
                action = "Created" if created else "Updated"
                logger.info(f"{action}: {username} ({role})")
            except Exception as e:
                logger.error(f"Failed to create {username}: {e}")

        logger.info(f"Admin account creation complete. {created_count}/{len(admins)} accounts ready.")
