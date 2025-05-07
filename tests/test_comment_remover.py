"""
Tests for the comment remover package.
"""

import unittest
import os
import tempfile
import shutil
import sys

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from comment_remover.core import process_comments, detect_file_type, COMMENT_PATTERNS


class TestCommentRemover(unittest.TestCase):
    """Test cases for the comment remover package."""

    def setUp(self):
        """Set up the test environment."""
        # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up the test environment."""
        # Clean up the temporary directory
        shutil.rmtree(self.test_dir)

    def test_c_style_comments(self):
        """Test C-style comments (C, C++, Java, JavaScript, etc.)"""
        content = """// This is a single-line comment
int main() {
    // This is another single-line comment
    int x = 5; // This is a trailing comment
    /* This is a
       multi-line comment */
    int y = 10;
    return 0; // Return statement
}"""
        # Create a temporary file to test the actual implementation
        test_file = os.path.join(self.test_dir, "test.c")
        with open(test_file, 'w') as f:
            f.write(content)

        # Process the file using our implementation
        file_type, patterns = detect_file_type(test_file)
        result = process_comments(content, file_type, patterns)

        # Check that comments are removed
        self.assertNotIn("// This is a single-line comment", result)
        self.assertNotIn("// This is another single-line comment", result)
        self.assertNotIn("// This is a trailing comment", result)
        self.assertNotIn("/* This is a\n       multi-line comment */", result)
        self.assertNotIn("// Return statement", result)

        # Check that code is preserved
        self.assertIn("int main() {", result)
        self.assertIn("int x = 5;", result)
        self.assertIn("int y = 10;", result)
        self.assertIn("return 0;", result)
        self.assertIn("}", result)

    def test_python_comments(self):
        """Test Python comments"""
        content = """# This is a single-line comment
def main():
    # This is another single-line comment
    x = 5  # This is a trailing comment
    '''This is a
       multi-line comment'''
    y = 10
    return 0  # Return statement
"""
        # Create a temporary file to test the actual implementation
        test_file = os.path.join(self.test_dir, "test.py")
        with open(test_file, 'w') as f:
            f.write(content)

        # Process the file using our implementation
        file_type, patterns = detect_file_type(test_file)
        result = process_comments(content, file_type, patterns)

        # Check that comments are removed
        self.assertNotIn("# This is a single-line comment", result)
        self.assertNotIn("# This is another single-line comment", result)
        self.assertNotIn("# This is a trailing comment", result)
        self.assertNotIn("'''This is a\n       multi-line comment'''", result)
        self.assertNotIn("# Return statement", result)

        # Check that code is preserved
        self.assertIn("def main():", result)
        self.assertIn("x = 5", result)
        self.assertIn("y = 10", result)
        self.assertIn("return 0", result)

    def test_html_comments(self):
        """Test HTML comments"""
        content = """<!DOCTYPE html>
<html>
<head>
    <title>Test</title>
    <!-- This is an HTML comment -->
</head>
<body>
    <!-- This is another
         multi-line comment -->
    <h1>Hello World</h1>
</body>
</html>"""
        # Create a temporary file to test the actual implementation
        test_file = os.path.join(self.test_dir, "test.html")
        with open(test_file, 'w') as f:
            f.write(content)

        # Process the file using our implementation
        file_type, patterns = detect_file_type(test_file)
        result = process_comments(content, file_type, patterns)

        # Check that comments are removed
        self.assertNotIn("<!-- This is an HTML comment -->", result)
        self.assertNotIn("<!-- This is another\n         multi-line comment -->", result)

        # Check that code is preserved
        self.assertIn("<!DOCTYPE html>", result)
        self.assertIn("<html>", result)
        self.assertIn("<head>", result)
        self.assertIn("<title>Test</title>", result)
        self.assertIn("</head>", result)
        self.assertIn("<body>", result)
        self.assertIn("<h1>Hello World</h1>", result)
        self.assertIn("</body>", result)
        self.assertIn("</html>", result)

    def test_sql_comments(self):
        """Test SQL comments"""
        content = """-- This is a SQL comment
SELECT * FROM users
WHERE id = 1; -- Get user with ID 1
/* This is a multi-line
   SQL comment */
UPDATE users SET name = 'John';"""
        # Create a temporary file to test the actual implementation
        test_file = os.path.join(self.test_dir, "test.sql")
        with open(test_file, 'w') as f:
            f.write(content)

        # Process the file using our implementation
        file_type, patterns = detect_file_type(test_file)
        result = process_comments(content, file_type, patterns)

        # Check that comments are removed
        self.assertNotIn("-- This is a SQL comment", result)
        self.assertNotIn("-- Get user with ID 1", result)
        self.assertNotIn("/* This is a multi-line\n   SQL comment */", result)

        # Check that code is preserved
        self.assertIn("SELECT * FROM users", result)
        self.assertIn("WHERE id = 1;", result)
        self.assertIn("UPDATE users SET name = 'John';", result)

    def test_file_type_detection(self):
        """Test file type detection based on extension"""
        # Create test files with different extensions
        extensions = {
            '.py': 'python',
            '.js': 'c_style',
            '.html': 'markup',
            '.css': 'css',
            '.sql': 'sql',
            '.sh': 'shell',
            '.rb': 'ruby',
            '.lua': 'lua',
            '.ps1': 'powershell',
            '.yml': 'yaml',
            '.hs': 'haskell',
            '.bat': 'batch'
        }

        for ext, expected_type in extensions.items():
            test_file = os.path.join(self.test_dir, f"test{ext}")
            with open(test_file, 'w') as f:
                f.write("Test content")

            detected_type, _ = detect_file_type(test_file)
            self.assertEqual(detected_type, expected_type, f"Failed to detect {expected_type} for extension {ext}")

    def test_url_in_comment(self):
        """Test that URLs in code are not mistaken for comments"""
        content = """// This is a comment
const url = "http://example.com"; // This is a trailing comment
const protocol = "https://"; // Protocol
const str = "This string contains // which is not a comment";
"""
        # Create a temporary file to test the actual implementation
        test_file = os.path.join(self.test_dir, "test.js")
        with open(test_file, 'w') as f:
            f.write(content)

        # Process the file using our implementation
        file_type, patterns = detect_file_type(test_file)
        result = process_comments(content, file_type, patterns)

        # Check that comments are removed
        self.assertNotIn("// This is a comment", result)
        self.assertNotIn("// This is a trailing comment", result)
        self.assertNotIn("// Protocol", result)

        # Check that code and URLs are preserved
        self.assertIn('const url = "http://example.com";', result)
        self.assertIn('const protocol = "https://";', result)
        self.assertIn('const str = "This string contains // which is not a comment";', result)


if __name__ == '__main__':
    unittest.main()
