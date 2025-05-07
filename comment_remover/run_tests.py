#!/usr/bin/env python3
"""
Script to run the tests for the comment_remover package.
"""

import unittest
import sys
import os

# Add the parent directory to the path so we can import the tests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the tests
from tests.test_comment_remover import TestCommentRemover

if __name__ == '__main__':
    # Run the tests
    unittest.main(module='tests.test_comment_remover')
