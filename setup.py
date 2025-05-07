"""
Setup script for the comment_remover package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="comment-remover",
    version="1.0.0",
    author="Shubham Sharma",
    author_email="shubhamsharma.emails@gmail.com",
    description="A tool to remove comments from code files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sharma-IT/comment-remover",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "comment-remover=comment_remover.cli:main",
        ],
    },
)
