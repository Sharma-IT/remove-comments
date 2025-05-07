"""
Main entry point for the comment remover package.

This module allows the package to be run as a script using `python -m comment_remover`.
"""

from .cli import main

if __name__ == "__main__":
    exit(main())
