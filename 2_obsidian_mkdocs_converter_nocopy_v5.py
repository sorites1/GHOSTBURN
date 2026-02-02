import os
import re

def convert_obsidian_callouts(text):
    """Convert Obsidian callouts to MkDocs admonitions format."""
    
    # Pattern to match Obsidian callouts
    # > [!TYPE] Title
    # > Content line 1
    # > Content line 2
    
    def replace_callout(match):
        callout_type = match.group(1).lower()  # NOTE, TIP, WARNING, etc.
        title = match.group(2).strip() if match.group(2) else callout_type.capitalize()
        content_lines = match.group(3).strip()
        
        # Remove leading > from content lines and preserve indentation
        content = []
        for line in content_lines.split('\n'):
            line = line.lstrip('> ').rstrip()
            if line:
                content.append('    ' + line)
        
        # Build the MkDocs admonition
        result = f'!!! {callout_type} "{title}"\n'
        result += '\n'.join(content)
        
        return result
    
    # Match callout blocks
    # Pattern: > [!TYPE] Title followed by lines starting with >
    pattern = r'^> \[!([A-Z]+)\](?: (.+?))?\n((?:^>.*\n?)+)'
    text = re.sub(pattern, replace_callout, text, flags=re.MULTILINE)
    
    return text

def convert_obsidian_links(text):
    """Convert Obsidian links to MkDocs format."""
    
    # Pattern 1: Handle escaped brackets with Obsidian links
    # Matches: \[[[path|display]]\] or \[[[path]]\]
    # Uses negative lookahead to avoid matching already-converted links
    def replace_escaped_link(match):
        inner_link = match.group(1)
        # Parse the inner Obsidian link
        if '|' in inner_link:
            path, display = inner_link.split('|', 1)
        else:
            path = inner_link
            display = path.split('/')[-1]  # Use filename as display
        
        # Remove '/index' from the end of the path if present
        if path.endswith('/index'):
            path = path[:-6]  # Remove '/index' (6 characters)
        
        # Convert to MkDocs format and wrap in brackets
        mkdocs_link = f"[{display}](/../{path})"
        return f"[{mkdocs_link}]"
    
    text = re.sub(r'\\\[\[\[([^\]]+)\]\]\\\]', replace_escaped_link, text)
    
    # Pattern 2: Handle regular Obsidian links
    # Matches: [[path|display]] or [[path]]
    # Negative lookahead (?!\() ensures we don't match links that already have (../ after them
    def replace_regular_link(match):
        content = match.group(1)
        
        # Skip if this looks like it's already been converted (contains ](../)
        if '](' in content:
            return match.group(0)  # Return unchanged
        
        if '|' in content:
            path, display = content.split('|', 1)
        else:
            path = content
            display = path.split('/')[-1]  # Use filename as display
        
        # Remove '/index' from the end of the path if present
        if path.endswith('/index'):
            path = path[:-6]  # Remove '/index' (6 characters)
        
        return f"[{display}](/../{path})"
    
    # Only match [[ ]] that are NOT followed by markdown link syntax
    text = re.sub(r'\[\[([^\]]+)\]\](?!\()', replace_regular_link, text)
    
    return text

def process_markdown_file(file_path):
    """Process a single markdown file to convert Obsidian links."""
    try:
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Convert callouts first, then links
        converted_content = convert_obsidian_callouts(content)
        converted_content = convert_obsidian_links(converted_content)
        
        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(converted_content)
        
        return True
    except Exception as e:
        print(f"  Error processing file: {e}")
        return False

def process_folder(folder_path, folder_name):
    """Process all .md files in a folder to convert Obsidian links."""
    if not os.path.exists(folder_path):
        print(f"  Folder not found: {folder_name}")
        return
    
    # Get all .md files in the folder
    md_files = [f for f in os.listdir(folder_path) if f.endswith('.md')]
    
    if not md_files:
        print(f"  No .md files found in {folder_name}")
        return
    
    print(f"  Found {len(md_files)} markdown file(s) in {folder_name}")
    
    for filename in md_files:
        file_path = os.path.join(folder_path, filename)
        if process_markdown_file(file_path):
            print(f"    Processed: {filename}")

def main():
    """Main function to orchestrate the conversion process."""
    vault_path = r'C:\GHOSTBURN_2325'
    docs_path = os.path.join(vault_path, 'docs')
    
    print("Starting Obsidian to MkDocs link conversion...")
    print(f"Vault path: {vault_path}\n")
    
    # Check if docs folder exists
    if not os.path.exists(docs_path):
        print(f"Error: docs folder not found at {docs_path}")
        print("Please ensure the docs folder exists before running this script.")
        return
    
    print(f"Found docs folder: {docs_path}\n")
    
    # List of folders to process
    folders_to_process = [
        'Characters',
        'Conditions',
        'Cybernetic_Augmentations',
        'Game_Master',
        'Gear_Mods',
        'Gear_and_Augments',
        'Firearms',
        'Health_and_Healing',
        'Making_a_Roll',
        'Mods',
        'Keywords',
        'Lexicon',
        'Melee_Weapons',
        'Playing_the_Game',
        'Skills_and_Tricks',
        'Weapon_Mods',
        'Vision_Mods'
    ]
    
    # Process each folder
    print("Processing folders...")
    for folder_name in folders_to_process:
        print(f"\n{folder_name}:")
        folder_path = os.path.join(docs_path, folder_name)
        process_folder(folder_path, folder_name)
    
    print("\nConversion complete!")

if __name__ == "__main__":
    main()