import os
import re
import shutil
from pathlib import Path
from datetime import datetime

# Configuration
VAULT_PATH = Path(r"C:\GHOSTBURN_2325")
BACKUP_SUFFIX = "_backup_" + datetime.now().strftime("%Y%m%d_%H%M%S")

EXCLUDED_FOLDERS = {".git", ".obsidian", "Archive", "assets", "docs"}

# Folder mapping rules
FOLDER_RULES = {
    "Char_": "Characters",
    "Condition_": "Conditions",
    "Aug_": "Cybernetic_Augmentations",
    "Gear_": "Gear",
    "HaH_": "Health_and_Healing",
    "Keyword_": "Keywords",
    "MaR_": "Making_a_Roll",
    "SaT_": "Skills_and_Tricks",
    "Trick_": "Skills_and_Tricks",
    "Skill_": "Skills_and_Tricks",
    "Turns_": "Turns"
}

# Build list of all known folders
VALID_FOLDERS = {
    "Characters",
    "Conditions",
    "Cybernetic_Augmentations",
    "Gear",
    "Health_and_Healing",
    "Keywords",
    "Making_a_Roll",
    "Skills_and_Tricks",
    "Turns"
}


def get_target_folder(filename):
    """Determine which folder a file should be in based on its prefix."""
    for prefix, folder in FOLDER_RULES.items():
        if filename.startswith(prefix):
            return folder
    return None


def find_markdown_files():
    """Find all markdown files in the vault, excluding specified folders."""
    md_files = []
    
    for root, dirs, files in os.walk(VAULT_PATH):
        root_path = Path(root)
        
        # Skip excluded folders
        relative_path = root_path.relative_to(VAULT_PATH)
        if any(part in EXCLUDED_FOLDERS for part in relative_path.parts):
            continue
        
        dirs[:] = [d for d in dirs if d not in EXCLUDED_FOLDERS]
        
        # Collect markdown files
        for file in files:
            if file.endswith('.md'):
                md_files.append(root_path / file)
    
    return md_files


def extract_links(content):
    """Extract all wikilinks from markdown content."""
    # Match [[link]] or [[link|display text]]
    pattern = r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]'
    return re.finditer(pattern, content)


def normalize_link(link_target):
    """
    Normalize a link by adding folder prefix if missing.
    Returns (normalized_link, was_changed, target_folder)
    """
    # Check if link already has a folder reference
    if '/' in link_target:
        parts = link_target.split('/', 1)
        folder = parts[0]
        # Verify it's a valid folder
        if folder in VALID_FOLDERS:
            return link_target, False, folder
    
    # Extract just the filename (remove .md extension if present)
    filename = link_target.split('/')[-1]
    if filename.endswith('.md'):
        filename = filename[:-3]
    
    # Determine target folder based on prefix
    target_folder = get_target_folder(filename)
    
    if target_folder:
        normalized = f"{target_folder}/{filename}"
        return normalized, True, target_folder
    
    # No matching rule found
    return link_target, False, None


def process_file(file_path, dry_run=False):
    """Process a single markdown file to normalize links."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"ERROR reading {file_path}: {e}")
        return 0
    
    original_content = content
    changes_made = 0
    changes_log = []
    
    # Find and process all links
    links = list(extract_links(content))
    
    # Process in reverse order to maintain string positions
    for match in reversed(links):
        link_target = match.group(1)
        display_text = match.group(2)
        
        normalized, was_changed, target_folder = normalize_link(link_target)
        
        if was_changed:
            # Build the new link
            if display_text:
                new_link = f"[[{normalized}|{display_text}]]"
            else:
                new_link = f"[[{normalized}]]"
            
            # Replace in content
            start, end = match.span()
            content = content[:start] + new_link + content[end:]
            
            changes_made += 1
            changes_log.append(f"  {link_target} → {normalized}")
    
    # Write changes if any were made
    if changes_made > 0 and not dry_run:
        # Create backup
        backup_path = file_path.parent / (file_path.stem + BACKUP_SUFFIX + file_path.suffix)
        shutil.copy2(file_path, backup_path)
        
        # Write normalized content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        rel_path = file_path.relative_to(VAULT_PATH)
        print(f"\n✓ {rel_path} ({changes_made} links normalized)")
        for log in changes_log:
            print(log)
    
    return changes_made


def main():
    """Main execution function."""
    print("=" * 70)
    print("Obsidian Link Normalizer")
    print("=" * 70)
    print(f"Vault: {VAULT_PATH}")
    print(f"Backup suffix: {BACKUP_SUFFIX}")
    print()
    
    # Verify vault exists
    if not VAULT_PATH.exists():
        print(f"ERROR: Vault path does not exist: {VAULT_PATH}")
        return
    
    # Find all markdown files
    print("Scanning for markdown files...")
    md_files = find_markdown_files()
    print(f"Found {len(md_files)} markdown files")
    print()
    
    # Ask for confirmation
    print("This script will:")
    print("1. Create backups of all modified files")
    print("2. Normalize links to include folder references")
    print("3. Log all changes made")
    print()
    
    response = input("Proceed? (yes/no): ").strip().lower()
    if response != 'yes':
        print("Aborted.")
        return
    
    print()
    print("Processing files...")
    print("-" * 70)
    
    # Process all files
    total_changes = 0
    files_modified = 0
    
    for file_path in md_files:
        changes = process_file(file_path, dry_run=False)
        if changes > 0:
            files_modified += 1
            total_changes += changes
    
    print()
    print("=" * 70)
    print(f"Complete!")
    print(f"Files modified: {files_modified}")
    print(f"Total links normalized: {total_changes}")
    print(f"Backups saved with suffix: {BACKUP_SUFFIX}")
    print("=" * 70)


if __name__ == "__main__":
    main()
