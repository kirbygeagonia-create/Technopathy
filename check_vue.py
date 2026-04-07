#!/usr/bin/env python
"""Check Vue files for CSS location and naming conventions"""
import os
import re

admin_components_dir = r"c:\Users\ADMIN\OneDrive\Documents\SAD_System_files\version4_technopath\frontend\src\components\admin"
views_dir = r"c:\Users\ADMIN\OneDrive\Documents\SAD_System_files\version4_technopath\frontend\src\views"

print("=" * 70)
print("VUE FILES VERIFICATION")
print("=" * 70)

issues = []
warnings = []

# Check admin components
vue_files = [f for f in os.listdir(admin_components_dir) if f.endswith('.vue')]

for filename in vue_files:
    filepath = os.path.join(admin_components_dir, filename)
    basename = filename.replace('.vue', '')
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"\n[Checking {filename}]")
    
    # Check for scoped attribute
    if '<style scoped>' in content:
        print("  ✓ Uses scoped CSS")
    elif '<style>' in content:
        warnings.append(f"{filename}: Uses unscoped <style> instead of <style scoped>")
        print("  ⚠ Uses unscoped CSS (should use <style scoped>)")
    else:
        print("  ✗ No <style> section found")
    
    # Check for inline style attributes
    inline_styles = re.findall(r'style="[^"]*"', content)
    if inline_styles:
        issues.append(f"{filename}: Found {len(inline_styles)} inline style attribute(s)")
        print(f"  ✗ Has {len(inline_styles)} inline style attribute(s)")
    else:
        print("  ✓ No inline style attributes")
    
    # Check class naming convention (filename_function format)
    # Expected pattern: basename-lowercase-function (e.g., adminannouncements-card)
    classes = re.findall(r'class="([^"]*)"', content)
    all_classes = ' '.join(classes).split()
    
    prefix_ok = True
    for cls in all_classes:
        # Skip dynamic class bindings and common utility classes
        if cls.startswith('tp-') or cls.startswith('material-icons') or '{' in cls:
            continue
        # Check if class follows naming convention
        expected_prefix = basename.lower()
        if not (cls.startswith(expected_prefix) or cls.startswith('tp-')):
            # Allow some common patterns
            if cls not in ['active', 'pending', 'published', 'rejected', 'archived']:
                prefix_ok = False
                warnings.append(f"{filename}: Class '{cls}' doesn't follow naming convention (expected {expected_prefix}-* or tp-*)")
    
    if prefix_ok:
        print("  ✓ Class naming follows convention")
    else:
        print("  ⚠ Some classes may not follow naming convention")
    
    # Check for id attributes
    ids = re.findall(r'id="([^"]*)"', content)
    if ids:
        print(f"  Found {len(ids)} id attribute(s): {ids}")
    else:
        print("  No id attributes found")
    
    # Syntax check - basic template structure
    if '<template>' in content and '</template>' in content:
        print("  ✓ Template section present")
    else:
        issues.append(f"{filename}: Missing template section")
        print("  ✗ Missing template section")
    
    if '<script setup>' in content:
        print("  ✓ Uses <script setup>")
    elif '<script>' in content:
        print("  ✓ Uses <script>")
    else:
        issues.append(f"{filename}: Missing script section")
        print("  ✗ Missing script section")

# Check views
print("\n" + "=" * 70)
print("CHECKING VIEWS")
print("=" * 70)

view_files = [f for f in os.listdir(views_dir) if f.endswith('.vue')]
for filename in view_files:
    filepath = os.path.join(views_dir, filename)
    basename = filename.replace('.vue', '').lower()
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"\n[Checking {filename}]")
    
    # Check for scoped style
    if '<style scoped>' in content:
        print("  ✓ Uses scoped CSS")
    elif '<style>' in content:
        print("  ⚠ Uses unscoped CSS")
    
    # Check for external CSS import
    if '@import' in content:
        print("  ℹ Uses external CSS import")
    
    # Check for admin-view specific classes
    if 'AdminView.vue' in filename:
        if 'tp-' in content:
            print("  ✓ Uses tp- prefixed classes (TechnoPath naming)")
        else:
            print("  ⚠ AdminView should use tp- prefixed classes")

# Summary
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

if issues:
    print(f"\nERRORS ({len(issues)}):")
    for i in issues:
        print(f"  ✗ {i}")
else:
    print("\n✓ No critical errors found")

if warnings:
    print(f"\nWARNINGS ({len(warnings)}):")
    for w in warnings:
        print(f"  ⚠ {w}")
else:
    print("\n✓ No warnings")

print(f"\nChecked {len(vue_files)} admin components and {len(view_files)} views")
