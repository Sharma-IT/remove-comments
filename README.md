# Comment Remover

A versatile tool to remove comments from code files of various programming languages.

## Features

- Supports multiple programming languages and file types
- Removes single-line and multi-line comments
- Preserves code structure and formatting
- Handles string literals correctly (doesn't remove comment-like patterns inside strings)
- Provides command-line interface with various options
- Can process files in-place or output to a new file

## Project Structure

```
comment-remover/
├── comment_remover/         # Main package
│   ├── __init__.py          # Package initialization
│   ├── core.py              # Core functionality
│   ├── cli.py               # Command-line interface
│   └── __main__.py          # Entry point for python -m comment_remover
├── tests/                   # Test package
│   ├── __init__.py          # Test package initialization
│   └── test_comment_remover.py  # Test cases
├── setup.py                 # Installation script
├── setup.cfg                # Package configuration
├── requirements.txt         # Dependencies
├── README.md                # This file
├── LICENSE                  # MIT License
├── MANIFEST.in              # Package manifest
├── .gitignore               # Git ignore file
├── run_tests.py             # Script to run tests
└── comment-remover          # Command-line script
```

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/Sharma-IT/comment-remover.git
cd comment-remover

# Install the package
pip install .

# Or install in development mode
pip install -e .
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

## Running Tests

```bash
# Run tests using the provided script
python run_tests.py

# Or run tests directly
python -m unittest discover tests
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Shubham Sharma - [GitHub](https://github.com/Sharma-IT)
