import os
import re
import textwrap

# === SETTINGS ===
input_folder = "./"              # Folder where your ch01_*.md files live
output_file = "ch02.typ"         # Output Typst file
file_prefix = "ch02_"            # Prefix for chapter 2 files

# --- Typst Table Conversion Function ---
def convert_md_table(md_block):
    # print(f"\n--- Entering convert_md_table ---") # Debug print
    # print(f"Received MD block:\n{md_block.strip()[:200]}...") # Debug print

    lines = md_block.strip().split('\n')

    # Basic validation for a table-like structure (header, separator, at least one data line)
    if len(lines) < 3:
        # print(f"DEBUG: Table block too short ({len(lines)} lines). Returning original.") # Debug print
        return md_block
    if not lines[0].strip().startswith('|'):
        # print(f"DEBUG: First line does not start with '|'. Returning original.") # Debug print
        return md_block
    if not lines[1].strip().startswith('|'):
        # print(f"DEBUG: Second line does not start with '|'. Returning original.") # Debug print
        return md_block

    # Robustly split a row into cells
    def split_row(row):
        cells = [cell.strip() for cell in row.strip().split('|')]
        # Filter out empty strings from splitting on leading/trailing pipes
        if cells and cells[0] == '':
            cells = cells[1:]
        if cells and cells[-1] == '':
            cells = cells[:-1]
        return cells

    header = split_row(lines[0])
    separator_line = lines[1]

    # Validate header has content and separator line is valid (contains pipes and dashes/colons)
    if not header:
        # print(f"DEBUG: Header is empty after splitting. Returning original.") # Debug print
        return md_block
    
    # This regex is more flexible for any number of columns
    # It checks for a pattern of | followed by optional whitespace,
    # then at least one dash or colon, then optional whitespace,
    # repeating this pattern and ending with a |
    if not re.match(r'^\s*\|(?:\s*[\-\:]+\s*\|)+\s*$', separator_line.strip()):
        # print(f"DEBUG: Separator line invalid: '{separator_line.strip()}'. Returning original.") # Debug print
        return md_block

    body_lines = lines[2:]
    body_rows = [split_row(line) for line in body_lines if line.strip().startswith('|')]

    col_count = len(header)
    if col_count == 0:
        # print(f"DEBUG: Column count is 0. Returning original.") # Debug print
        return md_block

    # Ensure all body rows have a consistent column count matching the header
    for r_idx, row in enumerate(body_rows):
        if len(row) != col_count:
            # print(f"DEBUG: Inconsistent column count in body row {r_idx+1}. Expected {col_count}, got {len(row)}. Returning original.") # Debug print
            return md_block

    # Convert cell content to Typst string format (escape backslashes, quotes, convert <br>)
    def convert_cell(cell):
        # Escape backslashes and square brackets, but not quotes, as we're now in a content block.
        # We also need to handle newlines from <br>
        escaped_cell = cell.replace('\\', '\\\\').replace('[', '\[').replace(']', '\]').replace('<br>', '\n')
        return f'[{escaped_cell}]' # Now returns a Typst content block

    # Format a list of cells into a Typst row array: ["[cell1]", "[cell2]"]
    def quote_row(row):
        return "[" + ", ".join(convert_cell(cell) for cell in row) + "]"

    # CHANGE 1: Use 'auto' for columns
    column_spec = ", ".join(["auto"] * col_count)

    # Combine header and body rows for Typst table rows argument
    row_lines = [quote_row(header)] + [quote_row(row) for row in body_rows]
    
    # Typst expects cells directly in 'rows', not sub-arrays for each row.
    # So, we need to flatten the list of lists of cells into a single list of cells.
    flattened_cells_str = []
    for row_str in row_lines:
        # Strip the leading '[' and trailing ']' from each row_str, then add to list
        flattened_cells_str.append(row_str.strip()[1:-1]) 
    
    # Finally, join all the flattened cell strings with a comma and newline for formatting
    rows_content_formatted = ",\n    ".join(flattened_cells_str)

    # Assemble the final Typst table block (using parentheses for columns and rows arguments)
    table_typ = (
        "#table(\n  inset: 4pt,\n  stroke: 1pt,\n  fill: none,\n"
        f"  columns: ({column_spec}),\n"
        # CHANGE 2: Add 'rows: (auto),'
        "  rows: (auto),\n"
        f"  {rows_content_formatted}\n" # This line now directly contains the cell content
        ")\n"
    )
    # print(f"--- Exiting convert_md_table. Converted to Typst. ---") # Debug print
    return table_typ

# --- Markdown → Typst conversions ---
def md_to_typst(text):
    lines = text.splitlines(keepends=True)
    processed_output_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped_line = line.strip()

        # print(f"DEBUG: Processing line {i+1}: '{stripped_line[:50]}...'") # Debug print

        # Check if the current line could be the start of a Markdown table (starts with '|')
        # and look ahead for the separator line to confirm it's a table
        is_potential_table_start = stripped_line.startswith('|') and \
                                   i + 1 < len(lines) and \
                                   lines[i+1].strip().startswith('|') and \
                                   re.search(r'\|\s*[\-\:]+\s*\|', lines[i+1]) # Updated regex for separator check
                                   
        if is_potential_table_start:
            # print(f"DEBUG: Potential table start detected at line {i+1}.") # Debug print
            table_lines = []
            current_table_start_index = i
            # Accumulate all lines that start with '|' (or are just whitespace)
            # as part of the table block. Stop when a non-table-like line is found.
            while i < len(lines):
                current_line_strip = lines[i].strip()
                if not current_line_strip.startswith('|') and current_line_strip != "":
                    # If it's not a table line and not just an empty line, break the table accumulation
                    break
                # Only add if it's a pipe-delimited line or an empty line right after a table line
                if current_line_strip.startswith('|') or current_line_strip == "":
                    table_lines.append(lines[i])
                else:
                    break # Stop if it's content that clearly breaks the table
                i += 1
            
            md_table_block = "".join(table_lines)
            # print(f"DEBUG: Extracted MD table block (approx):\n{md_table_block.strip()[:200]}...") # Debug print
            
            typst_table_block = convert_md_table(md_table_block)
            processed_output_lines.append(typst_table_block)
            
            # Continue the outer loop from where the table parsing ended
            continue 
            
        # If not a table line, or if the lookahead failed, process as regular text
        processed_output_lines.append(line)
        i += 1

    # Join the lines back and apply other Markdown to Typst conversions
    intermediate_text = "".join(processed_output_lines)

    # Apply other regex substitutions:
    intermediate_text = re.sub(r'^# (.*)', r'#pagebreak()\n= \1', intermediate_text, flags=re.M)
    intermediate_text = re.sub(r'^## (.*)', r'== \1', intermediate_text, flags=re.M)
    intermediate_text = re.sub(r'^### (.*)', r'=== \1', intermediate_text, flags=re.M)
    intermediate_text = re.sub(r'^#### (.*)', r'==== \1', intermediate_text, flags=re.M)
    intermediate_text = re.sub(r'^##### (.*)', r'===== \1', intermediate_text, flags=re.M)
    intermediate_text = re.sub(r'^###### (.*)', r'====== \1', intermediate_text, flags=re.M)
    
    intermediate_text = re.sub(r'^\* ', r'- ', intermediate_text, flags=re.M)
    intermediate_text = re.sub(r'\*\*(.*?)\*\*', r'*\1*', intermediate_text)
    intermediate_text = re.sub(r'(?<!\*)\*(?!\*)(.*?)(?<!\*)\*(?!\*)', r'_\1_', intermediate_text)
    intermediate_text = re.sub(r'_(.*?)_', r'_\1_', intermediate_text)
    intermediate_text = re.sub(r'\[\[(.*?)\]\]', r'\1', intermediate_text)
    intermediate_text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', intermediate_text)
    intermediate_text = re.sub(r'^---$', r'#line()', intermediate_text, flags=re.M)
    intermediate_text = re.sub(r'\n\n+', '\n\n', intermediate_text)
    intermediate_text = re.sub(r'[ \t]+$', '', intermediate_text, flags=re.M)

    return intermediate_text

# --- Main Process ---
def convert_chapter():
    files = sorted(f for f in os.listdir(input_folder) if f.startswith(file_prefix) and f.endswith('.md'))
    if not files:
        print("No files found matching the prefix and extension.")
        return

    output_content = []
    for filename in files:
        filepath = os.path.join(input_folder, filename)
        print(f"\n===== Processing file: {filename} =====")
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                md_text = f.read()
                typ_text = md_to_typst(md_text)
                output_content.append(typ_text)
        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")
            continue
            

    # Join all processed chapter content and write to the output file
    with open(output_file, 'w', encoding='utf-8') as f_out:
        f_out.write('\n'.join(output_content))

    print(f"\n✅ Successfully converted {len(files)} files to {output_file}")
    print(f"Please check '{output_file}' and the console output for debug messages.")

if __name__ == "__main__":
    convert_chapter()