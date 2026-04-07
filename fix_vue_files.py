#!/usr/bin/env python
"""Fix Vue files: add script setup and fix class naming"""
import os

components_dir = r"c:\Users\ADMIN\OneDrive\Documents\SAD_System_files\version4_technopath\frontend\src\components\admin"

# Files that need fixing
files_to_fix = [
    "AdminAccounts.vue",
    "AdminAuditLog.vue",
    "AdminFacilities.vue",
    "AdminFAQ.vue",
    "AdminFeedback.vue",
    "AdminNavGraph.vue",
    "AdminSendNotification.vue",
    "AdminRooms.vue",
]

for filename in files_to_fix:
    filepath = os.path.join(components_dir, filename)
    basename = filename.replace('.vue', '').lower()
    
    if not os.path.exists(filepath):
        print(f"✗ {filename} not found")
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already has script setup
    if '<script setup>' in content:
        print(f"✓ {filename} already has <script setup>")
        continue
    
    # Check if has generic admin-section class
    if 'class="admin-section"' in content:
        new_content = content.replace(
            'class="admin-section"',
            'class="' + basename + '-section"'
        ).replace(
            '.admin-section {',
            '.' + basename + '-section {'
        )
        
        # Add script setup before </template> closing
        if '</template>' in new_content and '<script' not in new_content:
            script_comment = filename.replace('.vue', '') + ' component'
            new_content = new_content.replace(
                '</template>',
                '</template>\n\n<script setup>\n// ' + script_comment + '\n</script>'
            )
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✓ Fixed {filename}")
    else:
        print(f"  {filename} doesn't have generic admin-section class")

print("\nDone!")
