# Documentation Update Instructions for OPAL Project

## Overview
This document provides comprehensive instructions for updating the OPAL (Oppositional Positions in Alabama) documentation based on the Apps Script documentation structure found in the `other-examples` folder.

## Key Learnings from Apps Script Documentation

### 1. Documentation Organization
The Apps Script documentation demonstrates excellent organization with:
- **Clear audience separation**: Separate sections for end users and developers
- **Progressive disclosure**: Start with concepts, then move to implementation
- **Practical examples**: Every concept includes working code examples
- **Troubleshooting integration**: Common issues addressed within relevant sections

### 2. Structure Patterns to Adopt

#### a. Navigation Hierarchy
```
- Home (Overview and quick links)
- Getting Started (Installation → Configuration → First Steps)
- User Guide (Task-oriented documentation)
- Developer Guide (Technical deep-dives)
- Reference (API documentation)
- Troubleshooting (Common issues and solutions)
```

#### b. Content Templates
Each technical page should include:
1. **Purpose statement** (what this does)
2. **Prerequisites** (what you need to know/have)
3. **Core concepts** (key ideas to understand)
4. **Step-by-step implementation**
5. **Code examples** (complete, runnable examples)
6. **Common patterns** (best practices)
7. **Troubleshooting** (inline with content)
8. **Next steps** (where to go next)

## Specific Updates for OPAL Documentation

### 1. Homepage Enhancement (index.md)
**Current**: Basic introduction
**Update to include**:
- Clear value proposition for OPAL
- Quick links to common tasks
- Brief overview of available parsers
- Prerequisites checklist
- "Choose your path" section (User vs Developer)

### 2. Getting Started Restructure
**Create a unified flow**:
1. `prerequisites.md` - System requirements, Python version, dependencies
2. `installation.md` - Step-by-step installation with troubleshooting
3. `first-scrape.md` - Minimal working example
4. `understanding-output.md` - What the data means

### 3. User Guide Enhancements

#### a. Task-Oriented Structure
Reorganize current content into task-based sections:
- "How to scrape Alabama Appeals Court"
- "How to extract cases from a specific date range"
- "How to handle pagination"
- "How to export to different formats"

#### b. Visual Learning
Add for each parser:
- Flow diagrams showing the scraping process
- Annotated output examples
- Common error scenarios with screenshots

### 4. Developer Guide Improvements

#### a. Architecture Deep Dive
Expand `architecture.md` to include:
- Class hierarchy diagram
- Data flow visualization
- Extension points for custom parsers
- Performance considerations

#### b. Parser Development Guide
Create comprehensive guide following Apps Script pattern:
```markdown
# Creating Custom Parsers

## Understanding the Parser Architecture
[Conceptual overview with diagrams]

## Your First Custom Parser
[Step-by-step tutorial]

## Parser Patterns
### Pattern 1: Simple HTML Parser
[Complete example]

### Pattern 2: JavaScript-Rendered Content
[Complete example]

### Pattern 3: Multi-Page Navigation
[Complete example]

## Testing Your Parser
[Testing strategies and examples]

## Common Pitfalls
[What to avoid and why]
```

### 5. Reference Documentation Enhancement

#### a. Standardize Class Documentation
For each parser class, include:
- **Purpose**: One-line description
- **Usage Example**: Minimal working code
- **Parameters**: Table with name, type, description, default
- **Methods**: Public API with examples
- **Attributes**: Available data fields
- **Exceptions**: What can go wrong
- **See Also**: Related classes/methods

#### b. Add Code Snippets Library
Create `snippets.md` with copy-paste ready examples:
- Basic scraping
- Date filtering
- Custom headers
- Error handling
- Output formatting

### 6. New Sections to Add

#### a. Cookbook Section
Create `cookbook/` directory with recipes:
- `bulk-scraping.md` - Scraping multiple courts
- `scheduling.md` - Automated scraping setup
- `data-pipeline.md` - Integrating with data processing
- `monitoring.md` - Setting up alerts for failures

#### b. Deployment Guide
Create `deployment/` section:
- `docker-setup.md` - Containerized deployment
- `cloud-deployment.md` - AWS/GCP/Azure setup
- `ci-cd.md` - Automated testing and deployment

### 7. Interactive Elements

#### a. Command Builder Enhancement
Improve the existing command builder to:
- Show live preview of command
- Explain each parameter
- Provide copy button
- Include common presets

#### b. Configuration Generator
Create tool that generates:
- Configuration files
- Custom parser templates
- Error handling setup

## Page Structure and Link Management

### Directory Structure Standards

#### 1. File Organization
```
docs/
├── index.md                    # Home page
├── getting-started/
│   ├── index.md               # Section overview
│   ├── prerequisites.md       # System requirements
│   ├── installation.md        # Installation guide
│   ├── configuration.md       # Configuration options
│   └── first-scrape.md        # Tutorial
├── user-guide/
│   ├── index.md               # User guide overview
│   ├── cli-reference.md       # CLI documentation
│   ├── parsers/               # Parser-specific guides
│   │   ├── index.md          # Parser overview
│   │   ├── appeals-al.md     # Alabama Appeals parser
│   │   ├── parser-1819.md    # 1819 News parser
│   │   └── daily-news.md     # Daily News parser
│   └── troubleshooting.md     # Common issues
├── developer/
│   ├── index.md               # Developer overview
│   ├── architecture.md        # System architecture
│   ├── creating-parsers.md    # Parser development
│   └── reference/                   # class reference
│       ├── index.md          # class overview
│       ├── base-parser.md    # BaseParser class
│       └── extractors.md     # Extractor classes
└── about/
    ├── contributing.md        # Contribution guide
    └── license.md            # License information
```

#### 2. Naming Conventions
- **Files**: Use lowercase with hyphens (e.g., `getting-started.md`)
- **Directories**: Use lowercase with hyphens
- **Index files**: Every directory should have an `index.md`
- **Consistency**: Match file names to navigation titles

### Link Management Strategy

#### 1. Internal Link Types

##### Relative Links (Preferred)
```markdown
<!-- From getting-started/installation.md -->
[Prerequisites](./prerequisites.md)
[Back to Getting Started](./)
[CLI Reference](../user-guide/cli-reference.md)
```

##### Absolute Links (When Necessary)
```markdown
<!-- For cross-section references -->
[See Architecture Guide](/developer/architecture/)
[View All Parsers](/user-guide/parsers/)
```

#### 2. Link Validation Rules

##### Always Include:
- File extensions (`.md`) in source files
- Trailing slashes for directories when linking to index
- Proper relative paths based on current location

##### Example Link Patterns:
```markdown
<!-- Same directory -->
[Configuration](./configuration.md)

<!-- Parent directory -->
[Back to User Guide](../)

<!-- Child directory -->
[Parser Documentation](./parsers/)

<!-- Cross-section -->
[Developer Guide](../developer/)

<!-- Specific file in another section -->
[BaseParser API](../developer/api/base-parser.md)
```

#### 3. Navigation Configuration

##### mkdocs.yml Structure:
```yaml
nav:
  - Home: index.md
  - Getting Started:
    - Overview: getting-started/index.md
    - Prerequisites: getting-started/prerequisites.md
    - Installation: getting-started/installation.md
    - Configuration: getting-started/configuration.md
    - First Scrape: getting-started/first-scrape.md
  - User Guide:
    - Overview: user-guide/index.md
    - CLI Reference: user-guide/cli-reference.md
    - Parsers:
      - Available Parsers: user-guide/parsers/index.md
      - Alabama Appeals: user-guide/parsers/appeals-al.md
      - 1819 News: user-guide/parsers/parser-1819.md
      - Daily News: user-guide/parsers/daily-news.md
    - Troubleshooting: user-guide/troubleshooting.md
  - Developer Guide:
    - Overview: developer/index.md
    - Architecture: developer/architecture.md
    - Creating Parsers: developer/creating-parsers.md
    - API Reference:
      - Overview: developer/api/index.md
      - BaseParser: developer/api/base-parser.md
      - Extractors: developer/api/extractors.md
```

### Cross-Reference System

#### 1. Consistent Anchor Links
```markdown
<!-- In architecture.md -->
## Parser Architecture {#parser-arch}

<!-- In another file -->
See the [Parser Architecture](../developer/architecture.md#parser-arch) section
```

#### 2. Reference Tables
Create a reference table in each section's index.md:
```markdown
| Page | Description | Link |
|------|-------------|------|
| Prerequisites | System requirements and setup | [View](./prerequisites.md) |
| Installation | Step-by-step installation | [View](./installation.md) |
| Configuration | Config options and examples | [View](./configuration.md) |
```

#### 3. Breadcrumb Navigation
Add breadcrumbs at the top of each page:
```markdown
[Home](/) > [Getting Started](/getting-started/) > Installation

# Installation Guide
```

### Link Testing Strategy

#### 1. Automated Testing
```bash
# Create a link checker script
#!/bin/bash
# check_links.sh

echo "Checking documentation links..."

# Find all markdown files
find docs -name "*.md" -type f | while read file; do
    echo "Checking: $file"
    
    # Extract all markdown links
    grep -oE '\[([^\]]+)\]\(([^\)]+)\)' "$file" | while read link; do
        url=$(echo "$link" | sed -E 's/\[[^\]]+\]\(([^\)]+)\)/\1/')
        
        # Check if internal link
        if [[ $url == /* ]] || [[ $url == ./* ]] || [[ $url == ../* ]]; then
            # Resolve the path
            resolved=$(realpath "$(dirname "$file")/$url" 2>/dev/null)
            
            # Check if file exists
            if [[ ! -f "$resolved" ]]; then
                echo "  ❌ Broken link: $url"
            fi
        fi
    done
done
```

#### 2. Manual Testing Checklist
- [ ] All navigation menu items load correct pages
- [ ] Section overview pages link to all subsections
- [ ] Cross-references between sections work
- [ ] Anchor links jump to correct headings
- [ ] External links open in new tabs
- [ ] No 404 errors in production build

### Page Template Structure

#### 1. Standard Page Template
```markdown
---
title: Page Title
description: Brief description for SEO
---

[Home](/) > [Section](/section/) > Current Page

# Page Title

!!! abstract "Overview"
    Brief introduction to what this page covers.

## Prerequisites

What users need before using this guide:
- Requirement 1
- Requirement 2

## Main Content

### Subsection 1

Content here...

### Subsection 2

Content here...

## Related Topics

- [Related Page 1](./related-1.md)
- [Related Page 2](../other-section/page.md)

## Next Steps

- [Continue to Next Topic](./next-topic.md)
- [Back to Section Overview](./)
```

#### 2. Section Index Template
```markdown
---
title: Section Name
description: Overview of this section
---

# Section Name

## In This Section

### [Topic 1](./topic-1.md)
Brief description of topic 1.

### [Topic 2](./topic-2.md)
Brief description of topic 2.

### [Topic 3](./topic-3.md)
Brief description of topic 3.

## Quick Links

- **Most Popular**: [Common Use Cases](./common-use-cases.md)
- **Getting Help**: [Troubleshooting](./troubleshooting.md)
- **Reference**: [API Documentation](./api/)
```

## Implementation Steps

### Phase 1: Structure and Link Foundation (Week 1)
1. Create complete directory structure
2. Add index.md files to all directories
3. Set up navigation in `mkdocs.yml`
4. Create link validation script
5. Test all navigation paths
6. Fix any broken links

### Phase 2: Content Migration (Week 2)
1. Move existing content to new structure
2. Update all internal links to new paths
3. Add breadcrumb navigation
4. Create section overview pages
5. Implement cross-reference system

### Phase 3: Content Enhancement (Week 3)
1. Apply page templates to all content
2. Add "Related Topics" sections
3. Create "Next Steps" navigation
4. Enhance with visual diagrams
5. Add code snippet library

### Phase 4: Developer Documentation (Week 4)
1. Expand architecture documentation
2. Create comprehensive parser guide
3. Add cookbook recipes
4. Build API reference with proper linking
5. Implement interactive tools

### Phase 5: Testing and Polish (Week 5)
1. Run automated link checker
2. Manual test all navigation paths
3. Verify anchor links work
4. Test on mobile devices
5. Add search optimization
6. Create feedback mechanism

## Documentation Standards

### Code Examples
- Every example must be complete and runnable
- Include imports and setup
- Show expected output
- Handle common errors

### Writing Style
- Active voice
- Present tense
- Short paragraphs
- Lots of headings for scanning

### Visual Standards
- Mermaid diagrams for flows
- Screenshots with annotations
- Consistent color scheme
- Responsive design

## Metrics for Success
- Time to first successful scrape < 5 minutes
- All code examples run without modification
- Clear navigation path for any task
- Positive user feedback on clarity

## Branding and Styling Guidelines

### Brand Identity
Based on the Apps Script documentation and OPAL's existing brand, implement consistent branding:

#### Color Palette
```css
/* Primary OPAL Colors */
--opal-primary: #B53D1A;        /* Reddish-orange - main brand color */
--opal-secondary: #363D4A;      /* Dark gray - professional accent */
--opal-accent: #ff5722;         /* Bright orange - highlights */
--opal-background: #EBE5D6;     /* Light beige - warm background */

/* Alabama Theme Colors */
--alabama-crimson: #a6192e;     /* University of Alabama crimson */
--alabama-gray: #828a8f;        /* Neutral gray */
--alabama-gold: #ffb71b;        /* Accent gold */
```

#### Typography
- **Primary Font**: Inter (from Google Fonts) for modern, clean readability
- **Monospace Font**: Monaco, Consolas, 'Courier New' for code
- **Font Weights**: 400 (regular), 500 (medium), 600 (semibold), 700 (bold)
- **Line Height**: 1.6-1.7 for optimal readability

### Visual Design Patterns

#### 1. Navigation Design
- **Fixed sidebar** (270px wide) with smooth scrolling
- **Hierarchical structure** with clear visual levels
- **Active state indicators** with primary color
- **Hover effects** with smooth transitions

#### 2. Content Styling
```css
/* Headers with visual hierarchy */
h1: 32px, border-bottom with primary color
h2: 24px, 40px top margin for section separation  
h3: 20px, 30px top margin for subsections

/* Code blocks with enhanced styling */
- Light background (#f5f5f5)
- Rounded corners (5px radius)
- Subtle border
- Horizontal scrolling for long lines
```

#### 3. Interactive Elements

##### Callout Boxes
Create styled callout boxes for different content types:
```css
.note {
  background-color: #e3f2fd;
  border-left: 4px solid #2196f3;
}

.warning {
  background-color: #fff3cd;
  border-left: 4px solid #ffc107;
}

.tip {
  background-color: #d4edda;
  border-left: 4px solid #28a745;
}

.court-section {
  border: 2px solid var(--alabama-crimson);
  background: linear-gradient(145deg, rgba(166, 25, 46, 0.05) 0%, rgba(255, 183, 27, 0.05) 100%);
}
```

##### Badges and Labels
```css
.cli-badge {
  background-color: var(--opal-primary);
  color: white;
  padding: 0.2rem 0.6rem;
  border-radius: 12px;
}

.parser-badge {
  background-color: var(--opal-secondary);
}

.option-badge {
  background-color: var(--opal-accent);
}
```

### Layout Patterns

#### 1. Page Structure
```html
<div class="wrapper">
  <header>
    <!-- Fixed sidebar navigation -->
    <h1>OPAL Documentation</h1>
    <nav><!-- Navigation items --></nav>
  </header>
  
  <section>
    <!-- Main content area (640px wide) -->
    <!-- Floating right of sidebar -->
  </section>
</div>
```

#### 2. Responsive Design
- **Desktop**: Fixed sidebar, 960px max width
- **Tablet** (720px): Collapsible sidebar
- **Mobile** (480px): Stacked layout, optimized padding

### Content Formatting Standards

#### 1. Code Examples
- **Syntax highlighting** with language-specific colors
- **Line numbers** for longer examples
- **Copy button** for easy code reuse
- **Filename headers** when showing file contents

#### 2. Tables
- **Striped rows** for readability
- **Hover states** for interactivity
- **Responsive scrolling** on mobile
- **Styled headers** with primary color background

#### 3. Documentation Components

##### Quick Start Boxes
```html
<div class="highlight-section">
  <h3>Quick Start</h3>
  <p>Get started in under 5 minutes</p>
  <a href="/quickstart" class="md-button md-button--primary">
    Start Tutorial
  </a>
</div>
```

##### Feature Cards
```html
<div class="feature-grid">
  <div class="feature-card">
    <h4>Alabama Appeals Court</h4>
    <p>Scrape appellate court decisions</p>
    <code>opal parse appeals-al</code>
  </div>
</div>
```

### Implementation Checklist

#### Phase 1: Style Foundation
- [ ] Import Inter font from Google Fonts
- [ ] Set up CSS variables for theming
- [ ] Configure Material theme colors
- [ ] Implement responsive breakpoints

#### Phase 2: Component Styling
- [ ] Style navigation with hover states
- [ ] Create callout box components
- [ ] Design badge system for CLI commands
- [ ] Implement code block enhancements

#### Phase 3: Content Templates
- [ ] Create page layout templates
- [ ] Design quick start sections
- [ ] Build feature comparison tables
- [ ] Implement interactive command builders

#### Phase 4: Brand Integration
- [ ] Add OPAL logo to header
- [ ] Create Alabama-themed sections
- [ ] Design parser-specific styling
- [ ] Implement print styles

### Accessibility Standards
- **Color contrast**: Minimum 4.5:1 for normal text
- **Focus indicators**: 2px solid outline on interactive elements
- **Keyboard navigation**: Full site navigable via keyboard
- **Screen reader support**: Proper ARIA labels and semantic HTML

### Performance Optimization
- **Font loading**: Use font-display: swap
- **CSS minification**: Compress production styles
- **Image optimization**: Use WebP format where supported
- **Lazy loading**: Implement for images and heavy content

## Tools and Resources
- MkDocs Material theme features
- Mermaid for diagrams
- Prism for syntax highlighting
- GitHub Actions for testing examples
- Google Fonts for typography
- CSS custom properties for theming

## Maintenance Plan
- Quarterly review of all examples
- Monthly check of external links
- User feedback integration process
- Version-specific documentation branches
- Regular accessibility audits
- Performance monitoring