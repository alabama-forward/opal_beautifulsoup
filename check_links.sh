#!/bin/bash
# check_links.sh - Script to validate documentation links

echo "======================================"
echo "OPAL Documentation Link Checker"
echo "======================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
total_files=0
total_links=0
broken_links=0
warnings=0

# Base directory
DOCS_DIR="docs"

# Check if docs directory exists
if [ ! -d "$DOCS_DIR" ]; then
    echo -e "${RED}Error: Documentation directory '$DOCS_DIR' not found!${NC}"
    exit 1
fi

# Function to resolve relative paths
resolve_path() {
    local base_dir="$1"
    local link="$2"
    
    # Remove anchor from link
    link="${link%%#*}"
    
    # Remove query parameters
    link="${link%%\?*}"
    
    # Skip external links
    if [[ "$link" =~ ^https?:// ]]; then
        echo "external"
        return
    fi
    
    # Skip mailto links
    if [[ "$link" =~ ^mailto: ]]; then
        echo "external"
        return
    fi
    
    # Handle absolute paths (starting with /)
    if [[ "$link" =~ ^/ ]]; then
        echo "$DOCS_DIR${link%.md}.md"
        return
    fi
    
    # Handle relative paths
    local resolved="$base_dir/$link"
    
    # Normalize the path (remove ../ and ./)
    resolved=$(realpath -m "$resolved" 2>/dev/null || echo "$resolved")
    
    # If link doesn't end with .md, assume it's a directory and add index.md
    if [[ ! "$resolved" =~ \.md$ ]]; then
        if [[ "$resolved" =~ /$ ]]; then
            resolved="${resolved}index.md"
        else
            resolved="${resolved}/index.md"
        fi
    fi
    
    echo "$resolved"
}

echo "Checking all markdown files in $DOCS_DIR..."
echo ""

# Find all markdown files
while IFS= read -r file; do
    total_files=$((total_files + 1))
    echo -e "${YELLOW}Checking:${NC} $file"
    
    # Get directory of current file
    file_dir=$(dirname "$file")
    
    # Extract all markdown links from the file
    # Matches [text](link) pattern
    grep -oE '\[[^]]+\]\([^)]+\)' "$file" 2>/dev/null | while IFS= read -r match; do
        # Extract just the URL part
        url=$(echo "$match" | sed -E 's/\[[^]]*\]\(([^)]+)\)/\1/')
        
        # Skip empty URLs
        if [ -z "$url" ]; then
            continue
        fi
        
        total_links=$((total_links + 1))
        
        # Resolve the path
        resolved=$(resolve_path "$file_dir" "$url")
        
        # Check if it's an external link
        if [ "$resolved" = "external" ]; then
            echo -e "  ${GREEN}✓${NC} External link: $url"
            continue
        fi
        
        # Check if file exists
        if [ -f "$resolved" ]; then
            echo -e "  ${GREEN}✓${NC} Valid link: $url → $resolved"
        else
            echo -e "  ${RED}✗${NC} Broken link: $url → $resolved"
            broken_links=$((broken_links + 1))
            
            # Try to find similar files
            base_name=$(basename "$resolved" .md)
            dir_name=$(dirname "$resolved")
            echo -e "    ${YELLOW}Suggestions:${NC}"
            find "$dir_name" -name "*$base_name*" -type f 2>/dev/null | head -3 | while read -r suggestion; do
                echo "      - $suggestion"
            done
        fi
    done
    
    echo ""
done < <(find "$DOCS_DIR" -name "*.md" -type f | sort)

# Check for orphaned files (files not linked from anywhere)
echo "======================================"
echo "Checking for orphaned files..."
echo ""

# Create temporary file to store all linked files
temp_file=$(mktemp)

# Find all linked files
while IFS= read -r file; do
    grep -oE '\[[^]]+\]\([^)]+\)' "$file" 2>/dev/null | while IFS= read -r match; do
        url=$(echo "$match" | sed -E 's/\[[^]]*\]\(([^)]+)\)/\1/')
        file_dir=$(dirname "$file")
        resolved=$(resolve_path "$file_dir" "$url")
        
        if [ "$resolved" != "external" ] && [ -f "$resolved" ]; then
            echo "$resolved" >> "$temp_file"
        fi
    done
done < <(find "$DOCS_DIR" -name "*.md" -type f)

# Find orphaned files
find "$DOCS_DIR" -name "*.md" -type f | while read -r file; do
    # Skip index.md files as they might be navigation entry points
    if [[ "$file" =~ index\.md$ ]]; then
        continue
    fi
    
    if ! grep -q "^$file$" "$temp_file"; then
        echo -e "${YELLOW}⚠${NC}  Orphaned file (not linked from anywhere): $file"
        warnings=$((warnings + 1))
    fi
done

rm -f "$temp_file"

# Summary
echo ""
echo "======================================"
echo "Summary"
echo "======================================"
echo "Total files checked: $total_files"
echo "Total links found: $total_links"
if [ $broken_links -eq 0 ]; then
    echo -e "${GREEN}Broken links: $broken_links${NC}"
else
    echo -e "${RED}Broken links: $broken_links${NC}"
fi
if [ $warnings -eq 0 ]; then
    echo -e "${GREEN}Warnings: $warnings${NC}"
else
    echo -e "${YELLOW}Warnings: $warnings${NC}"
fi

# Exit with error if broken links found
if [ $broken_links -gt 0 ]; then
    exit 1
else
    exit 0
fi