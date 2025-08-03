#!/usr/bin/env python3
"""
Script to convert custom {% img %} tags to standard markdown image syntax
Usage: python convert_image_tags.py
"""

import os
import re
import glob

def convert_image_tags(content):
    """Convert {% img %} tags to markdown image syntax"""
    
    # Pattern to match various image tag formats:
    # {% img center /path/to/image.jpg Alt text here %}
    # {% img /path/to/image.jpg Alt text here %}
    # {% img center /path/to/image.jpg %}
    # {% img /path/to/image.jpg %}
    
    pattern = r'{% img\s+(.*?)\s*%}'
    
    def replace_match(match):
        params = match.group(1).strip()
        
        if not params:
            return match.group(0)  # Return original if no parameters
        
        # Split parameters while preserving spaces in alt text
        parts = params.split()
        
        # Check if first part is an alignment keyword
        alignment_keywords = ['left', 'center', 'centre', 'right']
        has_alignment = False
        start_index = 0
        
        if parts and parts[0].lower() in alignment_keywords:
            has_alignment = True
            start_index = 1
        
        if len(parts) <= start_index:
            return match.group(0)  # Return original if not enough parts
        
        # Extract image path (should be the first non-alignment part)
        image_path = parts[start_index]
        
        # Extract alt text (everything after the image path)
        alt_text = ""
        if len(parts) > start_index + 1:
            # Rejoin the remaining parts as alt text
            alt_text = " ".join(parts[start_index + 1:])
        
        # Generate markdown image syntax
        if alt_text:
            markdown_image = f"![{alt_text}]({image_path})"
        else:
            # Use filename as alt text if no alt text provided
            filename = os.path.basename(image_path)
            name_without_ext = os.path.splitext(filename)[0]
            markdown_image = f"![{name_without_ext}]({image_path})"
        
        # If there was alignment, add it as a comment or in a div
        # For now, we'll add it as an HTML comment to preserve the intention
        if has_alignment:
            alignment = parts[0].lower()
            return f"<!-- {alignment} -->\n{markdown_image}"
        else:
            return markdown_image
    
    # Apply the replacement
    converted = re.sub(pattern, replace_match, content)
    
    return converted

def process_file(filepath):
    """Process a single markdown file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file contains image tags
        if '{% img' not in content:
            return False
        
        # Convert the tags
        converted_content = convert_image_tags(content)
        
        # Check if any changes were made
        if converted_content == content:
            return False
        
        # Write back the converted content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(converted_content)
        
        return True
        
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def preview_conversions(content):
    """Preview what conversions would be made without modifying files"""
    pattern = r'{% img\s+(.*?)\s*%}'
    matches = re.findall(pattern, content)
    
    conversions = []
    for match in matches:
        original = f"{{% img {match} %}}"
        converted = convert_image_tags(original)
        if converted != original:
            conversions.append((original, converted))
    
    return conversions

def main():
    """Main function to process all markdown files in _posts directory"""
    
    # Directory path
    posts_dir = "/Users/gaurav/work/testblog/_posts/"
    
    if not os.path.exists(posts_dir):
        print(f"Directory {posts_dir} does not exist!")
        return
    
    # Find all markdown files
    markdown_files = glob.glob(os.path.join(posts_dir, "*.md")) + \
                    glob.glob(os.path.join(posts_dir, "*.markdown"))
    
    if not markdown_files:
        print("No markdown files found in the _posts directory.")
        return
    
    print(f"Found {len(markdown_files)} markdown files to process...")
    print("\nSupported image tag formats:")
    print("  • {% img center /images/pic.jpg Alt text %} → ![Alt text](/images/pic.jpg)")
    print("  • {% img /images/pic.jpg Alt text %} → ![Alt text](/images/pic.jpg)")
    print("  • {% img center /images/pic.jpg %} → ![pic](/images/pic.jpg)")
    print("  • {% img /images/pic.jpg %} → ![pic](/images/pic.jpg)")
    print()
    
    # Ask user if they want to preview first
    preview = input("Would you like to preview conversions before applying them? (y/N): ").lower().strip()
    
    if preview == 'y' or preview == 'yes':
        print("\n" + "="*60)
        print("PREVIEW MODE - No files will be modified")
        print("="*60)
        
        total_conversions = 0
        for filepath in markdown_files:
            filename = os.path.basename(filepath)
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                conversions = preview_conversions(content)
                if conversions:
                    print(f"\n📁 {filename}:")
                    for i, (original, converted) in enumerate(conversions, 1):
                        print(f"  {i}. {original}")
                        print(f"     → {converted}")
                        total_conversions += 1
                        
            except Exception as e:
                print(f"Error reading {filepath}: {e}")
        
        if total_conversions == 0:
            print("\nNo image tags found to convert.")
            return
        
        print(f"\nTotal conversions found: {total_conversions}")
        proceed = input("\nProceed with actual conversion? (y/N): ").lower().strip()
        if proceed != 'y' and proceed != 'yes':
            print("Conversion cancelled.")
            return
        print()
    
    # Actual conversion
    converted_count = 0
    total_conversions = 0
    
    for filepath in markdown_files:
        filename = os.path.basename(filepath)
        print(f"Processing: {filename}")
        
        # Count conversions in this file
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            file_conversions = len(preview_conversions(content))
        except:
            file_conversions = 0
        
        if process_file(filepath):
            converted_count += 1
            total_conversions += file_conversions
            print(f"  ✓ Converted {file_conversions} image tag(s) in {filename}")
        else:
            print(f"  - No image tags found in {filename}")
    
    print(f"\nConversion complete!")
    print(f"Files processed: {len(markdown_files)}")
    print(f"Files with conversions: {converted_count}")
    print(f"Total image tags converted: {total_conversions}")
    
    if converted_count > 0:
        print("\nNotes:")
        print("• Alignment information (center, left, right) is preserved as HTML comments")
        print("• Alt text is preserved when provided")
        print("• When no alt text is provided, filename is used as alt text")
        print("• Review the converted files to ensure images display correctly")

if __name__ == "__main__":
    main()