#!/usr/bin/env python3
"""Add Jekyll front matter to all documentation markdown files."""

import os
import re

def add_front_matter(file_path):
    """Add Jekyll front matter to a markdown file if it doesn't have it."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if file already has front matter
    if content.startswith('---\n'):
        print(f"Skipping {file_path} - already has front matter")
        return
    
    # Extract title from first H1 heading or filename
    title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
    if title_match:
        title = title_match.group(1)
    else:
        # Use filename as title
        title = os.path.splitext(os.path.basename(file_path))[0]
        title = title.replace('-', ' ').replace('_', ' ').title()
    
    # Add front matter
    front_matter = f"""---
layout: default
title: "{title}"
---

"""
    
    # Write back with front matter
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(front_matter + content)
    
    print(f"Added front matter to {file_path}")

def process_docs_directory(docs_dir):
    """Process all markdown files in the docs directory."""
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                add_front_matter(file_path)

if __name__ == "__main__":
    docs_dir = "docs"
    if os.path.exists(docs_dir):
        process_docs_directory(docs_dir)
        print("Front matter addition complete!")
    else:
        print(f"Error: {docs_dir} directory not found")