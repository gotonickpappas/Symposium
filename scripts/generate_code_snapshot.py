#!/usr/bin/env python3
"""
Code Snapshot Generator for Symposium Knowledge Base
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
    
    print("Starting code snapshot generation...")
    
    all_files = []
    for pattern in include_patterns:
        # rglob scans recursively
        all_files.extend(project_root.rglob(pattern))
        
    # Filter out files in excluded directories
    final_files = []
    for file_path in all_files:
        is_excluded = False
        for excluded_dir in exclude_dirs:
            if project_root.joinpath(excluded_dir) in file_path.parents:
                is_excluded = True
                break
        if not is_excluded:
            final_files.append(file_path)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Complete Module Code\n\n")
        
        for file in sorted(final_files):
            rel_path = file.relative_to(project_root).as_posix()
            f.write(f"**File: {rel_path}**\n\n")
            
            try:
                with open(file, 'r', encoding='utf-8', errors='ignore') as source:
                    content = source.read()
                    # Determine language for markdown block
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

    print(f"✓ Code snapshot generated: {output_file}")
    print(f"  Processed {len(final_files)} files.")

if __name__ == "__main__":
    generate_code_snapshot()