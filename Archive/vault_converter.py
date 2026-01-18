import re
import os
import shutil
from pathlib import Path
import yaml

def build_file_index_from_nav(mkdocs_yml_path='mkdocs.yml'):
    """
    Build a file index from the nav structure in mkdocs.yml.
    This gives us the exact paths that MkDocs expects.
    Returns: {filename_without_ext: path_from_nav}
    """
    file_index = {}
    
    if not Path(mkdocs_yml_path).exists():
        print(f"Warning: {mkdocs_yml_path} not found")
        return file_index
    
    with open(mkdocs_yml_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    if 'nav' not in config:
        print("Warning: No nav section in mkdocs.yml")
        return file_index
    
    def extract_paths(nav_item):
        """Recursively extract all file paths from nav structure."""
        if isinstance(nav_item, dict):
            for key, value in nav_item.items():
                if isinstance(value, str):
                    # This is a file path like "Characters/Backgrounds.md"
                    # Extract filename without extension
                    path_without_ext = value.replace('.md', '')
                    filename = Path(value).stem  # Gets just the filename part
                    
                    if filename in file_index:
                        print(f"  [WARNING] Duplicate in nav: {filename}")
                    
                    file_index[filename] = path_without_ext
                elif isinstance(value, list):
                    # Recurse into list
                    for item in value:
                        extract_paths(item)
        elif isinstance(nav_item, list):
            for item in nav_item:
                extract_paths(item)
    
    extract_paths(config['nav'])
    
    return file_index

def calculate_relative_link(from_path, to_path):
    """
    Calculate a relative link from one file to another.
    Both paths are from docs root, without .md extension.
    """
    from_parts = from_path.split('/')
    to_parts = to_path.split('/')
    
    # Get directories (everything except last part which is filename)
    from_dir_parts = from_parts[:-1]
    to_dir_parts = to_parts[:-1]
    to_filename = to_parts[-1]
    
    # If same directory, just return filename
    if from_dir_parts == to_dir_parts:
        return to_filename
    
    # Find common prefix
    common_length = 0
    for i in range(min(len(from_dir_parts), len(to_dir_parts))):
        if from_dir_parts[i] == to_dir_parts[i]:
            common_length += 1
        else:
            break
    
    # Calculate ups and downs
    ups = len(from_dir_parts) - common_length
    downs = to_dir_parts[common_length:]
    
    # Build path
    path_parts = ['foo'] *  [to_filename]
    return '/'.join(path_parts)

def convert_file_content(content, current_file_path, file_index):
    """
    Convert all wikilinks to simple references for mkdocs-autorefs.
    autorefs will find the files automatically by name.
    """
    
    def replace_wikilink(link_content, is_escaped=False):
        """Common logic for replacing wikilinks."""
        if '|' in link_content:
            page_path, alias = link_content.split('|', 1)
            display_text = alias.strip()
        else:
            page_path = link_content
            display_text = page_path.replace('_', ' ').strip()
        
        # Clean up page path - just use the filename
        page_name = page_path.strip().replace(' ', '_')
        
        # For autorefs, we just need the page name without path or extension
        # It will search across all docs and find it
        link = f"[{display_text}]({page_name})"
        return f"\\[{link}\\]" if is_escaped else link
    
    # First pass: escaped bracket wikilinks
    def replace_escaped(match):
        return replace_wikilink(match.group(1), is_escaped=True)
    
    escaped_pattern = r'\\\[\[\[([^\]]+)\]\]\\\]'
    content = re.sub(escaped_pattern, replace_escaped, content)
    
    # Second pass: regular wikilinks
    def replace_regular(match):
        return replace_wikilink(match.group(1), is_escaped=False)
    
    simple_pattern = r'\[\[([^\]]+)\]\]'
    content = re.sub(simple_pattern, replace_regular, content)
    
    return content

def get_excluded_folders(mkdocs_yml_path='mkdocs.yml'):
    """
    Read the mkdocs.yml file and extract the excluded folders.
    """
    excluded = {'Archive', 'assets', '.obsidian', '.git'}
    
    if Path(mkdocs_yml_path).exists():
        try:
            with open(mkdocs_yml_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                if 'exclude_docs' in config:
                    exclude_str = config['exclude_docs']
                    for item in exclude_str.split('\n'):
                        item = item.strip().rstrip('/')
                        if item:
                            excluded.add(item)
        except Exception as e:
            print(f"Warning: Could not parse mkdocs.yml: {e}")
    
    return excluded

def scan_vault(vault_root='.', excluded_folders=None):
    """
    Scan the vault and return a dictionary of folders and their markdown files.
    """
    if excluded_folders is None:
        excluded_folders = get_excluded_folders()
    
    vault_path = Path(vault_root)
    structure = {}
    
    for root, dirs, files in os.walk(vault_path):
        dirs[:] = [d for d in dirs if d not in excluded_folders and not d.startswith('.')]
        
        rel_path = Path(root).relative_to(vault_path)
        
        if rel_path == Path('.'):
            continue
        
        md_files = [f for f in files if f.endswith('.md')]
        
        if md_files:
            folder_name = str(rel_path)
            structure[folder_name] = sorted(md_files)
    
    return structure

def convert_vault_to_docs(vault_structure, file_index, source_root='.', dest_root='docs'):
    """
    Convert all files from vault structure to docs folder.
    Uses file_index from mkdocs.yml nav for link resolution.
    """
    source_path = Path(source_root)
    dest_path = Path(dest_root)
    
    # Clear existing docs folder
    if dest_path.exists():
        for item in dest_path.iterdir():
            if item.name != '.gitkeep':
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
    
    dest_path.mkdir(parents=True, exist_ok=True)
    
    converted_count = 0
    
    for folder, files in vault_structure.items():
        dest_folder = dest_path / folder
        dest_folder.mkdir(parents=True, exist_ok=True)
        
        print(f"\nProcessing folder: {folder}")
        
        for filename in files:
            source_file = source_path / folder / filename
            dest_file = dest_folder / filename
            
            if not source_file.exists():
                print(f"  [SKIP] Not found: {filename}")
                continue
            
            try:
                with open(source_file, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                print(f"  [ERROR] Reading {filename}: {e}")
                continue
            
            # Get the current file's path as it appears in nav (without .md)
            filename_stem = filename.replace('.md', '')
            
            # Look up this file in the index to get its full path
            if filename_stem in file_index:
                current_file_path = file_index[filename_stem]
            else:
                # Fallback: construct from folder + filename
                current_file_path = f"{folder}/{filename_stem}".replace('\\', '/')
                print(f"  [WARNING] {filename} not found in nav, using fallback path")
            
            # Convert wikilinks
            converted_content = convert_file_content(content, current_file_path, file_index)
            
            try:
                with open(dest_file, 'w', encoding='utf-8') as f:
                    f.write(converted_content)
                print(f"  [OK] {filename}")
                converted_count += 1
            except Exception as e:
                print(f"  [ERROR] Writing {filename}: {e}")
    
    return converted_count

def generate_nav_structure(vault_structure):
    """
    Generate the nav section for mkdocs.yml based on vault structure.
    """
    nav = []
    
    for folder, files in sorted(vault_structure.items()):
        folder_name = folder.replace('_', ' ').replace('\\', ' / ')
        folder_items = []
        
        for filename in files:
            display_name = filename.replace('.md', '').replace('_', ' ')
            file_path = f"{folder}/{filename}".replace('\\', '/')
            folder_items.append({display_name: file_path})
        
        nav.append({folder_name: folder_items})
    
    return nav

def update_mkdocs_yml(vault_structure, mkdocs_yml_path='mkdocs.yml'):
    """
    Update the mkdocs.yml file with the new navigation structure.
    """
    with open(mkdocs_yml_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    new_nav = generate_nav_structure(vault_structure)
    config['nav'] = new_nav
    
    with open(mkdocs_yml_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    
    print(f"\n[OK] Updated mkdocs.yml with {len(new_nav)} sections")

def copy_custom_css(source='stylesheets/custom.css', dest='docs/stylesheets/custom.css'):
    """
    Copy the custom CSS file if it exists.
    """
    source_path = Path(source)
    dest_path = Path(dest)
    
    if source_path.exists():
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, dest_path)
        print(f"[OK] Copied custom.css")
    else:
        print(f"[SKIP] custom.css not found at {source}")

def main():
    """
    Main conversion process.
    """
    print("="*60)
    print("GHOSTBURN 2325 - Obsidian to MkDocs Converter")
    print("="*60)
    
    # Get excluded folders
    print("\nReading configuration...")
    excluded = get_excluded_folders()
    print(f"Excluding folders: {', '.join(sorted(excluded))}")
    
    # Scan vault
    print("\nScanning vault structure...")
    vault_structure = scan_vault('.', excluded)
    
    total_files = sum(len(files) for files in vault_structure.values())
    print(f"Found {len(vault_structure)} folders with {total_files} markdown files")
    
    # Update mkdocs.yml first
    print("\nUpdating navigation...")
    update_mkdocs_yml(vault_structure)
    
    # Build file index from the nav we just created
    print("\nBuilding file index from mkdocs.yml nav...")
    file_index = build_file_index_from_nav()
    print(f"Indexed {len(file_index)} files from nav")
    
    # Convert files using the file index
    print("\nConverting files...")
    converted = convert_vault_to_docs(vault_structure, file_index)
    
    # Copy CSS
    print("\nCopying assets...")
    copy_custom_css()
    
    # Summary
    print("\n" + "="*60)
    print("CONVERSION COMPLETE!")
    print("="*60)
    print(f"Converted {converted} files across {len(vault_structure)} folders")
    print("\nNext steps:")
    print("1. Run: mkdocs serve")
    print("2. Open: http://127.0.0.1:8000")
    print("\nOr build the site: mkdocs build")

if __name__ == "__main__":
    main()
