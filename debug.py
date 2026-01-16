import os
import re

# Configuration
search_dir = r"C:\GHOSTBURN_2325\Skills and Tricks"

# Just look for Move as a test
print("Searching for 'Move' links in Skills and Tricks...\n")

for root, dirs, files in os.walk(search_dir):
    for filename in files:
        if not filename.endswith('.md'):
            continue
        
        filepath = os.path.join(root, filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            continue
        
        # Look for any link to Move
        if 'Keyword_Move' in content:
            print(f"\n{'='*60}")
            print(f"FILE: {filename}")
            print(f"{'='*60}")
            
            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                if 'Keyword_Move' in line:
                    print(f"Line {i}: {line}")
            
            # Count occurrences
            pattern1 = r'\[\[\[Keyword_Move\\\|Move\]\]\]'  # Escaped pipe
            pattern2 = r'\[\[\[Keyword_Move\|Move\]\]\]'     # Unescaped pipe
            
            escaped_count = len(re.findall(pattern1, content))
            unescaped_count = len(re.findall(pattern2, content))
            
            print(f"\nEscaped pipe links (\\|): {escaped_count}")
            print(f"Unescaped pipe links (|): {unescaped_count}")

print("\n" + "="*60)
print("Debug complete")
