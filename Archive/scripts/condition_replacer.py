import os
import re

# Configuration
search_dir = r"C:\GHOSTBURN_2325\Conditions"

# Collect all keywords and conditions
keywords = [
    "Absolute Damage", "Admin", "Advanced Supplies", "Attack", "Auditory", "Basic",
    "Close", "Concentrate", "Contact", "Control Deck", "Counterattack", "Crashes",
    "Cyber Rig", "Datajack", "Damage Array", "Disabled", "Downgraded", "Drone",
    "Enabled", "Far", "Fine Control", "Fly", "Fort", "Gift", "Group", "Gun",
    "Handling", "High Speed", "Language", "Location", "Low Speed", "Lucky",
    "Manipulator Arm", "Maximum Damage", "Melee", "Minimum Damage", "Moderate Speed",
    "Move", "Nearby", "Normal Damage", "One Hand", "Operator", "Opposed",
    "Optimal Range", "Physical", "Range", "Reaction", "Scope", "Secret",
    "Security", "Security Alert", "Silencer", "Small Item", "Social", "Stability",
    "Stabilization DL", "Supplies", "Surgical Procedure", "Temporary", "Threat",
    "Tools", "Two Hands", "Unarmed Strike", "Upgraded", "Vehicle", "Vicinity",
    "Visible", "Visual", "Vocal", "Wireless", "Wits"
]

conditions = [
    "Agony", "Ally", "Bewildered", "Bleeding", "Blinded", "Break",
    "Cognitive Impairment", "Compliant", "Concealment Partial", "Concealment Total",
    "Confident", "Confused", "Critical Condition", "Deafened", "Deaths Door",
    "Disfigured Major", "Disfigured Minor", "Distracted", "Drowning", "Dying",
    "Emotional", "Entertained", "Fine Motor Impairment", "Healthy",
    "Hearing Impairment", "Hidden", "Immobilized", "Incapable", "Inspired",
    "Jammed", "Life Threatening", "Mouth Breather", "Movement Impaired",
    "Movement Restricted", "Mute", "Off Balance", "Off Guard", "Prone", "Raining",
    "Recovering", "Restrained", "Servile", "Severely Wounded", "Shaken",
    "Speech Impairment", "Stabilized", "Stress", "Stunned", "Suffocating",
    "Suppressed", "Suspicous", "Traumatized", "Unaware", "Unconscious",
    "Undetected", "Unresponsive", "Vision Impairment", "Wounded"
]

# Create lookup for all terms
all_terms = {}
for k in keywords:
    all_terms[k] = ('Keyword', k.replace(' ', '_'))
for c in conditions:
    all_terms[c] = ('Condition', c.replace(' ', '_'))

# Track changes
files_modified = 0
total_additions = 0

# Walk through all files
for root, dirs, files in os.walk(search_dir):
    for filename in files:
        if not filename.endswith('.md'):
            continue
        
        filepath = os.path.join(root, filename)
        
        # Determine which condition this file represents (for self-reference exclusion)
        # Filename format: Condition_Name.md
        current_condition = None
        if filename.startswith('Condition_'):
            condition_name = filename[10:-3].replace('_', ' ')  # Remove "Condition_" and ".md"
            current_condition = condition_name
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            continue
        
        original_content = content
        seen_terms = set()
        file_additions = 0
        
        # Process line by line to track first occurrences
        lines = content.split('\n')
        new_lines = []
        
        for line in lines:
            modified_line = line
            
            for term, (term_type, term_filename) in all_terms.items():
                # Skip if this is a self-reference (e.g., Confident.md referencing [Confident])
                if term_type == 'Condition' and term == current_condition:
                    continue
                
                # Skip if already seen
                if term in seen_terms:
                    continue
                
                # Look for unlinked term: \[Term\]
                unlinked_pattern = r'\\' + r'\[' + re.escape(term) + r'\\' + r'\]'
                
                if re.search(unlinked_pattern, modified_line):
                    # Found first occurrence - link it
                    seen_terms.add(term)
                    
                    # Replace with link: \[[[Type_Name|Term]]\]
                    linked = f'\\[[[{term_type}_{term_filename}|{term}]]\\]'
                    modified_line = re.sub(unlinked_pattern, linked, modified_line, count=1)
                    file_additions += 1
            
            new_lines.append(modified_line)
        
        new_content = '\n'.join(new_lines)
        
        # Write back if changes were made
        if new_content != original_content:
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                files_modified += 1
                total_additions += file_additions
                print(f"✓ {filename}: {file_additions} link(s) added")
            except Exception as e:
                print(f"Error writing {filename}: {e}")

# Summary
print(f"\n{'='*60}")
print(f"Modified {files_modified} file(s)")
print(f"Total links added: {total_additions}")
print(f"{'='*60}")
