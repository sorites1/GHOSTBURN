separator_line_example = '| ---- | --------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |'

print(f"Original length: {len(separator_line_example)}")
print(f"Stripped length: {len(separator_line_example.strip())}")

print("\nCharacter codes in the stripped separator line:")
for i, char in enumerate(separator_line_example.strip()):
    print(f"Index {i}: '{char}' (ord: {ord(char)})")

print("\nFull separator line (raw, with escapes):")
print(repr(separator_line_example))