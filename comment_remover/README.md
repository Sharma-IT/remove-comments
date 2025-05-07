# Comment Remover

A versatile tool to remove comments from code files of various programming languages.

## Features

- Supports multiple programming languages and file types
- Removes single-line and multi-line comments
- Preserves code structure and formatting
- Handles string literals correctly (doesn't remove comment-like patterns inside strings)
- Provides command-line interface with various options
- Can process files in-place or output to a new file

## Supported Languages

The tool supports a wide range of programming languages and file types, including:

- C-style languages (C, C++, Java, JavaScript, etc.)
- Python
- HTML/XML
- CSS/SCSS/LESS
- SQL
- Shell scripts
- Ruby
- Lua
- PowerShell
- YAML
- Perl
- R
- Haskell
- Batch files

## Installation

### From PyPI

```bash
pip install comment-remover
```

### From Source

```bash
git clone https://github.com/Sharma-IT/comment-remover.git
cd comment-remover
pip install .
```

## Usage

### Command-line Interface

```bash
# Basic usage (prints to console)
comment-remover file.py

# Output to a new file
comment-remover file.py -o file_no_comments.py

# Modify the file in-place (creates a backup)
comment-remover file.py -i

# Force a specific file type
comment-remover file.txt -t python

# Show verbose information
comment-remover file.py -v

# List all supported file types
comment-remover --list-types
```

### Python API

```python
from comment_remover import process_comments, detect_file_type, COMMENT_PATTERNS

# Process a file
file_path = 'file.py'
file_type, patterns = detect_file_type(file_path)

with open(file_path, 'r') as f:
    content = f.read()

# Remove comments
cleaned_content = process_comments(content, file_type, patterns)

# Write to a new file
with open('file_no_comments.py', 'w') as f:
    f.write(cleaned_content)
```

## Command-line Options

- `input_file`: Path to the input file
- `-o, --output`: Path to the output file (if not provided, prints to console)
- `-i, --in-place`: Modify the input file directly (creates a backup)
- `-t, --type`: Force a specific file type (e.g., python, c_style, css, etc.)
- `-l, --list-types`: List all supported file types and exit
- `-v, --verbose`: Print verbose information about the file type detection

## Examples

### Remove comments from a Python file

```bash
comment-remover script.py -o script_clean.py
```

### Remove comments from a JavaScript file in-place

```bash
comment-remover app.js -i
```

### Process a file with an unknown extension as Python

```bash
comment-remover data.txt -t python
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Shubham Sharma - [GitHub](https://github.com/Sharma-IT)
