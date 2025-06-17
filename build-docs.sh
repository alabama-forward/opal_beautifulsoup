#!/bin/bash
# Build documentation for GitHub Pages deployment

echo "Building OPAL documentation..."

# Clean and build
mkdocs build --clean

# Ensure .nojekyll exists in docs
touch docs/.nojekyll

echo "Documentation built successfully!"
echo "The 'docs' folder is ready for GitHub Pages deployment."
echo ""
echo "To deploy:"
echo "1. Commit the changes in the 'docs' folder"
echo "2. Push to GitHub"
echo "3. GitHub Pages will automatically update from main/docs"