#!/usr/bin/env python3
"""
Generate gear and augments index for GHOSTBURN.
Run this from the GHOSTBURN_2325 directory.
"""

import os
import re
from pathlib import Path
from collections import defaultdict


def extract_table_from_file(filepath):
    """
    Extract the first markdown table from a file.
    Returns (header_row, data_rows) or (None, None) if no table found.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the first table (lines starting with |)
    lines = content.split('\n')
    table_lines = []
    in_table = False
    
    for line in lines:
        if line.strip().startswith('|'):
            in_table = True
            table_lines.append(line.rstrip())  # Remove trailing whitespace
        elif in_table:
            # Table ended
            break
    
    if len(table_lines) < 3:  # Need at least header, separator, and one data row
        return None, None
    
    # First line is header, second is separator, rest are data
    header = table_lines[0]
    data_rows = table_lines[2:]  # Skip separator line
    
    return header, data_rows


def escape_pipes_in_brackets(text):
    """
    Escape all pipes that appear inside [ ] brackets, but only if not already escaped.
    E.g., [Link|Text] becomes [Link\|Text]
    But [Link\|Text] stays as [Link\|Text]
    """
    result = []
    in_brackets = False
    i = 0
    
    while i < len(text):
        char = text[i]
        
        if char == '[':
            in_brackets = True
            result.append(char)
            i += 1
        elif char == ']':
            in_brackets = False
            result.append(char)
            i += 1
        elif char == '|' and in_brackets:
            # Check if it's already escaped (preceded by \)
            if i > 0 and text[i-1] == '\\':
                # Already escaped, just add the pipe
                result.append(char)
            else:
                # Not escaped, add escape
                result.append('\\|')
            i += 1
        else:
            result.append(char)
            i += 1
    
    return ''.join(result)


def make_item_name_link(data_row, filepath, base_dir):
    """
    Convert the item name in the second column to a link.
    Then escape all pipes inside brackets in the entire row.
    """
    # Get the relative path for the link
    rel_path = filepath.relative_to(base_dir).with_suffix('')
    link_path = str(rel_path).replace('\\', '/')
    
    # Split by pipe to find cells
    parts = data_row.split('|')
    
    if len(parts) < 4:  # Need at least: empty, cost, name, something else
        # Still escape pipes in whatever we have
        return escape_pipes_in_brackets(data_row)
    
    # The item name is in parts[2] (0=empty, 1=cost, 2=name)
    item_name = parts[2].strip()
    
    # Create the link
    linked_name = f"[[{link_path}|{item_name}]]"
    parts[2] = f" {linked_name} "
    
    # Rebuild the row
    rebuilt_row = '|'.join(parts)
    
    # Now escape all pipes that are inside brackets
    return escape_pipes_in_brackets(rebuilt_row)


def process_category(category_path, base_dir, category_name):
    """
    Process all markdown files in a category and return consolidated table.
    Returns (header, rows) tuple.
    """
    if not category_path.exists():
        print(f"Warning: {category_path} does not exist")
        return None, []
    
    all_rows = []
    header = None
    
    # Process all .md files in this directory
    for filepath in sorted(category_path.glob('*.md')):
        file_header, data_rows = extract_table_from_file(filepath)
        
        if file_header and data_rows:
            # Use the first file's header as the canonical header
            if header is None:
                header = file_header
            
            # Process each data row to add links
            for row in data_rows:
                linked_row = make_item_name_link(row, filepath, base_dir)
                all_rows.append(linked_row)
    
    return header, all_rows


def create_section_table(header, rows, section_title):
    """
    Create a markdown section with title and table.
    """
    if not rows:
        return ""
    
    # Count the number of columns by splitting on pipes
    # that aren't inside brackets
    num_cols = 0
    in_brackets = False
    for char in header:
        if char == '[':
            in_brackets = True
        elif char == ']':
            in_brackets = False
        elif char == '|' and not in_brackets:
            num_cols += 1
    
    # Subtract 2 for the leading and trailing pipes
    num_cols = num_cols - 1
    
    # Create left-aligned separator row
    separator = '| ' + ' | '.join([':------' for _ in range(num_cols)]) + ' |'
    
    section = f"## {section_title}\n\n"
    section += header + "\n"
    section += separator + "\n"
    section += "\n".join(rows) + "\n\n"
    
    return section


def main():
    base_dir = Path.cwd()
    gear_dir = base_dir / 'Gear_and_Augments'
    index_file = gear_dir / 'index.md'
    
    if not index_file.exists():
        print(f"Error: {index_file} does not exist")
        return
    
    # Read existing content
    with open(index_file, 'r', encoding='utf-8') as f:
        existing_content = f.read()
    
    # Define all categories to process
    categories = [
        # Gear categories
        ('Armor', gear_dir / 'Armor'),
        ('Control Decks', gear_dir / 'Control_Decks'),
        ('Cyber Rigs', gear_dir / 'Cyber_Rigs'),
        ('Recon Drones', gear_dir / 'Drones' / 'Recon_Drones'),
        ('Light Combat Drones', gear_dir / 'Drones' / 'Light_Combat_Drones'),
        ('Light Pistols', gear_dir / 'Firearms' / 'Light_Pistols'),
        ('Heavy Pistols', gear_dir / 'Firearms' / 'Heavy_Pistols'),
        ('Shotguns', gear_dir / 'Firearms' / 'Shotguns'),
        ('SMGs', gear_dir / 'Firearms' / 'SMGs'),
        ('Rifles', gear_dir / 'Firearms' / 'Rifles'),
        ('Blunt Weapons', gear_dir / 'Melee_Weapons' / 'Blunt_Weapons'),
        ('Short Blades', gear_dir / 'Melee_Weapons' / 'Short_Blades'),
        ('Long Blades', gear_dir / 'Melee_Weapons' / 'Long_Blades'),
        ('Miscellaneous Gear', gear_dir / 'Miscellaneous'),
        ('Motorcycles', gear_dir / 'Vehicles' / 'Motorcycles'),
        ('Coupes', gear_dir / 'Vehicles' / 'Coupes'),
        ('Sedans', gear_dir / 'Vehicles' / 'Sedans'),
        ('SUVs', gear_dir / 'Vehicles' / 'SUVs'),
        ('Vans', gear_dir / 'Vehicles' / 'Vans'),
        
        # Augment categories
        ('Body Augments', gear_dir / 'Augments' / 'Body_Augments'),
        ('Combat Augments', gear_dir / 'Augments' / 'Combat_Augments'),
        ('Utility Augments', gear_dir / 'Augments' / 'Utility_Augments'),
    ]
    
    # Build all sections
    new_content = existing_content.rstrip() + "\n\n"
    
    # Add a main Gear header
    new_content += "# ⚏ Gear\n\n"
    
    # Process gear categories (everything before augments)
    for section_title, category_path in categories[:19]:  # First 19 are gear
        print(f"Processing {section_title}...")
        header, rows = process_category(category_path, base_dir, section_title)
        
        if rows:
            section = create_section_table(header, rows, section_title)
            new_content += section
            print(f"  Added {len(rows)} items")
        else:
            print(f"  No items found")
    
    # Add Augments header
    new_content += "# ⚏ Augments\n\n"
    
    # Process augment categories
    for section_title, category_path in categories[19:]:  # Last 3 are augments
        print(f"Processing {section_title}...")
        header, rows = process_category(category_path, base_dir, section_title)
        
        if rows:
            section = create_section_table(header, rows, section_title)
            new_content += section
            print(f"  Added {len(rows)} items")
        else:
            print(f"  No items found")
    
    # Write back to file
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"\nSuccessfully updated {index_file}")


if __name__ == '__main__':
    main()