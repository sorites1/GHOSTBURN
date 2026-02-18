#!/usr/bin/env python3
"""
Generate keyword and condition index for GHOSTBURN Lexicon.
Run this from the GHOSTBURN_2325 directory.
"""

import os
from pathlib import Path


def extract_display_name(filename, prefix):
    """
    Extract display name from filename.
    E.g., 'Keyword_Ability_Score.md' -> 'Ability Score'
    """
    # Remove .md extension
    name = filename.replace('.md', '')
    
    # Remove prefix (Keyword_ or Condition_)
    if name.startswith(prefix):
        name = name[len(prefix):]
    
    # Replace underscores with spaces
    return name.replace('_', ' ')


def generate_link(filepath, base_dir, prefix):
    """
    Generate Obsidian-style link for a file.
    E.g., [[Lexicon/Keywords/Keyword_Ability_Score|Ability Score]]
    """
    # Get the relative path from base_dir
    rel_path = filepath.relative_to(base_dir)
    
    # Build the link path (without .md extension)
    link_path = str(rel_path.with_suffix('')).replace('\\', '/')
    
    # Get display name
    display_name = extract_display_name(filepath.name, prefix)
    
    return f"[[{link_path}|{display_name}]]"


def scan_directory(directory, prefix):
    """
    Scan a directory for markdown files and generate links.
    Returns a sorted list of Obsidian-style links.
    """
    links = []
    
    if not directory.exists():
        print(f"Warning: Directory {directory} does not exist")
        return links
    
    for filepath in directory.glob('*.md'):
        if filepath.name.startswith(prefix):
            link = generate_link(filepath, directory.parent.parent, prefix)
            links.append(link)
    
    # Sort alphabetically by display name
    links.sort(key=lambda x: x.split('|')[1].split(']]')[0])
    
    return links


def format_links_as_obsidian(links):
    """
    Format links as comma-separated list with backslash-escaped brackets.
    E.g., \[[[Link1]]\], \[[[Link2]]\]
    """
    formatted = []
    for link in links:
        # Wrap in \[ and \]
        formatted.append(f"\\[{link}\\]")
    
    # Join with commas and space
    return ", ".join(formatted)


def main():
    # Define paths
    base_dir = Path.cwd()
    lexicon_dir = base_dir / 'Lexicon'
    keywords_dir = lexicon_dir / 'Keywords'
    conditions_dir = lexicon_dir / 'Conditions'
    index_file = lexicon_dir / 'index.md'
    
    # Check if index file exists
    if not index_file.exists():
        print(f"Error: {index_file} does not exist")
        return
    
    # Read existing content
    with open(index_file, 'r', encoding='utf-8') as f:
        existing_content = f.read()
    
    # Scan directories
    print("Scanning Keywords directory...")
    keyword_links = scan_directory(keywords_dir, 'Keyword_')
    print(f"Found {len(keyword_links)} keywords")
    
    print("Scanning Conditions directory...")
    condition_links = scan_directory(conditions_dir, 'Condition_')
    print(f"Found {len(condition_links)} conditions")
    
    # Format the links
    keywords_text = format_links_as_obsidian(keyword_links)
    conditions_text = format_links_as_obsidian(condition_links)
    
    # Build the new sections
    new_content = existing_content.rstrip() + "\n\n"
    new_content += "## Conditions\n\n"
    new_content += conditions_text + "\n"
    new_content += "## Keywords\n\n"
    new_content += keywords_text + "\n\n"    
    
    # Write back to file
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"\nSuccessfully updated {index_file}")
    print(f"Added {len(keyword_links)} keywords and {len(condition_links)} conditions")


if __name__ == '__main__':
    main()