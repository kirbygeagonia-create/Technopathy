import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'technopath.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import django
django.setup()

from django.db import connection

cursor = connection.cursor()

# Check if announcements table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='announcements'")
exists = cursor.fetchone()

if exists:
    print("✓ announcements table exists")
    # Check if it has the archived columns
    cursor.execute("PRAGMA table_info(announcements)")
    columns = [row[1] for row in cursor.fetchall()]
    if 'archived_at' in columns:
        print("✓ archived_at column exists")
    else:
        print("✗ archived_at column missing - adding...")
        cursor.execute("ALTER TABLE announcements ADD COLUMN archived_at DATETIME NULL")
        print("✓ Added archived_at column")
    
    if 'archived_by_id' in columns:
        print("✓ archived_by_id column exists")
    else:
        print("✗ archived_by_id column missing - adding...")
        cursor.execute("ALTER TABLE announcements ADD COLUMN archived_by_id INTEGER NULL REFERENCES admin_users(id)")
        print("✓ Added archived_by_id column")
else:
    print("✗ announcements table does not exist!")
    print("Creating table manually...")
    cursor.execute("""
        CREATE TABLE announcements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(200) NOT NULL,
            content TEXT NOT NULL,
            created_by_id INTEGER NULL REFERENCES admin_users(id),
            source_label VARCHAR(200) NOT NULL,
            source_color VARCHAR(20) NOT NULL DEFAULT 'orange',
            scope VARCHAR(20) NOT NULL DEFAULT 'campus_wide',
            target_department VARCHAR(50) NULL,
            status VARCHAR(20) NOT NULL DEFAULT 'pending_approval',
            requires_approval BOOL NOT NULL DEFAULT 1,
            approved_by_id INTEGER NULL REFERENCES admin_users(id),
            rejected_by_id INTEGER NULL REFERENCES admin_users(id),
            rejection_note TEXT NULL,
            approved_at DATETIME NULL,
            archived_by_id INTEGER NULL REFERENCES admin_users(id),
            archived_at DATETIME NULL,
            is_deleted BOOL NOT NULL DEFAULT 0,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("✓ Created announcements table")

# Verify
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='announcements'")
if cursor.fetchone():
    print("\n✓ Table is ready")
else:
    print("\n✗ Table creation failed")
