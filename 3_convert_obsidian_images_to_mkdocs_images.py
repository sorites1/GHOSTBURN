import os
import re
from pathlib import Path

def calculate_relative_path_to_assets(source_file, docs_path):
    """
    Calculate the relative path from a source file to the assets folder.
    
    Args:
        source_file: Path to the file containing the image link
        docs_path: Path to docs directory
    
    Returns:
        Relative path string to assets folder (e.g., "../assets/" or "../../assets/")
    """
    # Get path relative to docs folder
    source_rel = source_file.relative_to(docs_path)
    
    # Get the directory containing the source file
    source_dir = source_rel.parent
    
    # Count how many levels up we need to go
    levels_up = len(source_dir.parts)
    
    # Build the relative path to assets
    if levels_up == 0:
        # File is in root of docs/
        return "assets/"
    else:
        # File is in a subfolder
        up_parts = ['..'] * levels_up
        return '/'.join(up_parts) + '/assets/'

def convert_image_links(text, source_file_path, docs_path):
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
        
        # Remove 'assets/' prefix if present (we'll add it back with correct relative path)
        if path.startswith('assets/'):
            path = path[7:]  # Remove 'assets/' prefix
        
        # Calculate relative path from source file to assets folder
        assets_path = calculate_relative_path_to_assets(source_file_path, docs_path)
        
        # Combine assets path with image filename
        mkdocs_path = f"{assets_path}{path}"
        
        return f"![{alt_text}]({mkdocs_path})"
    
    # Match ![[...]] for images
    text = re.sub(r'!\[\[([^\]]+)\]\]', replace_image_link, text)
    
    return text

def process_markdown_file(file_path, docs_path):
    """Process a single markdown file to convert image links."""
    try:
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Convert image links
        converted_content = convert_image_links(content, file_path, docs_path)
        
        # Only write if there were changes
        if converted_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(converted_content)
            return True
        return False
    except Exception as e:
        print(f"  Error processing file: {e}")
        return False

def process_all_markdown_files(docs_path):
    """Recursively process all markdown files in docs folder."""
    processed_count = 0
    converted_count = 0
    
    for root, dirs, files in os.walk(docs_path):
        # Get all .md files in current directory
        md_files = [f for f in files if f.endswith('.md')]
        
        if md_files:
            root_path = Path(root)
            relative_path = root_path.relative_to(docs_path)
            print(f"\n{relative_path if str(relative_path) != '.' else 'Root'}:")
            print(f"  Found {len(md_files)} markdown file(s)")
            
            folder_converted = 0
            for filename in md_files:
                file_path = root_path / filename
                processed_count += 1
                if process_markdown_file(file_path, docs_path):
                    print(f"    Converted images in: {filename}")
                    converted_count += 1
                    folder_converted += 1
            
            if folder_converted == 0:
                print(f"    No image links found to convert")
    
    return processed_count, converted_count

def main():
    """Main function to orchestrate the image conversion process."""
    vault_path = Path(r'C:\GHOSTBURN_2325')
    docs_path = vault_path / 'docs'
    
    print("=" * 60)
    print("Obsidian to MkDocs Image Link Conversion")
    print("=" * 60)
    print(f"Vault path: {vault_path}")
    print(f"Docs path: {docs_path}\n")
    
    # Check if docs folder exists
    if not docs_path.exists():
        print(f"Error: docs folder not found at {docs_path}")
        print("Please ensure the docs folder exists before running this script.")
        return
    
    print(f"Found docs folder: {docs_path}\n")
    print("Processing all markdown files for image links...")
    
    # Process all markdown files recursively
    processed_count, converted_count = process_all_markdown_files(docs_path)
    
    print("\n" + "=" * 60)
    print(f"Image conversion complete!")
    print(f"Processed {processed_count} files, converted images in {converted_count} files.")
    print("=" * 60)

if __name__ == "__main__":
    main()