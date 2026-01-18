import os
import shutil
from pathlib import Path

# Configuration
VAULT_PATH = Path(r"C:\GHOSTBURN_2325")
DOCS_FOLDER = VAULT_PATH / "docs"

EXCLUDED_FOLDERS = {".git", ".obsidian", "Archive", "assets", "docs"}
EXCLUDED_FILES = {".gitignore"}
EXCLUDED_EXTENSIONS = {".py"}


def should_exclude_folder(folder_name):
    """Check if folder should be excluded from copy."""
    return folder_name in EXCLUDED_FOLDERS


def should_exclude_file(file_path):
    """Check if file should be excluded from copy."""
    file_name = file_path.name
    file_ext = file_path.suffix
    
    if file_name in EXCLUDED_FILES:
        return True
    if file_ext in EXCLUDED_EXTENSIONS:
        return True
    
    return False


def clear_docs_folder():
    """Clear all contents of the docs folder."""
    if DOCS_FOLDER.exists():
        print(f"Clearing contents of {DOCS_FOLDER}...")
        shutil.rmtree(DOCS_FOLDER)
    
    DOCS_FOLDER.mkdir(exist_ok=True)
    print(f"Created fresh docs folder at {DOCS_FOLDER}")


def copy_vault_files():
    """Copy all non-excluded files from vault to docs folder."""
    files_copied = 0
    
    for root, dirs, files in os.walk(VAULT_PATH):
        root_path = Path(root)
        
        # Skip if current directory is docs or any excluded folder
        relative_path = root_path.relative_to(VAULT_PATH)
        if any(part in EXCLUDED_FOLDERS for part in relative_path.parts):
            continue
        
        # Filter out excluded subdirectories to prevent os.walk from descending into them
        dirs[:] = [d for d in dirs if not should_exclude_folder(d)]
        
        # Process files in current directory
        for file in files:
            file_path = root_path / file
            
            if should_exclude_file(file_path):
                continue
            
            # Calculate destination path
            rel_to_vault = file_path.relative_to(VAULT_PATH)
            dest_path = DOCS_FOLDER / rel_to_vault
            
            # Create destination directory if needed
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy file
            shutil.copy2(file_path, dest_path)
            files_copied += 1
            print(f"Copied: {rel_to_vault}")
    
    return files_copied


def main():
    """Main execution function."""
    print("=" * 60)
    print("Obsidian Vault Copy Script")
    print("=" * 60)
    
    # Verify vault path exists
    if not VAULT_PATH.exists():
        print(f"ERROR: Vault path does not exist: {VAULT_PATH}")
        return
    
    # Clear and recreate docs folder
    clear_docs_folder()
    print()
    
    # Copy files
    print("Copying files...")
    print()
    files_copied = copy_vault_files()
    
    print()
    print("=" * 60)
    print(f"Complete! Copied {files_copied} files to {DOCS_FOLDER}")
    print("=" * 60)


if __name__ == "__main__":
    main()
