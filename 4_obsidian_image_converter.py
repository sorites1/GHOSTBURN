import os
import re

def convert_image_links(text, is_root_file):
    """Convert Obsidian image links to MkDocs format."""
    
    def replace_image_link(match):
        content = match.group(1)
        
        # Handle alt text if provided
        if '|' in content:
            path, alt_text = content.split('|', 1)
        else:
            path = content
            # Use filename without extension as alt text
            alt_text = path.split('/')[-1].rsplit('.', 1)[0]
        
        # Determine the correct path based on file location
        if is_root_file:
            # Root level files can reference assets directly
            mkdocs_path = path
        else:
            # Subfolder files need to go up one level
            # If path already starts with assets/, use ../assets/
            # Otherwise keep the path as-is with ../
            if path.startswith('assets/'):
                mkdocs_path = f"../{path}"
            else:
                mkdocs_path = f"../{path}"
        
        return f"![{alt_text}]({mkdocs_path})"
    
    # Match ![[...]] for images
    text = re.sub(r'!\[\[([^\]]+)\]\]', replace_image_link, text)
    
    return text

def process_markdown_file(file_path, is_root_file):
    """Process a single markdown file to convert image links."""
    try:
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Convert image links
        converted_content = convert_image_links(content, is_root_file)
        
        # Only write if there were changes
        if converted_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(converted_content)
            return True
        return False
    except Exception as e:
        print(f"  Error processing file: {e}")
        return False

def process_root_files(docs_path):
    """Process .md files in the root of docs/ folder."""
    print("Processing root-level markdown files...")
    
    # Get all .md files in root
    md_files = [f for f in os.listdir(docs_path) 
                if f.endswith('.md') and os.path.isfile(os.path.join(docs_path, f))]
    
    if not md_files:
        print("  No .md files found in root")
        return
    
    print(f"  Found {len(md_files)} markdown file(s) in root")
    
    for filename in md_files:
        file_path = os.path.join(docs_path, filename)
        if process_markdown_file(file_path, is_root_file=True):
            print(f"    Converted images in: {filename}")

def process_folder(folder_path, folder_name):
    """Process all .md files in a subfolder to convert image links."""
    if not os.path.exists(folder_path):
        print(f"  Folder not found: {folder_name}")
        return
    
    # Get all .md files in the folder
    md_files = [f for f in os.listdir(folder_path) if f.endswith('.md')]
    
    if not md_files:
        print(f"  No .md files found in {folder_name}")
        return
    
    print(f"  Found {len(md_files)} markdown file(s) in {folder_name}")
    
    converted_count = 0
    for filename in md_files:
        file_path = os.path.join(folder_path, filename)
        if process_markdown_file(file_path, is_root_file=False):
            converted_count += 1
            print(f"    Converted images in: {filename}")
    
    if converted_count == 0:
        print(f"    No image links found to convert")

def main():
    """Main function to orchestrate the image conversion process."""
    vault_path = r'C:\GHOSTBURN_2325'
    docs_path = os.path.join(vault_path, 'docs')
    
    print("Starting Obsidian to MkDocs image link conversion...")
    print(f"Vault path: {vault_path}\n")
    
    # Check if docs folder exists
    if not os.path.exists(docs_path):
        print(f"Error: docs folder not found at {docs_path}")
        print("Please ensure the docs folder exists before running this script.")
        return
    
    print(f"Found docs folder: {docs_path}\n")
    
    # Process root-level files first
    process_root_files(docs_path)
    
    print()
    
    # List of folders to process
    folders_to_process = [
        'Characters',
        'Conditions',
        'Cybernetic_Augmentations',
        'Game_Master',
        'Gear',
        'Gear_Mods',
        'Gear_and_Augments',
        'Firearms',
        'Health_and_Healing',
        'Making_a_Roll',
        'Mods',
        'Mods_Augment',
        'Mods_Weapon',
        'Keywords',
        'Lexicon',
        'Melee_Weapons',
        'Playing_the_Game',
        'Skills_and_Tricks'
    ]
    
    # Process each folder
    print("Processing subfolders...")
    for folder_name in folders_to_process:
        print(f"\n{folder_name}:")
        folder_path = os.path.join(docs_path, folder_name)
        process_folder(folder_path, folder_name)
    
    print("\nImage conversion complete!")

if __name__ == "__main__":
    main()
