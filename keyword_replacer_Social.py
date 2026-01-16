import os
import re

# Configuration
search_dir = r"C:\GHOSTBURN_2325\Skills and Tricks"
search_string = r"\[Social\]"
replace_string = r"\[[[Keyword_Social\|Social]]\]"

# Track changes
files_modified = 0
total_replacements = 0

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
        
        # Count occurrences before replacement
        count = content.count(search_string)
        
        if count > 0:
            # Perform replacement
            new_content = content.replace(search_string, replace_string)
            
            # Write back to file
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                files_modified += 1
                total_replacements += count
                print(f"✓ {filename}: {count} replacement(s)")
            except Exception as e:
                print(f"Error writing {filename}: {e}")

# Summary
print(f"\n{'='*50}")
print(f"Modified {files_modified} file(s)")
print(f"Total replacements: {total_replacements}")
print(f"{'='*50}")
