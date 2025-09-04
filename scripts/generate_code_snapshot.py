#!/usr/bin/env python3
"""
Code Snapshot Generator for Symposium Knowledge Base (v1.1)
Walks through the entire project directory and generates a markdown-formatted code dump.
"""

import os
import sys
from pathlib import Path

def generate_code_snapshot():
    """Generate a complete code snapshot in markdown format."""
    
    project_root = Path.cwd()
    output_file = project_root / "docs" / "codesnapshot.md"
    
    # Define what to include
    include_patterns = ["*.py", "*.bat", "*.txt", "*.md", ".gitignore"]
    
    # Define what to exclude
    exclude_dirs = ["symposium_env", "__pycache__", ".git", "docs/Obsolete", "docs/PastUpdates"]
    
    print("  -> Starting code snapshot generation...")
    
    all_files = []
    for pattern in include_patterns:
        all_files.extend(project_root.rglob(pattern))
    print(f"  -> Found {len(all_files)} files matching patterns.")
        
    # Filter out files in excluded directories
    final_files = []
    for file_path in all_files:
        is_excluded = False
        # Create a comparable parts tuple for the file path
        file_parts = file_path.relative_to(project_root).parts
        for excluded_dir in exclude_dirs:
            # Create a comparable parts tuple for the excluded dir
            excluded_parts = Path(excluded_dir).parts
            # Check if the excluded path is a prefix of the file path
            if file_parts[:len(excluded_parts)] == excluded_parts:
                is_excluded = True
                break
        if not is_excluded:
            final_files.append(file_path)

    print(f"  -> Filtering excluded directories... {len(final_files)} files remain.")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Complete Module Code\n\n")
        
        for file in sorted(final_files):
            rel_path = file.relative_to(project_root).as_posix()
            f.write(f"**File: {rel_path}**\n\n")
            
            try:
                with open(file, 'r', encoding='utf-8', errors='ignore') as source:
                    content = source.read()
                    lang = ""
                    if file.suffix == '.py':
                        lang = "python"
                    elif file.suffix == '.bat':
                        lang = "batch"
                    
                    f.write(f"```{lang}\n")
                    f.write(content)
                    f.write("\n```\n\n")
            except Exception as e:
                f.write(f"*Error reading file: {e}*\n\n")

    print(f"  -> Writing {len(final_files)} files to '{output_file.name}'...")
    print("  -> Snapshot generation complete.")

if __name__ == "__main__":
    generate_code_snapshot()