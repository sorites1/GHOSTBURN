import os
import re

# Configuration
search_dir = r"C:\GHOSTBURN_2325\Skills and Tricks"

# All keywords to replace
# Format: keyword name (as it appears in \[KeywordName\])
keywords = [
    "Absolute Damage",
    "Admin",
    "Advanced Supplies",
    "Attack",
    "Auditory",
    "Basic",
    "Close",
    "Concentrate",
    "Contact",
    "Control Deck",
    "Counterattack",
    "Crashes",
    "Cyber Rig",
    "Datajack",
    "Damage Array",
    "Disabled",
    "Downgraded",
    "Drone",
    "Enabled",
    "Far",
    "Fine Control",
    "Fly",
    "Fort",
    "Gift",
    "Group",
    "Gun",
    "Handling",
    "High Speed",
    "Location",
    "Low Speed",
    "Lucky",
    "Manipulator Arm",
    "Maximum Damage",
    "Melee",
    "Minimum Damage",
    "Moderate Speed",
    "Move",
    "Nearby",
    "Normal Damage",
    "One Hand",
    "Operator",
    "Opposed",
    "Optimal Range",
    "Physical",
    "Range",
    "Reaction",
    "Scope",
    "Secret",
    "Security",
    "Security Alert",
    "Silencer",
    "Small Item",
    "Stability",
    "Stabilization DL",
    "Supplies",
    "Surgical Procedure",
    "Temporary",
    "Threat",
    "Tools",
    "Two Hands",
    "Unarmed Strike",
    "Upgraded",
    "Vehicle",
    "Vicinity",
    "Visible",
    "Visual",
    "Vocal",
    "Wireless",
    "Wits"
]

# Track changes
files_modified = set()
total_replacements = 0
replacements_by_keyword = {}

# Walk through all files in the directory and subdirectories
for root, dirs, files in os.walk(search_dir):
    for filename in files:
        # Only process markdown files
        if not filename.endswith('.md'):
            continue
        
        filepath = os.path.join(root, filename)
        
        # Read the file
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            continue
        
        original_content = content
        file_replacements = 0
        
        # Process each keyword
        for keyword in keywords:
            # Create the filename-safe version for the link
            keyword_filename = keyword.replace(' ', '_')
            
            # Search string: \[KeywordName\]
            search_string = f"\\[{keyword}\\]"
            
            # Replace string: \[[[Keyword_KeywordName|KeywordName]]\]
            replace_string = f"\\[[[Keyword_{keyword_filename}|{keyword}]]\\]"
            
            # Count and replace
            count = content.count(search_string)
            if count > 0:
                content = content.replace(search_string, replace_string)
                file_replacements += count
                
                # Track by keyword
                if keyword not in replacements_by_keyword:
                    replacements_by_keyword[keyword] = 0
                replacements_by_keyword[keyword] += count
        
        # Write back if changes were made
        if content != original_content:
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                files_modified.add(filename)
                total_replacements += file_replacements
                print(f"✓ {filename}: {file_replacements} replacement(s)")
            except Exception as e:
                print(f"Error writing {filename}: {e}")

# Summary
print(f"\n{'='*60}")
print(f"Modified {len(files_modified)} file(s)")
print(f"Total replacements: {total_replacements}")
print(f"\nReplacements by keyword:")
for keyword, count in sorted(replacements_by_keyword.items(), key=lambda x: x[1], reverse=True):
    print(f"  {keyword}: {count}")
print(f"{'='*60}")
