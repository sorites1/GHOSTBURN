import re
import os
import shutil
from pathlib import Path

"""
def convert_file_content(content):

    # Pattern to match wikilinks with escaped brackets: \[[[link|alias]]\]
    def replace_escaped_wikilink(match):
        link_content = match.group(1)
        
        if '|' in link_content:
            page_path, alias = link_content.split('|', 1)
            display_text = alias.strip()
        else:
            page_path = link_content
            display_text = page_path.replace('_', ' ').strip()
        
        page_path = page_path.strip()
        relative_path = get_relative_path(page_path)
        
        return f"\\[[{display_text}]({relative_path})\\]"
    
    escaped_pattern = r'\\\[\[\[([^\]]+)\]\]\\\]'
    content = re.sub(escaped_pattern, replace_escaped_wikilink, content)
    
    # Handle regular wikilinks [[link]] or [[link|alias]]
    def replace_regular_wikilink(match):
        link_content = match.group(1)
        
        if '|' in link_content:
            page_path, alias = link_content.split('|', 1)
            display_text = alias.strip()
        else:
            page_path = link_content
            display_text = page_path.replace('_', ' ').strip()
        
        page_path = page_path.strip()
        relative_path = get_relative_path(page_path)
        
        return f"[{display_text}]({relative_path})"
    
    simple_pattern = r'\[\[([^\]]+)\]\]'
    content = re.sub(simple_pattern, replace_regular_wikilink, content)
    
    return content
"""

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
    Convert all wikilinks in the content to MkDocs format. - WORKED IN TEST
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

def get_relative_path(page_path):
    """
    Convert a page path to the appropriate relative path.
    """
    # Handle paths with slashes (e.g., "Making_a_Roll/Outcomes")
    if '/' in page_path:
        parts = page_path.split('/')
        folder = parts[0].replace('_', ' ')
        filename = parts[-1] + '.md'
        return f"../{folder}/{filename}"
    
    filename = page_path
    
    # Map prefixes to folders
    if filename.startswith('Condition_'):
        return f"../Conditions/{filename}.md"
    elif filename.startswith('Keyword_'):
        return f"../Keywords/{filename}.md"
    elif filename.startswith('Skill_') or filename.startswith('Trick_'):
        return f"../Skills_and_Tricks/{filename}.md"
    elif filename.startswith('Gear_'):
        return f"../Gear/{filename}.md"
    elif filename in ['Abilities_and_Ability_Scores', 'Backgrounds', 'Burns_and_Hooks', 
                      'Character_Creation', 'NPCs', 'Burns_and_Hooks']:
        return f"../Characters/{filename.replace(' ', '_')}.md"
    elif filename in ['Health_Condition_Effects', 'Hit_Points_and_Conditions', 
                      'Stabilization_DL', 'Sustaining_an_Injury']:
        return f"../Health_and_Healing/{filename}.md"
    elif filename in ['2d10_Probability_Tables', 'Adjusting_the_Difficulty_Level', 
                      'Difficulty_Level', 'End_of_the_Action', 'Luck_Points', 
                      'Making_a_Roll', 'Outcomes', 'Roll_2d10', 'When_to_Roll']:
        return f"../Making_a_Roll/{filename.replace(' ', '_')}.md"
    elif filename in ['Round_Robin_the_Flow_of_the_Game', 'Turn_Etiquette', 
                      'Turn_Length', 'Turn_Order', 'Types_of_Turns', 'Your_Turn']:
        return f"../Turns/{filename}.md"
    elif 'Cybernetic' in filename:
        return f"../Cybernetic_Augmentations/{filename}.md"
    else:
        return f"{filename}.md"

def convert_file(input_path, output_path):
    """Convert a single markdown file."""
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        converted_content = convert_file_content(content)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(converted_content)
        
        return True
    except Exception as e:
        print(f"ERROR converting {input_path}: {e}")
        return False

def setup_full_mkdocs():
    """Set up complete MkDocs environment."""
    docs_dir = Path("docs")
    docs_dir.mkdir(exist_ok=True)
    
    folders = [
        "Characters", "Conditions", "Cybernetic_Augmentations", "Gear",
        "Health_and_Healing", "Keywords", "Making_a_Roll", 
        "Skills_and_Tricks", "Turns"
    ]
    
    file_count = 0
    print("Converting files...")
    print("="*60)
    
    for folder in folders:
        source_folder = Path(folder)
        if not source_folder.exists():
            print(f"[SKIP] Folder not found: {folder}")
            continue
        
        md_files = list(source_folder.rglob("*.md"))
        
        for md_file in md_files:
            relative_path = md_file.relative_to(Path("."))
            output_path = docs_dir / relative_path
            
            if convert_file(md_file, output_path):
                file_count += 1
                print(f"[OK] {relative_path}")
    
    # Create CSS
    css_dir = docs_dir / "stylesheets"
    css_dir.mkdir(exist_ok=True)
    
    css_content = """/* GHOSTBURN 2325 Styling */
table {
    border-collapse: collapse;
    margin: 1em 0;
}
th, td {
    padding: 0.5em;
    border: 1px solid var(--md-default-fg-color--lightest);
}
a[href*="Keyword_"] {
    font-weight: 500;
    color: var(--md-accent-fg-color);
}
"""
    
    with open(css_dir / "custom.css", 'w', encoding='utf-8') as f:
        f.write(css_content)
    print(f"[OK] Created custom.css")
    
    # Copy your original mkdocs.yml (you'll need to create this file separately)
    # For now, create a basic one
    print(f"\n[INFO] Copy your mkdocs.yml to the root directory")
    print(f"[INFO] Make sure it points to docs_dir: docs")
    
    print("\n" + "="*60)
    print(f"CONVERSION COMPLETE! {file_count} files converted")
    print("="*60)
    print("\nNext steps:")
    print("1. Ensure mkdocs.yml is in the root directory")
    print("2. Run: mkdocs serve")
    print("3. Open: http://127.0.0.1:8000")

if __name__ == "__main__":
    setup_full_mkdocs()
