from pathlib import Path

# Configuration
VAULT_PATH = Path(r"C:\GHOSTBURN_2325")
CHARACTERS_FOLDER = VAULT_PATH / "Skills_and_Tricks"

# Get all .md files in Characters folder
md_files = list(CHARACTERS_FOLDER.glob("*.md"))

print(f"Found {len(md_files)} markdown files in Characters folder")
print("=" * 60)

total_changes = 0

for md_file in md_files:
    print(f"\nProcessing: {md_file.name}")
    
    # Read file
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    file_changes = 0

    # First pass: escaped bracket links \[[[
    print("  Pass 1: Escaped bracket links")
    replacements_escaped = [
        (r'\[[[Keyword_', r'\[[[Keywords/Keyword_'),
        (r'\[[[Char_', r'\[[[Characters/Char_'),
        (r'\[[[Condition_', r'\[[[Conditions/Condition_'),
        (r'\[[[Aug_', r'\[[[Cybernetic_Augmentations/Aug_'),
        (r'\[[[Gear_', r'\[[[Gear/Gear_'),
        (r'\[[[HaR_', r'\[[[Health_and_Healing/HaR_'),
        (r'\[[[MaR_', r'\[[[Making_a_Roll/MaR_'),
        (r'\[[[SaT_', r'\[[[Skills_and_Tricks/SaT_'),
        (r'\[[[Trick_', r'\[[[Skills_and_Tricks/Trick_'),
    ]

    for old, new in replacements_escaped:
        count = content.count(old)
        if count > 0:
            print(f"    Found {count} instances of {old}")
            content = content.replace(old, new)
            file_changes += count

    # Second pass: regular links [[
    print("  Pass 2: Regular bracket links")
    replacements_regular = [
        ('[[Keyword_', '[[Keywords/Keyword_'),
        ('[[Char_', '[[Characters/Char_'),
        ('[[Condition_', '[[Conditions/Condition_'),
        ('[[Aug_', '[[Cybernetic_Augmentations/Aug_'),
        ('[[Gear_', '[[Gear/Gear_'),
        ('[[HaR_', '[[Health_and_Healing/HaR_'),
        ('[[MaR_', '[[Making_a_Roll/MaR_'),
        ('[[SaT_', '[[Skills_and_Tricks/SaT_'),
        ('[[Trick_', '[[Skills_and_Tricks/Trick_'),
    ]

    for old, new in replacements_regular:
        count = content.count(old)
        if count > 0:
            print(f"    Found {count} instances of {old}")
            content = content.replace(old, new)
            file_changes += count

    # Write file if changes were made
    if file_changes > 0:
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  SAVED: {file_changes} changes")
        total_changes += file_changes
    else:
        print(f"  No changes needed")

print("\n" + "=" * 60)
print(f"Total changes across all files: {total_changes}")
