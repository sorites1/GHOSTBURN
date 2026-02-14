import os
import re
from pathlib import Path

def convert_obsidian_callouts(text):
    """Convert Obsidian callouts to MkDocs admonitions format."""
    
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
    pattern = r'^> \[!([A-Z]+)\](?: (.+?))?\n((?:^>.*\n?)+)'
    text = re.sub(pattern, replace_callout, text, flags=re.MULTILINE)
    
    return text

def find_target_file(docs_path, link_target):
    """
    Find the actual file path for a given link target.
    Searches through docs directory to find matching .md file.
    
    Args:
        docs_path: Path to docs directory
        link_target: The target from the link (e.g., "Firearms/Light_Pistols/EZTech_Punisher_Lite")
    
    Returns:
        Path object if found, None otherwise
    """
    # Remove .md extension if present
    if link_target.endswith('.md'):
        link_target = link_target[:-3]
    
    # Try exact path match first
    exact_path = docs_path / f"{link_target}.md"
    if exact_path.exists():
        return exact_path
    
    # Try with /index at the end (for folder links)
    index_path = docs_path / link_target / "index.md"
    if index_path.exists():
        return index_path
    
    # Search for the file by name anywhere in docs
    # This handles cases where just a filename is provided
    filename = link_target.split('/')[-1]
    for root, dirs, files in os.walk(docs_path):
        if f"{filename}.md" in files:
            return Path(root) / f"{filename}.md"
    
    return None

def calculate_relative_path(source_file, target_file, docs_path):
    """
    Calculate the relative path from source file to target file.
    
    Args:
        source_file: Path to the file containing the link
        target_file: Path to the file being linked to
        docs_path: Path to docs directory (for reference)
    
    Returns:
        Relative path string suitable for markdown link
    """
    # Get paths relative to docs folder
    source_rel = source_file.relative_to(docs_path)
    target_rel = target_file.relative_to(docs_path)
    
    # Get the directory containing the source file
    source_dir = source_rel.parent
    
    # Calculate relative path from source directory to target
    # We need to go up from source_dir, then down to target
    
    # Count how many levels up we need to go
    levels_up = len(source_dir.parts)
    
    # Build the relative path
    if levels_up == 0:
        # Same directory
        rel_path = target_rel.name
    else:
        # Go up appropriate number of levels, then down to target
        up_parts = ['..'] * levels_up
        rel_path = '/'.join(up_parts + list(target_rel.parts))
    
    return rel_path

def convert_obsidian_links(text, source_file_path, docs_path):
    """
    Convert Obsidian links to MkDocs format with proper relative paths.
    
    Args:
        text: The markdown text to process
        source_file_path: Path to the file being processed
        docs_path: Path to docs directory
    """
    
    # Pattern 1: Handle escaped brackets with Obsidian links
    # Matches: \[[[path|display]]\] or \[[[path]]\]
    def replace_escaped_link(match):
        inner_link = match.group(1)
        
        # Parse the inner Obsidian link
        if '|' in inner_link:
            path, display = inner_link.split('|', 1)
        else:
            path = inner_link
            display = path.split('/')[-1]  # Use filename as display
        
        # Find the actual target file
        target_file = find_target_file(docs_path, path)
        
        if target_file:
            # Calculate relative path from source to target
            rel_path = calculate_relative_path(source_file_path, target_file, docs_path)
            mkdocs_link = f"[{display}]({rel_path})"
            return f"[{mkdocs_link}]"
        else:
            print(f"    WARNING: Could not find target for link: {path}")
            # Return original if we can't find the target
            return match.group(0)
    
    text = re.sub(r'\\\[\[\[([^\]]+)\]\]\\\]', replace_escaped_link, text)
    
    # Pattern 2: Handle regular Obsidian links
    # Matches: [[path|display]] or [[path]]
    def replace_regular_link(match):
        content = match.group(1)
        
        # Skip if this looks like it's already been converted
        if '](' in content:
            return match.group(0)
        
        if '|' in content:
            path, display = content.split('|', 1)
        else:
            path = content
            display = path.split('/')[-1]  # Use filename as display
        
        # Find the actual target file
        target_file = find_target_file(docs_path, path)
        
        if target_file:
            # Calculate relative path from source to target
            rel_path = calculate_relative_path(source_file_path, target_file, docs_path)
            return f"[{display}]({rel_path})"
        else:
            print(f"    WARNING: Could not find target for link: {path}")
            # Return original if we can't find the target
            return match.group(0)
    
    text = re.sub(r'\[\[([^\]]+)\]\](?!\()', replace_regular_link, text)
    
    return text

def process_markdown_file(file_path, docs_path):
    """Process a single markdown file to convert Obsidian links."""
    try:
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Convert callouts first, then links
        converted_content = convert_obsidian_callouts(content)
        converted_content = convert_obsidian_links(converted_content, file_path, docs_path)
        
        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(converted_content)
        
        return True
    except Exception as e:
        print(f"  Error processing file: {e}")
        return False

def process_all_markdown_files(docs_path):
    """Recursively process all markdown files in docs folder."""
    processed_count = 0
    
    for root, dirs, files in os.walk(docs_path):
        # Get all .md files in current directory
        md_files = [f for f in files if f.endswith('.md')]
        
        if md_files:
            root_path = Path(root)
            relative_path = root_path.relative_to(docs_path)
            print(f"\n{relative_path if str(relative_path) != '.' else 'Root'}:")
            print(f"  Found {len(md_files)} markdown file(s)")
            
            for filename in md_files:
                file_path = root_path / filename
                if process_markdown_file(file_path, docs_path):
                    print(f"    Processed: {filename}")
                    processed_count += 1
    
    return processed_count

def main():
    """Main function to orchestrate the conversion process."""
    vault_path = Path(r'C:\GHOSTBURN_2325')
    docs_path = vault_path / 'docs'
    
    print("=" * 60)
    print("Obsidian to MkDocs Link Conversion")
    print("=" * 60)
    print(f"Vault path: {vault_path}")
    print(f"Docs path: {docs_path}\n")
    
    # Check if docs folder exists
    if not docs_path.exists():
        print(f"Error: docs folder not found at {docs_path}")
        print("Please ensure the docs folder exists before running this script.")
        return
    
    print(f"Found docs folder: {docs_path}\n")
    print("Processing all markdown files...")
    
    # Process all markdown files recursively
    processed_count = process_all_markdown_files(docs_path)
    
    print("\n" + "=" * 60)
    print(f"Conversion complete! Processed {processed_count} files.")
    print("=" * 60)

if __name__ == "__main__":
    main()