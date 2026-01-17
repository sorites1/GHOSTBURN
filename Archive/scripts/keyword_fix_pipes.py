import os
import re

# Configuration
search_dir = r"C:\GHOSTBURN_2325\Skills and Tricks"

# Track changes
files_modified = 0
total_fixes = 0

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
                lines = f.readlines()
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            continue
        
        modified = False
        file_fixes = 0
        new_lines = []
        in_table = False
        
        for line in lines:
            original_line = line
            
            # Detect if we're in a table
            # A line is part of a table if it starts with | (after whitespace)
            stripped = line.lstrip()
            if stripped.startswith('|'):
                in_table = True
            elif stripped and not stripped.startswith('|') and in_table:
                # Empty lines or non-table lines after table content
                if stripped.strip() and not stripped.startswith('#'):
                    in_table = False
            
            # If we're in a table, escape unescaped pipes inside wikilinks
            if in_table:
                # Find all wikilinks with unescaped pipes: [[Something|Something]]
                # Pattern: [[text that doesn't contain ]|text]]
                # We want to find pipes that are NOT already escaped
                
                # This regex finds [[...UNESCAPED_PIPE...]]
                # Negative lookbehind (?<!\\) ensures the pipe isn't already escaped
                pattern = r'\[\[([^\]]+?)(?<!\\)\|([^\]]+?)\]\]'
                
                def escape_pipe(match):
                    return f'[[{match.group(1)}\\|{match.group(2)}]]'
                
                new_line = re.sub(pattern, escape_pipe, line)
                
                if new_line != line:
                    fixes = line.count('|') - line.count('\\|') - new_line.count('|') + new_line.count('\\|')
                    file_fixes += abs(fixes)
                    modified = True
                    line = new_line
            
            new_lines.append(line)
        
        # Write back if changes were made
        if modified:
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.writelines(new_lines)
                
                files_modified += 1
                total_fixes += file_fixes
                print(f"✓ {filename}: {file_fixes} pipe(s) escaped")
            except Exception as e:
                print(f"Error writing {filename}: {e}")

# Summary
print(f"\n{'='*60}")
print(f"Modified {files_modified} file(s)")
print(f"Total pipes escaped: {total_fixes}")
print(f"{'='*60}")
