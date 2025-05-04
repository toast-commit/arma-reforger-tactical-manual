#!/usr/bin/env python3
import re
import sys
import os
import shutil

def sanitize_filename(filename):
    """Convert heading text to valid filename"""
    # Remove BBCode tags
    filename = re.sub(r'\[.*?\]', '', filename)
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    # Remove special characters
    filename = re.sub(r'[^a-zA-Z0-9_-]', '', filename)
    # Limit length
    filename = filename[:50]
    return filename

def split_bbcode_by_h1(input_file):
    """Split BBCode file by H1 headings"""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create output directory
        output_dir = 'bbcode_sections'
        
        # Clear the directory if it exists
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        os.makedirs(output_dir)
        
        # Find all H1 sections
        sections = re.split(r'(\[h1\].*?\[/h1\])', content)
        
        current_heading = None
        current_content = []
        created_files = []
        
        # Process sections
        for i, section in enumerate(sections):
            if re.match(r'\[h1\].*?\[/h1\]', section):
                # Save previous section if exists
                if current_heading and current_content:
                    filename = sanitize_filename(current_heading) + '.bbcode'
                    filepath = os.path.join(output_dir, filename)
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(f"[h1]{current_heading}[/h1]\n")
                        f.write(''.join(current_content))
                    created_files.append(filename)
                    print(f"Created: {filepath}")
                
                # Start new section
                current_heading = re.sub(r'\[h1\](.*?)\[/h1\]', r'\1', section)
                current_content = []
            else:
                if current_heading:  # Only add content if we have a heading
                    current_content.append(section)
                elif section.strip():  # Content before first H1
                    filename = '00_Introduction.bbcode'
                    filepath = os.path.join(output_dir, filename)
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(section)
                    created_files.append(filename)
                    print(f"Created: {filepath}")
        
        # Save last section
        if current_heading and current_content:
            filename = sanitize_filename(current_heading) + '.bbcode'
            filepath = os.path.join(output_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"[h1]{current_heading}[/h1]\n")
                f.write(''.join(current_content))
            created_files.append(filename)
            print(f"Created: {filepath}")
        
        print(f"Successfully split {input_file} into {len(created_files)} sections in {output_dir}/")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python split_bbcode_sections.py input.bbcode")
        sys.exit(1)
    
    input_file = sys.argv[1]
    split_bbcode_by_h1(input_file)
