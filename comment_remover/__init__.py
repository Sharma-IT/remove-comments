"""
Comment Remover - A tool to remove comments from code files.

This package provides functionality to remove comments from various types of code files,
including single-line and multi-line comments, while preserving the code structure.
"""

from .core import process_comments, detect_file_type, COMMENT_PATTERNS

__version__ = '1.0.0'
