import os
import re

# Configuration
search_dir = r"C:\GHOSTBURN_2325\Skills and Tricks"

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
total_removals = 0

def process_section(lines, in_table):
    """Process a section and apply first-occurrence logic"""
    seen_in_section = set()
    processed_lines = []
    
    for line in lines:
        modified_line = line
        
        for term, (term_type, term_filename) in all_terms.items():
            # The actual format is: \[[[Type_Name|Name]]\] or \[[[Type_Name\|Name]]\]
            # Breaking it down: \[ = escaped bracket, [[ = wikilink start, Type_Name|Name, ]] = wikilink end, \] = escaped bracket
            # Match both: unescaped pipe (|) for body text, escaped pipe (\|) for tables
            pattern = r'\\' + r'\[' + r'\[\[' + re.escape(f'{term_type}_{term_filename}') + r'\\?' + r'\|' + re.escape(term) + r'\]\]' + r'\\' + r'\]'
            
            matches = list(re.finditer(pattern, modified_line))
            
            if matches:
                if term in seen_in_section:
                    # Already seen - remove ALL links
                    # Replace with: \[Term\]
                    unlinked = f'\\[{term}\\]'
                    modified_line = re.sub(pattern, unlinked, modified_line)
                else:
                    # First occurrence - keep it
                    seen_in_section.add(term)
                    
                    # If multiple on same line, keep first, remove rest
                    if len(matches) > 1:
                        parts = []
                        last_pos = 0
                        
                        for idx, match in enumerate(matches):
                            parts.append(modified_line[last_pos:match.start()])
                            
                            if idx == 0:
                                # Keep first
                                parts.append(match.group(0))
                            else:
                                # Replace with unlinked
                                parts.append(f'\\[{term}\\]')
                            
                            last_pos = match.end()
                        
                        parts.append(modified_line[last_pos:])
                        modified_line = ''.join(parts)
        
        processed_lines.append(modified_line)
    
    return processed_lines

# Walk through all files
for root, dirs, files in os.walk(search_dir):
    for filename in files:
               
        if not filename.endswith('.md'):
            continue
        
        filepath = os.path.join(root, filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            continue
        
        original_content = ''.join(lines)
        new_lines = []
        current_section = []
        in_table = False
        
        for line in lines:
            stripped = line.lstrip()
            is_table_line = stripped.startswith('|')
            
            # Detect section boundaries
            if is_table_line and not in_table:
                # Starting a table
                if current_section:
                    new_lines.extend(process_section(current_section, False))
                    current_section = []
                in_table = True
                current_section.append(line)
            elif not is_table_line and in_table:
                # Ending a table
                if current_section:
                    new_lines.extend(process_section(current_section, True))
                    current_section = []
                in_table = False
                current_section.append(line)
            else:
                # Continue current section
                current_section.append(line)
        
        # Process final section
        if current_section:
            new_lines.extend(process_section(current_section, in_table))
        
        new_content = ''.join(new_lines)
        
        # Check if changed
        if new_content != original_content:
            # Count removals
            old_count = original_content.count('[[[')
            new_count = new_content.count('[[[')
            removals = old_count - new_count
            
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                files_modified += 1
                total_removals += removals
                print(f"✓ {filename}: {removals} redundant link(s) removed")
            except Exception as e:
                print(f"Error writing {filename}: {e}")

# Summary
print(f"\n{'='*60}")
print(f"Modified {files_modified} file(s)")
print(f"Total redundant links removed: {total_removals}")
print(f"{'='*60}")
