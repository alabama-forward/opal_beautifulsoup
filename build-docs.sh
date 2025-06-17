#!/bin/bash
# Build documentation for GitHub Pages deployment

echo "Building OPAL documentation..."

# Clean and build
mkdocs build --clean

# Ensure .nojekyll exists in docs
touch docs/.nojekyll

# Copy extra CSS if it exists
if [ -f "docs_source/stylesheets/extra.css" ]; then
    mkdir -p docs/stylesheets
    cp docs_source/stylesheets/extra.css docs/stylesheets/
fi

echo "Documentation built successfully!"
echo "The 'docs' folder is ready for GitHub Pages deployment."
echo ""
echo "To deploy:"
echo "1. Commit the changes in the 'docs' folder"
echo "2. Push to GitHub"
echo "3. GitHub Pages will automatically update from main/docs"