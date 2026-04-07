from django.core.management.base import BaseCommand
from apps.users.models import AdminUser

DEFAULT_ADMINS = [
    # ── Super Admin ───────────────────────────────────────────
    {
        'username':       'safety_admin',
        'password':       'TechnoPath@Safety2024!',
        'role':           'super_admin',
        'department':     'safety_security',
        'display_name':   'Safety and Security Office',
        'is_staff':       True,
        'is_superuser':   True,
    },
    # ── Dean ─────────────────────────────────────────────────
    {
        'username':       'dean_seait',
        'password':       'TechnoPath@Dean2024!',
        'role':           'dean',
        'department':     'office_of_the_dean',
        'display_name':   'Office of the Dean',
        'is_staff':       True,
    },
    # ── College Deans ─────────────────────────────────────────
    {
        'username':       'dean_agriculture',
        'password':       'TechnoPath@AgriDean2024!',
        'role':           'dean',
        'department':     'college_agriculture',
        'display_name':   'Dean — College of Agriculture and Fisheries',
        'is_staff':       True,
    },
    {
        'username':       'dean_criminology',
        'password':       'TechnoPath@CrimDean2024!',
        'role':           'dean',
        'department':     'college_criminology',
        'display_name':   'Dean — College of Criminal Justice Education',
        'is_staff':       True,
    },
    {
        'username':       'dean_business',
        'password':       'TechnoPath@BusDean2024!',
        'role':           'dean',
        'department':     'college_business',
        'display_name':   'Dean — College of Business and Good Governance',
        'is_staff':       True,
    },
    {
        'username':       'dean_ict',
        'password':       'TechnoPath@ICTDean2024!',
        'role':           'dean',
        'department':     'college_ict',
        'display_name':   'Dean — College of Information and Communication Technology',
        'is_staff':       True,
    },
    {
        'username':       'dean_civil_eng',
        'password':       'TechnoPath@CivEngDean2024!',
        'role':           'dean',
        'department':     'dept_civil_engineering',
        'display_name':   'Dean — Department of Civil Engineering',
        'is_staff':       True,
    },
    {
        'username':       'dean_teacher_ed',
        'password':       'TechnoPath@TeachEdDean2024!',
        'role':           'dean',
        'department':     'college_teacher_education',
        'display_name':   'Dean — College of Teacher Education',
        'is_staff':       True,
    },
    {
        'username':       'dean_tesda',
        'password':       'TechnoPath@TESDADean2024!',
        'role':           'dean',
        'department':     'tesda',
        'display_name':   'Dean — TESDA',
        'is_staff':       True,
    },
    {
        'username':       'dean_gen_ed',
        'password':       'TechnoPath@GenEdDean2024!',
        'role':           'dean',
        'department':     'general_education',
        'display_name':   'Dean — General Education Department',
        'is_staff':       True,
    },
    # ── Basic Education Dean ──────────────────────────────────
    {
        'username':       'dean_basic_ed',
        'password':       'TechnoPath@BasicEdDean2024!',
        'role':           'dean',
        'department':     'basic_education',
        'display_name':   'Dean — Basic Education (Elem / JHS / SHS)',
        'is_staff':       True,
    },
    # ── College Program Heads ─────────────────────────────────
    {
        'username':       'head_agriculture',
        'password':       'TechnoPath@Agri2024!',
        'role':           'program_head',
        'department':     'college_agriculture',
        'display_name':   'Program Head — College of Agriculture and Fisheries',
        'is_staff':       True,
    },
    {
        'username':       'head_criminology',
        'password':       'TechnoPath@Crim2024!',
        'role':           'program_head',
        'department':     'college_criminology',
        'display_name':   'Program Head — College of Criminal Justice Education',
        'is_staff':       True,
    },
    {
        'username':       'head_business',
        'password':       'TechnoPath@Bus2024!',
        'role':           'program_head',
        'department':     'college_business',
        'display_name':   'Program Head — College of Business and Good Governance',
        'is_staff':       True,
    },
    {
        'username':       'head_ict',
        'password':       'TechnoPath@ICT2024!',
        'role':           'program_head',
        'department':     'college_ict',
        'display_name':   'Program Head — College of Information and Communication Technology',
        'is_staff':       True,
    },
    {
        'username':       'head_civil_eng',
        'password':       'TechnoPath@CivEng2024!',
        'role':           'program_head',
        'department':     'dept_civil_engineering',
        'display_name':   'Program Head — Department of Civil Engineering',
        'is_staff':       True,
    },
    {
        'username':       'head_teacher_ed',
        'password':       'TechnoPath@TeachEd2024!',
        'role':           'program_head',
        'department':     'college_teacher_education',
        'display_name':   'Program Head — College of Teacher Education',
        'is_staff':       True,
    },
    {
        'username':       'head_tesda',
        'password':       'TechnoPath@TESDA2024!',
        'role':           'program_head',
        'department':     'tesda',
        'display_name':   'TESDA Coordinator — SEAIT',
        'is_staff':       True,
    },
    {
        'username':       'head_gen_ed',
        'password':       'TechnoPath@GenEd2024!',
        'role':           'program_head',
        'department':     'general_education',
        'display_name':   'Program Head — General Education Department',
        'is_staff':       True,
    },
    # ── Basic Education Head ──────────────────────────────────
    {
        'username':       'head_basic_ed',
        'password':       'TechnoPath@BasicEd2024!',
        'role':           'basic_ed_head',
        'department':     'basic_education',
        'display_name':   'Department Head — Basic Education (Elem / JHS / SHS)',
        'is_staff':       True,
    },
]

class Command(BaseCommand):
    help = 'Seed all default SEAIT admin accounts for TechnoPath'

    def handle(self, *args, **kwargs):
        created = 0
        for d in DEFAULT_ADMINS:
            username = d.pop('username')
            password = d.pop('password')
            if not AdminUser.objects.filter(username=username).exists():
                AdminUser.objects.create_user(username=username, password=password, **d)
                self.stdout.write(self.style.SUCCESS(f'  Created: {username}'))
                created += 1
            else:
                self.stdout.write(f'  Exists:  {username}')
        self.stdout.write(self.style.SUCCESS(f'\nDone. {created} new admin account(s) created.'))
        self.stdout.write('\nDefault credentials are in this seed file.')
        self.stdout.write('IMPORTANT: Change all passwords after first login in production.')
