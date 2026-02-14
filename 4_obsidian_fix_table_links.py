import os
import re

def fix_backslashes_in_md_files(directory="docs/"):
    """
    Search for .md files in the specified directory and its subdirectories,
    and remove the backslash before ')]' in all .md files.
    
    Args:
        directory (str): The root directory to search for .md files
    """
    # Counters for reporting
    files_processed = 0
    replacements_made = 0
    
    # Walk through all files in the directory and its subdirectories
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if file has .md extension
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                
                try:
                    # Read the file content
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Count occurrences before replacement
                    occurrences_before = len(re.findall(r'\\\)\]', content))
                    
                    if occurrences_before > 0:
                        # Replace all occurrences of '\)]' with ')]'
                        new_content = content.replace('\\)]', ')]')
                        
                        # Write the modified content back to the file
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        
                        replacements_made += occurrences_before
                        print(f"Fixed {occurrences_before} occurrences in: {filepath}")
                    else:
                        print(f"  No changes needed for: {filepath}")
                    
                    files_processed += 1
                    
                except Exception as e:
                    print(f"✗ Error processing {filepath}: {e}")
    
    # Summary
    print("\n" + "="*50)
    print("SUMMARY:")
    print(f"Total .md files processed: {files_processed}")
    print(f"Total replacements made: {replacements_made}")
    print("="*50)

def fix_backslashes_in_md_files_without_brackets(directory="docs/"):
    """
    Search for .md files in the specified directory and its subdirectories,
    and remove the backslash before ')' in all .md files.
    
    Args:
        directory (str): The root directory to search for .md files
    """
    # Counters for reporting
    files_processed_b = 0
    replacements_made_b = 0
    
    # Walk through all files in the directory and its subdirectories
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if file has .md extension
            if file.endswith('.md'):
                filepath_b = os.path.join(root, file)
                
                try:
                    # Read the file content
                    with open(filepath_b, 'r', encoding='utf-8') as f:
                        content_b = f.read()
                    
                    # Count occurrences before replacement
                    occurrences_before_b = len(re.findall(r'\\\)', content_b))
                    
                    if occurrences_before_b > 0:
                        # Replace all occurrences of '\)' with ')'
                        new_content_b = content_b.replace('\\)', ')')
                        
                        # Write the modified content back to the file
                        with open(filepath_b, 'w', encoding='utf-8') as f:
                            f.write(new_content_b)
                        
                        replacements_made_b += occurrences_before_b
                        print(f"Fixed {occurrences_before_b} occurrences in: {filepath_b}")
                    else:
                        print(f"  No changes needed for: {filepath_b}")
                    
                    files_processed_b += 1
                    
                except Exception as e:
                    print(f"✗ Error processing {filepath_b}: {e}")
    
    # Summary
    print("\n" + "="*50)
    print("SUMMARY:")
    print(f"Total .md files processed: {files_processed_b}")
    print(f"Total replacements made: {replacements_made_b}")
    print("="*50)

if __name__ == "__main__":
    # You can specify a different directory by passing it as an argument
    fix_backslashes_in_md_files("docs/")
    fix_backslashes_in_md_files_without_brackets("docs/")