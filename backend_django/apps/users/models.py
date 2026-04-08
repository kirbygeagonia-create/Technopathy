from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from datetime import timedelta
import json


class AdminUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('Username is required')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('role', 'super_admin')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)


class AdminUser(AbstractBaseUser, PermissionsMixin):

    ROLE_CHOICES = [
        ('super_admin',   'System Administrator'),
        ('dean',          'College Dean'),
        ('program_head',  'College Program Head'),
        ('basic_ed_head', 'Basic Education Head'),
    ]

    DEPARTMENT_CHOICES = [
        # ── Administrative ────────────────────────────────────
        ('safety_security',          'Safety and Security Office'),
        ('office_of_the_dean',       'Office of the Dean'),
        # ── College departments ───────────────────────────────
        ('college_agriculture',      'College of Agriculture and Fisheries'),
        ('college_criminology',      'College of Criminal Justice Education'),
        ('college_business',         'College of Business and Good Governance'),
        ('college_ict',              'College of Information and Communication Technology'),
        ('dept_civil_engineering',   'Department of Civil Engineering'),
        ('college_teacher_education','College of Teacher Education'),
        ('tesda',                    'Technical Education and Skills Development Authority (TESDA)'),
        ('general_education',        'General Education Department'),
        # ── Basic Education ───────────────────────────────────
        ('basic_education',          'Basic Education Department'),
    ]

    # Department display colors for announcement labels on mobile
    DEPARTMENT_COLORS = {
        'safety_security':          'red',
        'office_of_the_dean':       'dark_blue',
        'college_agriculture':      'green',
        'college_criminology':      'charcoal',
        'college_business':         'purple',
        'college_ict':              'teal',
        'dept_civil_engineering':   'amber',
        'college_teacher_education':'blue',
        'tesda':                    'dark_green',
        'general_education':        'indigo',
        'basic_education':          'brown',
    }

    username         = models.CharField(max_length=150, unique=True)
    email            = models.EmailField(blank=True, null=True)
    display_name     = models.CharField(
        max_length=200, blank=True, null=True,
        help_text='Full name or title shown in audit logs and admin panel'
    )
    role             = models.CharField(max_length=20, choices=ROLE_CHOICES, default='program_head')
    department       = models.CharField(
        max_length=50, choices=DEPARTMENT_CHOICES, blank=True, null=True
    )
    department_label = models.CharField(
        max_length=200, blank=True, null=True,
        help_text='Override label shown on announcements. Auto-filled from department if blank.'
    )

    is_active        = models.BooleanField(default=True)
    is_staff         = models.BooleanField(default=False)
    login_attempts   = models.IntegerField(default=0)
    locked_until     = models.DateTimeField(blank=True, null=True)
    last_login       = models.DateTimeField(blank=True, null=True)
    show_email_public = models.BooleanField(default=False, help_text='Allow email to be shown in public directory')
    office_location  = models.CharField(max_length=100, blank=True, null=True, help_text='Office location for public directory')
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)

    objects = AdminUserManager()
    USERNAME_FIELD  = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'admin_users'

    def clean(self):
        super().clean()
        from django.core.exceptions import ValidationError
        if self.role == 'dean' and self.department:
            # Enforce 1 dean per department
            qs = AdminUser.objects.filter(role='dean', department=self.department)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError({
                    'department': f"A Dean account already exists for department {self.get_department_display()}."
                })

    # ── Label helpers ─────────────────────────────────────────

    def get_department_label(self):
        if self.department_label:
            return self.department_label
        for code, label in self.DEPARTMENT_CHOICES:
            if code == self.department:
                return label
        return self.get_role_display()

    def get_department_color(self):
        return self.DEPARTMENT_COLORS.get(self.department, 'orange')

    # ── Security helpers ──────────────────────────────────────

    def is_locked(self):
        return bool(self.locked_until and timezone.now() < self.locked_until)

    def record_failed_login(self):
        self.login_attempts += 1
        if self.login_attempts >= 5:
            self.locked_until = timezone.now() + timedelta(minutes=30)
        self.save(update_fields=['login_attempts', 'locked_until'])

    def record_successful_login(self):
        self.login_attempts = 0
        self.locked_until   = None
        self.last_login     = timezone.now()
        self.save(update_fields=['login_attempts', 'locked_until', 'last_login'])

    # ── Permission helpers (used by views AND returned to frontend) ──

    def can_manage_facilities(self):
        return self.role == 'super_admin'

    def can_manage_all_rooms(self):
        return self.role == 'super_admin'

    def can_manage_own_rooms(self):
        return self.role in ('program_head', 'basic_ed_head', 'dean')

    def can_manage_navigation(self):
        return self.role == 'super_admin'

    def can_manage_faq(self):
        return self.role == 'super_admin'

    def can_manage_admin_accounts(self):
        return self.role == 'super_admin'

    def can_view_audit_log(self):
        """Dean can only view audit logs for their own department."""
        return self.role in ('super_admin',)

    def can_view_dept_audit_log(self):
        """Dean can view audit logs for their own department only."""
        return self.role == 'dean' and self.department

    def can_view_all_feedback(self):
        """Only Super Admin can view all feedback."""
        return self.role == 'super_admin'

    def can_view_dept_feedback(self):
        """Dean can view feedback for their own department only."""
        return self.role == 'dean' and self.department

    def can_approve_announcements(self):
        """Only Super Admin can approve announcements. Dean has no approval authority."""
        return self.role == 'super_admin'

    def can_publish_directly(self):
        """
        Super Admin: always
        Dean: only for department-scoped announcements (campus-wide requires approval)
        Program Head/Basic Ed Head: never (always requires approval)
        """
        if self.role == 'super_admin':
            return True
        if self.role == 'dean':
            # Dean can only publish directly to their department
            # Campus-wide announcements require Super Admin approval
            return True  # The check for scope is done in the view
        return False

    def can_post_dept_announcement(self):
        """Dean can post department-scoped announcements without approval."""
        return self.role == 'dean' and self.department

    def can_post_campus_announcement(self):
        """Dean can post campus-wide but it requires Super Admin approval."""
        return self.role == 'dean'

    def can_post_announcement(self):
        return self.role in ('super_admin', 'dean', 'program_head', 'basic_ed_head')

    def can_send_campus_notification(self):
        return self.role == 'super_admin'

    def get_permissions_dict(self):
        """Return all permission flags as a dict for the JWT login response."""
        return {
            'can_manage_facilities':       self.can_manage_facilities(),
            'can_manage_all_rooms':        self.can_manage_all_rooms(),
            'can_manage_own_rooms':        self.can_manage_own_rooms(),
            'can_manage_navigation':       self.can_manage_navigation(),
            'can_manage_faq':              self.can_manage_faq(),
            'can_manage_admin_accounts':   self.can_manage_admin_accounts(),
            'can_view_audit_log':          self.can_view_audit_log(),
            'can_view_dept_audit_log':     self.can_view_dept_audit_log(),
            'can_view_all_feedback':       self.can_view_all_feedback(),
            'can_view_dept_feedback':      self.can_view_dept_feedback(),
            'can_approve_announcements':   self.can_approve_announcements(),
            'can_publish_directly':        self.can_publish_directly(),
            'can_post_announcement':       self.can_post_announcement(),
            'can_post_dept_announcement':  self.can_post_dept_announcement(),
            'can_post_campus_announcement':self.can_post_campus_announcement(),
            'can_send_campus_notification':self.can_send_campus_notification(),
            'department':                  self.department,
            'role':                        self.role,
        }

    def __str__(self):
        return f'{self.display_name or self.username} — {self.get_department_label()}'
