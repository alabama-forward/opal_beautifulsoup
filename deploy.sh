#!/bin/bash
# Deploy script for GitHub Pages

# Build the documentation
echo "Building documentation..."
mkdocs build --clean

# Create a temporary directory
temp_dir=$(mktemp -d)

# Copy only the site contents
cp -r site/* "$temp_dir/"

# Switch to gh-pages branch
git checkout gh-pages || git checkout -b gh-pages

# Remove all existing files
git rm -rf .

# Copy the built site
cp -r "$temp_dir"/* .

# Add .nojekyll file
touch .nojekyll

# Commit and push
git add .
git commit -m "Deploy documentation"
git push origin gh-pages

# Switch back to main branch
git checkout main

# Clean up
rm -rf "$temp_dir"

echo "Deployment complete!"