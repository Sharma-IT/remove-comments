"""
Command-line interface for the comment remover.

This module provides the command-line interface for the comment remover tool.
"""

import argparse
import os
import time
from pathlib import Path

from .core import process_comments, detect_file_type, COMMENT_PATTERNS


def main():
    """
    Main entry point for the command-line interface.
    
    Returns:
        int: Exit code (0 for success, non-zero for failure).
    """
    parser = argparse.ArgumentParser(
        description='Process comments in any file: remove multi-line comments, '
                    'strip trailing single-line comments, replace full-line single comments with blank lines.'
    )
    parser.add_argument('input_file', nargs='?', help='Path to the input file.')
    parser.add_argument('-o', '--output', help='Path to the output file. If not provided, prints to console.')
    parser.add_argument('-i', '--in-place', action='store_true', 
                        help='Modify the input file directly (use with caution!).')
    parser.add_argument('-t', '--type', 
                        help='Force a specific file type (e.g., python, c_style, css, etc.). '
                             'By default, auto-detects based on file extension.')
    parser.add_argument('-l', '--list-types', action='store_true', 
                        help='List all supported file types and exit.')
    parser.add_argument('-v', '--verbose', action='store_true', 
                        help='Print verbose information about the file type detection.')

    args = parser.parse_args()

    # Handle listing supported file types
    if args.list_types:
        print("Supported file types:")
        for file_type, patterns in COMMENT_PATTERNS.items():
            extensions = ', '.join(patterns['extensions'])
            single_line = patterns['single_line'] if patterns['single_line'] else 'None'
            multi_line = f"{patterns['multi_line'][0]} ... {patterns['multi_line'][1]}" if patterns['multi_line'] else 'None'
            print(f"  {file_type}:")
            print(f"    Extensions: {extensions}")
            print(f"    Single-line comment: {single_line}")
            print(f"    Multi-line comment: {multi_line}")
            print()
        return 0

    # Check if input file is provided
    if not args.input_file:
        parser.print_help()
        print("\nError: Input file is required unless using --list-types")
        return 1

    input_path = args.input_file
    output_path = args.output
    in_place = args.in_place
    forced_type = args.type
    verbose = args.verbose

    if not os.path.exists(input_path):
        print(f"Error: Input file not found: {input_path}")
        return 1

    if in_place and output_path:
        print("Error: Cannot use --in-place (-i) and --output (-o) together.")
        return 1

    try:
        # Detect file type
        if forced_type and forced_type in COMMENT_PATTERNS:
            file_type = forced_type
            patterns = COMMENT_PATTERNS[forced_type]
            if verbose:
                print(f"Using forced file type: {file_type}")
        else:
            file_type, patterns = detect_file_type(input_path)
            if verbose:
                if forced_type and forced_type not in COMMENT_PATTERNS:
                    print(f"Warning: Forced file type '{forced_type}' not recognized. Auto-detecting instead.")
                print(f"Detected file type: {file_type}")
                print(f"Single-line comment: {patterns['single_line'] if patterns['single_line'] else 'None'}")
                print(f"Multi-line comment: {patterns['multi_line'] if patterns['multi_line'] else 'None'}")

        with open(input_path, 'r', encoding='utf-8') as f_in:
            original_content = f_in.read()

        # Process the content with the detected or forced file type
        cleaned_content = process_comments(original_content, file_type, patterns)

        if in_place:
            # Create a unique backup just in case
            base, ext = os.path.splitext(input_path)
            backup_path = f"{base}.{int(time.time())}.bak"
            # Fallback if needed
            default_backup_path = input_path + '.bak'

            chosen_backup_path = backup_path
            if os.path.exists(chosen_backup_path):
                 chosen_backup_path = default_backup_path # Use default if timestamped exists somehow

            try:
                 # Ensure backup doesn't overwrite another backup easily
                if os.path.exists(chosen_backup_path):
                    print(f"Warning: Backup file {chosen_backup_path} already exists. Overwriting.")
                    # os.remove(chosen_backup_path) # Uncomment to force overwrite

                os.rename(input_path, chosen_backup_path)
                print(f"Original file backed up to: {chosen_backup_path}")

                with open(input_path, 'w', encoding='utf-8') as f_out:
                    f_out.write(cleaned_content)
                print(f"Comments processed in-place: {input_path}")

            except Exception as e:
                print(f"Error during in-place modification: {e}")
                # Attempt to restore backup if writing failed
                if os.path.exists(chosen_backup_path) and not os.path.exists(input_path):
                    os.rename(chosen_backup_path, input_path)
                    print("Original file restored from backup.")
                elif not os.path.exists(chosen_backup_path) and os.path.exists(default_backup_path) and not os.path.exists(input_path):
                    # Try restoring default backup name if timestamped failed
                    os.rename(default_backup_path, input_path)
                    print("Original file restored from backup.")
                return 1

        elif output_path:
            with open(output_path, 'w', encoding='utf-8') as f_out:
                f_out.write(cleaned_content)
            print(f"Processed file written to: {output_path}")
        else:
            # Print to console if no output or in-place flag specified
            print(f"\n--- Processed {file_type.upper()} file ---")
            print(cleaned_content.strip()) # Strip trailing newline for cleaner console output
            print("----------------------\n")

        return 0

    except FileNotFoundError:
        print(f"Error: Input file not found: {input_path}")
        return 1
    except IOError as e:
        print(f"Error reading or writing file: {e}")
        return 1
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
