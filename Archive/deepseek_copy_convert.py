import os
import shutil
import re
from pathlib import Path

def clear_or_create_docs_folder():
    """Clear existing docs folder or create it if it doesn't exist."""
    docs_path = Path("C:/GHOSTBURN_2325/docs")
    
    if docs_path.exists():
        # Clear the docs folder
        for item in docs_path.iterdir():
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)
        print(f"Cleared existing docs folder at {docs_path}")
    else:
        docs_path.mkdir(parents=True, exist_ok=True)
        print(f"Created docs folder at {docs_path}")
    
    return docs_path

def copy_folders_and_files(vault_path, docs_path):
    """Copy specified folders and files from the vault to docs folder."""
    folders_to_copy = [
        "Characters",
        "Conditions", 
        "Cybernetic_Augmentations",
        "Gear",
        "Health_and_Healing",
        "Keywords",
        "Making_a_roll",
        "Skills_and_Tricks",
        "stylesheets",
        "Turns"
    ]
    
    files_to_copy = ["mkdocs.yml"]
    
    exclusions = [".git", ".obsidian", "Archive", "assets", "site", "docs"]
    
    print("Copying folders and files...")
    
    # Copy folders
    for folder in folders_to_copy:
        src_folder = vault_path / folder
        dst_folder = docs_path / folder
        
        if src_folder.exists():
            # Create destination folder
            dst_folder.mkdir(parents=True, exist_ok=True)
            
            # Copy all files in the folder, excluding specific patterns
            for item in src_folder.iterdir():
                # Skip excluded items
                if item.name in exclusions:
                    continue
                if item.name == ".gitignore":
                    continue
                if item.suffix == ".py":
                    continue
                
                if item.is_file():
                    shutil.copy2(item, dst_folder)
                elif item.is_dir():
                    shutil.copytree(item, dst_folder / item.name, dirs_exist_ok=True)
            
            print(f"  Copied: {folder}")
        else:
            print(f"  Warning: Folder not found - {folder}")
    
    # Copy specific files
    for file_name in files_to_copy:
        src_file = vault_path / file_name
        dst_file = docs_path / file_name
        
        if src_file.exists():
            shutil.copy2(src_file, dst_file)
            print(f"  Copied: {file_name}")
        else:
            print(f"  Warning: File not found - {file_name}")
    
    print("Copy completed successfully!")

def convert_links_in_file(file_path):
    """
    Convert Obsidian links to mkdocs-compatible links.
    Handles both bracketed and non-bracketed links.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern for links with escaped brackets: \[\[[^\]]+\]\] (like \[\[Characters/Char_Backgrounds|Background\]\])
    # Pattern for regular links: \[\[[^\]]+\]\] (like [[Characters/Char_Backgrounds|Background]])
    
    # Combined pattern to match both types of links
    # This pattern matches [[...]] or \[\[...\]\]
    link_pattern = r'(\\?)\[\[([^\]\n]+)\]\]'
    
    def replace_link(match):
        escaped = match.group(1)  # Either '' or '\'
        link_content = match.group(2)
        
        # Split link into path and alias if pipe exists
        if '|' in link_content:
            link_path, alias = link_content.split('|', 1)
        else:
            link_path = link_content
            alias = None
        
        # Remove file extension if present
        if link_path.endswith('.md'):
            link_path = link_path[:-3]
        
        # Check if the link contains a folder path
        if '/' in link_path:
            # Extract just the filename
            filename = link_path.split('/')[-1]
            
            # For mkdocs, we typically use relative paths without .md extension
            # Format: [alias](filename) or [filename](filename)
            if alias:
                return f'[{alias}]({filename})'
            else:
                return f'[{filename}]({filename})'
        else:
            # No folder path in link
            if alias:
                return f'[{alias}]({link_path})'
            else:
                return f'[{link_path}]({link_path})'
    
    # Apply the replacement
    new_content = re.sub(link_pattern, replace_link, content)
    
    # Write back to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  Converted links in: {file_path.name}")
    return new_content != content  # Return True if changes were made

def main():
    vault_path = Path("C:/GHOSTBURN_2325")
    docs_path = clear_or_create_docs_folder()
    
    # Step 1: Copy folders and files
    copy_folders_and_files(vault_path, docs_path)
    
    # Step 2: Convert links in the specified file only
    print("\nConverting links in Characters/Char_NPCs.md only...")
    
    char_npcs_path = docs_path / "Characters" / "Char_NPCs.md"
    
    if char_npcs_path.exists():
        changes_made = convert_links_in_file(char_npcs_path)
        if changes_made:
            print("  Successfully converted links!")
        else:
            print("  No links found to convert.")
    else:
        print(f"  Warning: File not found - {char_npcs_path}")
    
    print("\nProcess completed successfully!")
    print(f"Files copied to: {docs_path}")
    print("Note: Only Char_NPCs.md was processed for link conversion.")

if __name__ == "__main__":
    main()