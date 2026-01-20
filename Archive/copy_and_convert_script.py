import shutil
import re
from pathlib import Path

# Configuration
VAULT_PATH = Path(r"C:\GHOSTBURN_2325")
DOCS_FOLDER = VAULT_PATH / "docs"

FOLDERS_TO_COPY = [
    "Characters",
    "Conditions",
    "Cybernetic_Augmentations",
    "Gear",
    "Health_and_Healing",
    "Keywords",
    "Making_a_Roll",
    "Skills_and_Tricks",
    "Turns"
]

print("=" * 60)
print("Step 1 & 2: Clear and copy to docs/")
print("=" * 60)

# Clear docs folder if it exists
if DOCS_FOLDER.exists():
    print(f"Removing existing docs/ folder...")
    shutil.rmtree(DOCS_FOLDER)

# Create fresh docs folder
DOCS_FOLDER.mkdir()
print(f"Created fresh docs/ folder")

# Copy mkdocs.yml
mkdocs_yml = VAULT_PATH / "mkdocs.yml"
if mkdocs_yml.exists():
    shutil.copy2(mkdocs_yml, DOCS_FOLDER / "mkdocs.yml")
    print(f"Copied mkdocs.yml")

# Copy folders
for folder_name in FOLDERS_TO_COPY:
    source = VAULT_PATH / folder_name
    dest = DOCS_FOLDER / folder_name
    
    if source.exists():
        shutil.copytree(source, dest)
        print(f"Copied {folder_name}/")

print("\n" + "=" * 60)
print("Step 3: Convert links in docs/Characters/Char_NPCs.md")
print("=" * 60)

# Target file
target_file = DOCS_FOLDER / "Characters" / "Char_NPCs.md"

if not target_file.exists():
    print(f"ERROR: File not found: {target_file}")
else:
    # Read file
    with open(target_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    changes = 0
    
    # Convert escaped wikilinks: \[[[path|text]]\] -> [text](path.md)
    # Convert escaped wikilinks without text: \[[[path]]\] -> [path](path.md)
    def convert_escaped_link(match):
        nonlocal changes
        link_path = match.group(1)
        display_text = match.group(2)
        
        if display_text:
            # Has display text: \[[[path|text]]\]
            result = f"[{display_text}]({link_path}.md)"
        else:
            # No display text: \[[[path]]\]
            # Use the filename without folder as display text
            filename = link_path.split('/')[-1]
            result = f"[{filename}]({link_path}.md)"
        
        changes += 1
        print(f"  {match.group(0)} -> {result}")
        return result
    
    # Pattern for escaped links
    escaped_pattern = r'\\?\[\[\[([^\]|]+)(?:\|([^\]]+))?\]\]\\?'
    content = re.sub(escaped_pattern, convert_escaped_link, content)
    
    # Convert regular wikilinks: [[path|text]] -> [text](path.md)
    # Convert regular wikilinks without text: [[path]] -> [path](path.md)
    def convert_regular_link(match):
        nonlocal changes
        link_path = match.group(1)
        display_text = match.group(2)
        
        if display_text:
            # Has display text: [[path|text]]
            result = f"[{display_text}]({link_path}.md)"
        else:
            # No display text: [[path]]
            # Use the filename without folder as display text
            filename = link_path.split('/')[-1]
            result = f"[{filename}]({link_path}.md)"
        
        changes += 1
        print(f"  {match.group(0)} -> {result}")
        return result
    
    # Pattern for regular wikilinks
    regular_pattern = r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]'
    content = re.sub(regular_pattern, convert_regular_link, content)
    
    # Write converted content
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\nTotal conversions: {changes}")

print("\n" + "=" * 60)
print("Done!")
print("=" * 60)
