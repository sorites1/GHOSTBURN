import re
import os
import shutil
from pathlib import Path

def convert_wikilink(match, current_file_folder):
    """
    Convert a single wikilink to MkDocs format.
    Handles both [[page]] and [[page|alias]] formats,
    with or without escaped brackets around them.
    """
    full_match = match.group(0)
    
    # Check if we have escaped brackets at the start and end
    has_escaped_brackets = full_match.startswith('\\[') and full_match.endswith('\\]')
    
    # Extract the link content (remove all brackets and backslashes)
    if has_escaped_brackets:
        # Remove \[ and \] from the ends, then remove [[ and ]]
        link_content = full_match[2:-2]  # Remove \[ from start and \] from end
        link_content = link_content[2:-2]  # Remove [[ from start and ]] from end
    else:
        # Just remove [[ and ]]
        link_content = match.group(1)
    
    # Check if link has an alias
    if '|' in link_content:
        page_path, alias = link_content.split('|', 1)
        display_text = alias
    else:
        page_path = link_content
        # Use the page name as display text
        display_text = page_path.replace('_', ' ')
    
    # Clean up the page path
    page_path = page_path.strip()
    display_text = display_text.strip()
    
    # Convert filename: replace spaces with underscores, add .md
    filename = page_path.replace(' ', '_') + '.md'
    
    # Since all files are in the same Characters folder, use relative path
    relative_path = filename
    
    # Create the markdown link
    markdown_link = f"[{display_text}]({relative_path})"
    
    # Check if the original had escaped brackets around it
    if has_escaped_brackets:
        return f"\\[{markdown_link}\\]"
    else:
        return markdown_link

def convert_file_content(content, current_file_folder):
    """
    Convert all wikilinks in the content to MkDocs format.
    """
    # Pattern to match wikilinks with escaped brackets: \[[[link|alias]]\]
    # This pattern specifically looks for the complete structure
    def replace_escaped_wikilink(match):
        link_content = match.group(1)  # Content between [[[ and ]]]
        
        # Check if link has an alias
        if '|' in link_content:
            page_path, alias = link_content.split('|', 1)
            display_text = alias.strip()
        else:
            page_path = link_content
            display_text = page_path.replace('_', ' ').strip()
        
        page_path = page_path.strip()
        filename = page_path.replace(' ', '_') + '.md'
        
        return f"\\[[{display_text}]({filename})\\]"
    
    # First pass: handle escaped bracket wikilinks \[[[link|alias]]\]
    escaped_pattern = r'\\\[\[\[([^\]]+)\]\]\\\]'
    content = re.sub(escaped_pattern, replace_escaped_wikilink, content)
    
    # Second pass: handle regular wikilinks [[link]] or [[link|alias]]
    def replace_regular_wikilink(match):
        link_content = match.group(1)
        
        if '|' in link_content:
            page_path, alias = link_content.split('|', 1)
            display_text = alias.strip()
        else:
            page_path = link_content
            display_text = page_path.replace('_', ' ').strip()
        
        page_path = page_path.strip()
        filename = page_path.replace(' ', '_') + '.md'
        
        return f"[{display_text}]({filename})"
    
    simple_pattern = r'\[\[([^\]]+)\]\]'
    content = re.sub(simple_pattern, replace_regular_wikilink, content)
    
    return content

def setup_test_mkdocs():
    """
    Set up a minimal MkDocs test environment with 3 files.
    """
    # Define paths
    source_dir = Path("Characters")
    output_dir = Path("docs/Characters")
    css_source = Path("stylesheets/custom.css")
    css_dest = Path("docs/stylesheets/custom.css")
    
    # Create output directories
    output_dir.mkdir(parents=True, exist_ok=True)
    css_dest.parent.mkdir(parents=True, exist_ok=True)
    
    # Files to convert
    test_files = [
        "Character_Creation_test.md",
        "Backgrounds.md",
        "Burns_and_Hooks.md"
    ]
    
    print("Converting files...")
    for filename in test_files:
        input_path = source_dir / filename
        output_path = output_dir / filename
        
        if not input_path.exists():
            print(f"WARNING: {input_path} not found, skipping...")
            continue
        
        # Read the file
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Convert wikilinks
        converted_content = convert_file_content(content, "Characters")
        
        # Write to output
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(converted_content)
        
        print(f"[OK] Converted: {filename}")
    
    # Create a basic CSS file for proof of concept
    basic_css = """/* GHOSTBURN 2325 - Basic Styling */

/* Make tables more readable */
table {
    border-collapse: collapse;
    margin: 1em 0;
}

th, td {
    padding: 0.5em;
    border: 1px solid var(--md-default-fg-color--lightest);
}

/* Highlight keywords in brackets */
a[href*="Keyword_"] {
    font-weight: 500;
    color: var(--md-accent-fg-color);
}
"""
    
    with open(css_dest, 'w', encoding='utf-8') as f:
        f.write(basic_css)
    print(f"[OK] Created: custom.css (basic styling)")
    
    # Create minimal mkdocs.yml
    mkdocs_content = """site_name: GHOSTBURN 2325 Test
site_description: GHOSTBURN 2325 System Reference Document 1.0 - Test Setup
site_author: Justin Smith
docs_dir: docs

theme:
  name: material
  palette:
  - scheme: default
    primary: indigo
    accent: indigo
    toggle:
      icon: material/brightness-7
      name: Switch to dark mode
  - scheme: slate
    primary: indigo
    accent: indigo
    toggle:
      icon: material/brightness-4
      name: Switch to light mode
  features:
  - navigation.tabs
  - navigation.sections
  - navigation.expand
  - navigation.top
  - search.suggest
  - search.highlight
  - content.code.copy

markdown_extensions:
- abbr
- admonition
- attr_list
- def_list
- footnotes
- md_in_html
- tables
- toc:
    permalink: true
- pymdownx.arithmatex:
    generic: true
- pymdownx.betterem
- pymdownx.caret
- pymdownx.details
- pymdownx.highlight:
    anchor_linenums: true
- pymdownx.inlinehilite
- pymdownx.keys
- pymdownx.mark
- pymdownx.smartsymbols
- pymdownx.superfences
- pymdownx.tabbed:
    alternate_style: true
- pymdownx.tasklist:
    custom_checkbox: true
- pymdownx.tilde

plugins:
- search

extra_css:
- stylesheets/custom.css

nav:
- Characters:
  - Character Creation: Characters/Character_Creation_test.md
  - Backgrounds: Characters/Backgrounds.md
  - Burns and Hooks: Characters/Burns_and_Hooks.md
"""
    
    # Write mkdocs.yml
    with open("mkdocs.yml", 'w', encoding='utf-8') as f:
        f.write(mkdocs_content)
    
    print("[OK] Created: mkdocs.yml")
    
    print("\n" + "="*50)
    print("TEST SETUP COMPLETE!")
    print("="*50)
    print("\nTo test your site:")
    print("1. Install MkDocs: pip install mkdocs-material")
    print("2. Run: mkdocs serve")
    print("3. Open: http://127.0.0.1:8000")
    print("\nFiles converted:")
    for f in test_files:
        print(f"  - {f}")

if __name__ == "__main__":
    setup_test_mkdocs()
