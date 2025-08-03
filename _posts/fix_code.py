#!/usr/bin/env python3
"""
Script to convert Octopress codeblock tags to standard markdown code blocks
Usage: python convert_codeblocks.py
"""

import os
import re
import glob

def get_language_mapping():
    """Map common language names to their markdown identifiers"""
    return {
        'c++': 'cpp',
        'c': 'c',
        'python': 'python',
        'java': 'java',
        'javascript': 'javascript',
        'js': 'javascript',
        'html': 'html',
        'css': 'css',
        'bash': 'bash',
        'shell': 'bash',
        'ruby': 'ruby',
        'php': 'php',
        'sql': 'sql',
        'xml': 'xml',
        'json': 'json',
        'yaml': 'yaml',
        'yml': 'yaml',
        'markdown': 'markdown',
        'md': 'markdown',
        'text': 'text',
        'plain': 'text',
        'go': 'go',
        'rust': 'rust',
        'swift': 'swift',
        'kotlin': 'kotlin',
        'scala': 'scala',
        'r': 'r',
        'matlab': 'matlab',
        'perl': 'perl',
        'vim': 'vim',
        'diff': 'diff',
        'dockerfile': 'dockerfile',
        'makefile': 'makefile'
    }

def get_extension_mapping():
    """Map file extensions to their markdown language identifiers"""
    return {
        '.cpp': 'cpp',
        '.cc': 'cpp',
        '.cxx': 'cpp',
        '.c++': 'cpp',
        '.hpp': 'cpp',
        '.h': 'cpp',  # Assuming C++ headers
        '.c': 'c',
        '.py': 'python',
        '.java': 'java',
        '.js': 'javascript',
        '.ts': 'typescript',
        '.html': 'html',
        '.htm': 'html',
        '.css': 'css',
        '.scss': 'scss',
        '.sass': 'sass',
        '.sh': 'bash',
        '.bash': 'bash',
        '.zsh': 'bash',
        '.rb': 'ruby',
        '.php': 'php',
        '.sql': 'sql',
        '.xml': 'xml',
        '.json': 'json',
        '.yaml': 'yaml',
        '.yml': 'yaml',
        '.md': 'markdown',
        '.markdown': 'markdown',
        '.txt': 'text',
        '.go': 'go',
        '.rs': 'rust',
        '.swift': 'swift',
        '.kt': 'kotlin',
        '.kts': 'kotlin',
        '.scala': 'scala',
        '.r': 'r',
        '.R': 'r',
        '.m': 'matlab',
        '.pl': 'perl',
        '.vim': 'vim',
        '.diff': 'diff',
        '.patch': 'diff',
        '.dockerfile': 'dockerfile',
        '.makefile': 'makefile',
        '.make': 'makefile',
        '.gradle': 'gradle',
        '.xml': 'xml',
        '.toml': 'toml',
        '.ini': 'ini',
        '.cfg': 'ini',
        '.conf': 'text'
    }

def convert_codeblock_tags(content):
    """Convert {% codeblock %} and {% endcodeblock %} tags to markdown"""
    
    language_map = get_language_mapping()
    extension_map = get_extension_mapping()
    
    # Pattern to match various codeblock formats:
    # {% codeblock lang:language %}
    # {% codeblock lang:language filename.ext %}
    # {% codeblock lang:language Title or description %}
    # {% codeblock filename.ext %}
    # {% codeblock %}
    pattern = r'{% codeblock(?:\s+(.*?))?\s*%}(.*?){% endcodeblock %}'
    
    def replace_match(match):
        params = match.group(1)         # Everything after 'codeblock'
        code_content = match.group(2)   # the actual code
        
        # Clean up the code content
        code_content = code_content.strip()
        
        # Determine the language
        markdown_lang = ''
        
        if params:
            params = params.strip()
            
            # Check if it starts with lang:
            if params.startswith('lang:'):
                # Extract the language part
                lang_match = re.match(r'lang:(\w+)', params)
                if lang_match:
                    language = lang_match.group(1).lower()
                    markdown_lang = language_map.get(language, language)
            else:
                # No explicit lang: prefix, try to infer from extension
                # Look for something that looks like a filename (has an extension)
                words = params.split()
                for word in words:
                    if '.' in word:
                        import os
                        _, ext = os.path.splitext(word.lower())
                        if ext in extension_map:
                            markdown_lang = extension_map[ext]
                            break
                # If no extension found, leave empty (could be a title/description)
        
        # Return the markdown code block
        return f'```{markdown_lang}\n{code_content}\n```'
    
    # Apply the replacement
    converted = re.sub(pattern, replace_match, content, flags=re.DOTALL)
    
    return converted

def process_file(filepath):
    """Process a single markdown file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file contains codeblock tags
        if '{% codeblock' not in content:
            return False
        
        # Convert the tags
        converted_content = convert_codeblock_tags(content)
        
        # Write back the converted content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(converted_content)
        
        return True
        
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

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
    print("\nSupported codeblock formats:")
    print("  • {% codeblock lang:cpp %} → ```cpp")
    print("  • {% codeblock lang:cpp FordFulkerson.cpp %} → ```cpp") 
    print("  • {% codeblock lang:cpp Augmenting the path %} → ```cpp")
    print("  • {% codeblock example.cpp %} → ```cpp") 
    print("  • {% codeblock %} → ``` (for pseudo-code)")
    print()
    
    converted_count = 0
    
    for filepath in markdown_files:
        filename = os.path.basename(filepath)
        print(f"Processing: {filename}")
        
        if process_file(filepath):
            converted_count += 1
            print(f"  ✓ Converted codeblocks in {filename}")
        else:
            print(f"  - No codeblocks found in {filename}")
    
    print(f"\nConversion complete!")
    print(f"Files processed: {len(markdown_files)}")
    print(f"Files with conversions: {converted_count}")
    
    if converted_count > 0:
        print("\nRecommendation: Review the converted files to ensure the language")
        print("identifiers are correct and the code formatting looks good.")
        print("\nExample conversions:")
        print("  {% codeblock lang:python %} → ```python")
        print("  {% codeblock lang:cpp main.cpp %} → ```cpp")
        print("  {% codeblock lang:java Finding the solution %} → ```java")
        print("  {% codeblock main.cpp %} → ```cpp")
        print("  {% codeblock algorithm %} → ``` (pseudo-code)")



if __name__ == "__main__":
    main()
