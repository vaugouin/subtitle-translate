import re
import sys
import os
import argparse
from pathlib import Path

def normalize_srt(input_file, output_file=None):
    """
    Normalizes SRT subtitle file by ensuring consistent newline characters
    and proper formatting between subtitle entries.
    
    Args:
        input_file (str): Path to the input SRT file
        output_file (str, optional): Path to save the normalized file. 
                                    If None, will add '_normalized' to the original filename
    
    Returns:
        str: Path to the normalized file
    """
    # Determine output file path if not provided
    if output_file is None:
        input_path = Path(input_file)
        output_file = str(input_path.with_stem(f"{input_path.stem}_normalized"))
    
    # Try different encodings to open the file correctly
    encodings = ['utf-8', 'utf-8-sig', 'cp1251', 'latin1']
    content = None
    
    for encoding in encodings:
        try:
            with open(input_file, 'r', encoding=encoding) as f:
                content = f.read()
            print(f"Successfully read file with encoding: {encoding}")
            break
        except UnicodeDecodeError:
            print(f"Failed to read with encoding: {encoding}")
    
    if content is None:
        raise ValueError("Could not read the file with any of the attempted encodings")
    
    # Ensure consistent newline characters (convert to \n)
    content = content.replace('\r\n', '\n').replace('\r', '\n')
    
    # Regular expression to identify subtitle entries
    # A subtitle entry consists of:
    # 1. Number (digits)
    # 2. Timestamp (00:00:00,000 --> 00:00:00,000)
    # 3. One or more lines of text
    # 4. Empty line to separate from next entry
    
    # First normalize entry structure with proper newlines
    pattern = re.compile(r'(\d+)\s*\n([\d:,]+\s*-->\s*[\d:,]+)\s*\n(.*?)(?=\n\s*\n\s*\d+\n|\Z)', 
                         re.DOTALL)
    
    def normalize_entry(match):
        num = match.group(1).strip()
        timestamp = match.group(2).strip()
        text = match.group(3).strip()
        
        # Ensure text has consistent newlines (not too many, not too few)
        text = re.sub(r'\n{2,}', '\n', text)
        
        return f"{num}\n{timestamp}\n{text}\n\n"
    
    normalized_content = pattern.sub(normalize_entry, content)
    
    # Remove any extra blank lines at the beginning or end
    normalized_content = normalized_content.strip() + '\n'
    
    # Write the normalized content to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(normalized_content)
    
    return output_file

def main():
    parser = argparse.ArgumentParser(description='Normalize SRT subtitle files')
    parser.add_argument('input_file', help='Path to the input SRT file')
    parser.add_argument('-o', '--output', help='Path to save the normalized file (optional)')
    
    args = parser.parse_args()
    
    try:
        output_file = normalize_srt(args.input_file, args.output)
        print(f"Normalized SRT file saved to: {output_file}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
