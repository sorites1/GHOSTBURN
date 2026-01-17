import re
import os

# Paths
input_file = r"C:\GHOSTBURN_2325\Skills and Tricks\Keywords.md"
output_dir = r"C:\GHOSTBURN_2325\Keywords"

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Read the keywords file
with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the table section (starts after "| Keyword" header row and divider row)
# Split by lines and find where the actual data rows start
lines = content.split('\n')

# Find the table start (look for the header row)
table_start = None
for i, line in enumerate(lines):
    if line.strip().startswith('| Keyword'):
        # Skip the header and the divider line
        table_start = i + 2
        break

if table_start is None:
    print("Could not find the keywords table!")
    exit(1)

# Process each table row
keyword_count = 0
for line in lines[table_start:]:
    line = line.strip()
    
    # Stop if we hit an empty line or non-table content
    if not line or not line.startswith('|'):
        break
    
    # Split the row into cells
    cells = [cell.strip() for cell in line.split('|')]
    
    # Remove empty cells at start/end (from leading/trailing |)
    cells = [c for c in cells if c]
    
    if len(cells) >= 2:
        keyword_name = cells[0].strip()
        keyword_effect = cells[1].strip()
        
        # Clean up the keyword name (remove any markdown formatting)
        keyword_name_clean = re.sub(r'\\?\[|\]', '', keyword_name)
        
        # Create filename-safe version
        filename = f"Keyword_{keyword_name_clean.replace(' ', '_')}.md"
        filepath = os.path.join(output_dir, filename)
        
        # Create the markdown content
        md_content = f"""## {keyword_name_clean}

{keyword_effect}
"""
        
        # Write the file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        keyword_count += 1
        print(f"Created: {filename}")

print(f"\n✓ Successfully created {keyword_count} keyword files in {output_dir}")
