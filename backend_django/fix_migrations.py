import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'technopath.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.db import connection
from datetime import datetime

cursor = connection.cursor()

# Check if announcements migration exists
cursor.execute("SELECT COUNT(*) FROM django_migrations WHERE app = 'announcements' AND name = '0001_initial'")
count = cursor.fetchone()[0]

if count == 0:
    now = datetime.now().isoformat()
    cursor.execute(
        "INSERT INTO django_migrations (app, name, applied) VALUES (%s, %s, %s)",
        ['announcements', '0001_initial', now]
    )
    print("✓ Added announcements.0001_initial to migration history")
else:
    print("✓ announcements.0001_initial already in migration history")

# Verify
cursor.execute("SELECT app, name FROM django_migrations WHERE app IN ('announcements', 'notifications', 'users', 'core') ORDER BY app, name")
rows = cursor.fetchall()
print("\nCurrent migration state:")
for app, name in rows:
    print(f"  {app}.{name}")
