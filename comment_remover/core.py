"""
Core functionality for the comment remover.

This module contains the main functions for detecting file types and removing comments.
"""

import re
import mimetypes
from pathlib import Path

# Dictionary of file types and their comment patterns
COMMENT_PATTERNS = {
    # C-style languages (C, C++, Java, JavaScript, C#, etc.)
    'c_style': {
        'extensions': ['.c', '.cpp', '.h', '.hpp', '.java', '.js', '.jsx', '.ts', '.tsx', '.cs', '.php', '.swift', '.go', '.kt', '.scala'],
        'single_line': '//',
        'multi_line': ('/*', '*/'),
        'string_literals': ['"', "'", '`']  # For avoiding comments in strings
    },
    # Shell scripts
    'shell': {
        'extensions': ['.sh', '.bash', '.zsh', '.ksh'],
        'single_line': '#',
        'multi_line': None,
        'string_literals': ['"', "'"]
    },
    # Python
    'python': {
        'extensions': ['.py', '.pyw', '.pyc', '.pyo', '.pyd'],
        'single_line': '#',
        'multi_line': ('"""', '"""'),  # Python also has ''' but we'll handle that separately
        'string_literals': ['"', "'"]
    },
    # Ruby
    'ruby': {
        'extensions': ['.rb', '.rake', '.gemspec'],
        'single_line': '#',
        'multi_line': ('=begin', '=end'),
        'string_literals': ['"', "'"]
    },
    # HTML/XML
    'markup': {
        'extensions': ['.html', '.htm', '.xml', '.svg', '.xhtml', '.jsp', '.asp', '.aspx'],
        'single_line': None,
        'multi_line': ('<!--', '-->'),
        'string_literals': ['"', "'"]
    },
    # CSS/SCSS/LESS
    'css': {
        'extensions': ['.css', '.scss', '.sass', '.less'],
        'single_line': '//',  # SCSS/LESS only
        'multi_line': ('/*', '*/'),
        'string_literals': ['"', "'"]
    },
    # SQL
    'sql': {
        'extensions': ['.sql', '.sqlite', '.pgsql'],
        'single_line': '--',
        'multi_line': ('/*', '*/'),
        'string_literals': ['"', "'"]
    },
    # Lua
    'lua': {
        'extensions': ['.lua'],
        'single_line': '--',
        'multi_line': ('--[[', ']]'),
        'string_literals': ['"', "'"]
    },
    # PowerShell
    'powershell': {
        'extensions': ['.ps1', '.psm1', '.psd1'],
        'single_line': '#',
        'multi_line': ('<#', '#>'),
        'string_literals': ['"', "'"]
    },
    # YAML
    'yaml': {
        'extensions': ['.yaml', '.yml'],
        'single_line': '#',
        'multi_line': None,
        'string_literals': ['"', "'"]
    },
    # Perl
    'perl': {
        'extensions': ['.pl', '.pm', '.t'],
        'single_line': '#',
        'multi_line': ('=pod', '=cut'),
        'string_literals': ['"', "'", '`']
    },
    # R
    'r': {
        'extensions': ['.r', '.R'],
        'single_line': '#',
        'multi_line': None,
        'string_literals': ['"', "'"]
    },
    # Haskell
    'haskell': {
        'extensions': ['.hs', '.lhs'],
        'single_line': '--',
        'multi_line': ('{-', '-}'),
        'string_literals': ['"', "'"]
    },
    # Batch files
    'batch': {
        'extensions': ['.bat', '.cmd'],
        'single_line': 'REM',
        'multi_line': None,
        'string_literals': ['"']
    }
}


def detect_file_type(file_path):
    """
    Detect the file type based on extension or content.
    
    Args:
        file_path (str): Path to the file to detect.
        
    Returns:
        tuple: A tuple containing the file type name and its comment patterns.
    """
    ext = Path(file_path).suffix.lower()
    
    # First try to match by extension
    for file_type, patterns in COMMENT_PATTERNS.items():
        if ext in patterns['extensions']:
            return file_type, patterns
    
    # If extension not found, try to use mimetype
    mime_type, _ = mimetypes.guess_type(file_path)
    
    if mime_type:
        if mime_type.startswith('text/x-python'):
            return 'python', COMMENT_PATTERNS['python']
        elif mime_type.startswith('text/html') or mime_type.startswith('application/xml'):
            return 'markup', COMMENT_PATTERNS['markup']
        elif mime_type.startswith('text/css'):
            return 'css', COMMENT_PATTERNS['css']
        elif mime_type.startswith('application/javascript') or mime_type.startswith('text/javascript'):
            return 'c_style', COMMENT_PATTERNS['c_style']
        elif mime_type.startswith('text/x-sql'):
            return 'sql', COMMENT_PATTERNS['sql']
    
    # Default to C-style as a fallback (most common)
    return 'unknown', COMMENT_PATTERNS['c_style']


def process_comments(content, file_type=None, patterns=None):
    """
    Process comments in the given content based on the file type.
    
    Args:
        content (str): The content to process.
        file_type (str, optional): The file type. Defaults to None.
        patterns (dict, optional): The comment patterns. Defaults to None.
        
    Returns:
        str: The processed content with comments removed.
    """
    if not patterns:
        # Default to C-style if no patterns provided
        patterns = COMMENT_PATTERNS['c_style']
    
    # Process multi-line comments if the file type supports them
    if patterns['multi_line']:
        start_pattern, end_pattern = patterns['multi_line']
        
        # Handle different multi-line comment patterns
        if start_pattern == '/*' and end_pattern == '*/':
            # C-style comments - need to handle the special regex characters
            # Use a more direct approach to find and remove C-style comments
            i = 0
            result = []
            while i < len(content):
                # Look for the start of a comment
                start_idx = content.find('/*', i)
                if start_idx == -1:
                    # No more comments, add the rest of the content
                    result.append(content[i:])
                    break
                
                # Add the content before the comment
                result.append(content[i:start_idx])
                
                # Find the end of the comment
                end_idx = content.find('*/', start_idx)
                if end_idx == -1:
                    # Unclosed comment, treat the rest as a comment
                    break
                
                # Skip past the end of the comment
                i = end_idx + 2
            
            content = ''.join(result)
        elif start_pattern == '<!--' and end_pattern == '-->':
            # HTML/XML comments
            content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
        elif start_pattern == '"""' and end_pattern == '"""':
            # Python triple double quotes
            content = re.sub(r'""".*?"""', '', content, flags=re.DOTALL)
        elif start_pattern == "'''" and end_pattern == "'''":
            # Python triple single quotes
            content = re.sub(r"'''.*?'''", '', content, flags=re.DOTALL)
        else:
            # Generic handling for other multi-line comment formats
            start_pattern_escaped = re.escape(start_pattern)
            end_pattern_escaped = re.escape(end_pattern)
            multiline_pattern = f"{start_pattern_escaped}.*?{end_pattern_escaped}"
            multiline_comment_pattern = re.compile(multiline_pattern, re.DOTALL)
            content = multiline_comment_pattern.sub('', content)
    
    # Special handling for Python triple quotes
    if file_type == 'python':
        # Handle triple single quotes
        content = re.sub(r"'''.*?'''", '', content, flags=re.DOTALL)
        # Handle triple double quotes
        content = re.sub(r'""".*?"""', '', content, flags=re.DOTALL)
    
    # Process single-line comments if the file type supports them
    if patterns['single_line']:
        processed_lines = []
        single_line_pattern = patterns['single_line']
        
        for line in content.splitlines():
            stripped_line = line.strip()
            
            # Check if the line IS ONLY a single-line comment (potentially indented)
            if stripped_line and stripped_line.startswith(single_line_pattern):
                # Replace the entire line with a blank line
                processed_lines.append('')
                continue
            
            # Check if the line CONTAINS a single-line comment after some code
            try:
                # Find all occurrences of the comment pattern
                comment_indices = [i for i in range(len(line)) 
                                  if line[i:i+len(single_line_pattern)] == single_line_pattern]
                
                if not comment_indices:
                    # No comment pattern found
                    processed_lines.append(line)
                    continue
                
                # Find the first valid comment (not in a string)
                valid_comment_index = -1
                
                for comment_index in comment_indices:
                    # Skip if this is part of a string literal
                    in_string = False
                    string_char = None
                    escaped = False
                    
                    for i in range(comment_index):
                        char = line[i]
                        
                        # Handle escape sequences
                        if escaped:
                            escaped = False
                            continue
                        
                        if char == '\\':
                            escaped = True
                            continue
                        
                        # Check for string literals
                        if char in patterns['string_literals']:
                            if not in_string:
                                # Start of string
                                in_string = True
                                string_char = char
                            elif char == string_char:
                                # End of string
                                in_string = False
                                string_char = None
                    
                    # If we're not in a string at the comment position, it's a valid comment
                    if not in_string:
                        # Heuristic: Avoid replacing '//' if it looks like part of a URL protocol
                        is_likely_url_protocol = False
                        if comment_index > 0 and line[comment_index-1] == ':':
                            is_likely_url_protocol = True
                        
                        if not is_likely_url_protocol:
                            valid_comment_index = comment_index
                            break
                
                if valid_comment_index >= 0:
                    # Keep only the part *before* the comment, preserving trailing whitespace
                    code_part = line[:valid_comment_index].rstrip()
                    processed_lines.append(code_part)
                else:
                    # No valid comment found, keep the original line
                    processed_lines.append(line)
                continue
            
            except ValueError:
                # No comment pattern found in the line, treat it as a regular code line
                pass
            
            # If the line wasn't a full comment and didn't have a trailing comment removed,
            # add the original line (whitespace included)
            processed_lines.append(line)
        
        # Join the processed lines back together
        content = '\n'.join(processed_lines)
    
    # Collapse multiple consecutive blank lines into a maximum of one blank line
    content = re.sub(r'\n(\s*\n)+', '\n\n', content)
    
    # Ensure the file ends with a single newline for POSIX compatibility
    return content.strip() + '\n'
