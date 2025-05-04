#!/usr/bin/env python3
import re
import sys

def markdown_to_bbcode(markdown_text):
    # Convert headers
    text = re.sub(r'^# (.*?)$', r'[h1]\1[/h1]', markdown_text, flags=re.MULTILINE)
    text = re.sub(r'^## (.*?)$', r'[h2]\1[/h2]', text, flags=re.MULTILINE)
    text = re.sub(r'^### (.*?)$', r'[h3]\1[/h3]', text, flags=re.MULTILINE)
    text = re.sub(r'^#### (.*?)$', r'[b]\1[/b]', text, flags=re.MULTILINE)
    
    # Convert emphasis
    text = re.sub(r'\*\*\*(.*?)\*\*\*', r'[b][i]\1[/i][/b]', text)
    text = re.sub(r'\*\*(.*?)\*\*', r'[b]\1[/b]', text)
    text = re.sub(r'\*(.*?)\*', r'[i]\1[/i]', text)
    text = re.sub(r'__(.*?)__', r'[b]\1[/b]', text)
    text = re.sub(r'_(.*?)_', r'[i]\1[/i]', text)
    
    # Convert links
    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'[url=\2]\1[/url]', text)
    
    # Convert images
    text = re.sub(r'!\[(.*?)\]\((.*?)\)', r'[img]\2[/img]', text)
    
    # Convert unordered lists
    text = re.sub(r'^[\*\-] (.*?)$', r'[*]\1', text, flags=re.MULTILINE)
    
    # Convert ordered lists (simple approach)
    text = re.sub(r'^\d+\. (.*?)$', r'[*]\1', text, flags=re.MULTILINE)
    
    # Convert code blocks
    text = re.sub(r'```(.*?)```', r'[code]\1[/code]', text, flags=re.DOTALL)
    text = re.sub(r'`(.*?)`', r'[code]\1[/code]', text)
    
    # Convert blockquotes
    text = re.sub(r'^> (.*?)$', r'[quote]\1[/quote]', text, flags=re.MULTILINE)
    
    # Convert horizontal rules
    text = re.sub(r'^---$', r'[hr][/hr]', text, flags=re.MULTILINE)
    
    # Convert tables to preformatted text (BBCode doesn't have native tables)
    def convert_table(match):
        table = match.group(0)
        return '[code]\n' + table + '\n[/code]'
    
    text = re.sub(r'\|.*\|(\n\|[-:| ]+\|)?(\n\|.*\|)*', convert_table, text)
    
    return text

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python convert_to_bbcode.py input.md output.bbcode")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        bbcode_content = markdown_to_bbcode(markdown_content)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(bbcode_content)
        
        print(f"Successfully converted {input_file} to {output_file}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
