# Documentation Consolidation Plan for OPAL

## Overview

This document outlines recommendations for consolidating the OPAL documentation to make it easier for users to navigate. The current documentation has 35+ files with significant redundancy and confusing navigation paths. This plan proposes reducing to ~25 files with clearer organization. OPAL is a command-line tool for web scraping, not an API service.

## Key Issues Identified

1. **Redundant Content**: Multiple files covering the same topics
2. **Redirect Files**: Files that only redirect to other files
3. **Scattered Information**: Related content split across multiple sections
4. **Overly Granular Files**: Small files that could be combined

## High Priority Consolidations

### 1. CLI Documentation (3 files → 1 file)

**Current State:**
- `/user-guide/cli-usage.md` (37 lines)
- `/user-guide/command_line_tools.md` (44 lines)
- `/user-guide/command-builder.md` (separate interactive guide)

**Recommendation:**
- Merge `cli-usage.md` and `command_line_tools.md` into a single `cli-reference.md`
- Keep `command-builder.md` separate as it's an interactive tool guide
- Eliminate redundant examples and create one comprehensive CLI reference

### 2. Remove Redirect-Only Files

**Files to Delete:**
- `quickstart.md` - Just redirects to `quickstart-tutorial.md`
- `installation.md` - Just redirects to `complete-setup-guide.md`
- `output-formats.md` - Just redirects to `output-examples.md`

**Impact:** Saves users 3 unnecessary clicks and reduces confusion

### 3. Consolidate Setup Documentation

**Current State:**
- Installation information scattered across multiple files
- Users must follow redirects to find complete information

**Recommendation:**
- Merge all installation content directly into `complete-setup-guide.md`
- Create a single, comprehensive setup resource

## Medium Priority Consolidations

### 1. Parser Documentation

**ParserAppealsAL Documentation:**
- `/reference/parser-appeals-al.md` (227 lines) - Class reference
- `/developer/ParserAppealsAL_documentation.md` (338 lines) - Developer guide
- Additional commented-out files in navigation

**Recommendation:**
- Expand the class reference with implementation details
- Remove redundant developer documentation
- Archive commented-out files

**Parser Creation Guides:**
- `/developer/creating-parsers.md` (210 lines)
- `/developer/BaseParser_web_scraping_guide.md` (395 lines)

**Recommendation:**
- Merge into single comprehensive "Creating Custom Parsers" guide

### 2. Court Extractor Documentation

**Current State:**
- `/user-guide/configurable_court_extractor.md` (401 lines) - User guide
- `/developer/configurable_court_extractor_design.md` (1055 lines) - Contains full implementation

**Recommendation:**
- Create new `/reference/court-extractor-classes.md` for implementation code
- Keep design document focused on architecture decisions only
- Maintain clear separation between user guide and technical reference

## Proposed New Structure

```
docs/
├── getting-started/           (-2 files)
│   ├── complete-setup-guide.md (includes installation)
│   ├── quickstart-tutorial.md
│   ├── prerequisites-checker.md
│   └── environment-guides.md
├── user-guide/               (-2 files)
│   ├── cli-reference.md (NEW - consolidated CLI docs)
│   ├── command-builder.md
│   ├── visual-flow-diagrams.md
│   ├── parsers-overview.md
│   ├── configurable-court-extractor.md
│   ├── output-examples.md (includes format descriptions)
│   ├── working-with-output-data.md
│   ├── common-use-cases.md
│   └── understanding-errors.md
├── reference/                (+1 file)
│   ├── parser-classes-overview.md
│   ├── parser-appeals-al.md (expanded with implementation)
│   ├── parser-1819.md
│   ├── parser-daily-news.md
│   ├── base-parser.md
│   ├── court-extractor-classes.md (NEW)
│   ├── court-url-paginator.md
│   └── data-structures.md
├── developer/                (-1 file)
│   ├── architecture.md
│   ├── creating-custom-parsers.md (consolidated guide)
│   ├── court-extractor-design.md (architecture only)
│   ├── workflows.md
│   ├── error-handling.md
│   └── user-agent-headers-guide.md
└── about/
    ├── contributing.md
    └── license.md
```

## Implementation Steps

### Phase 1: Quick Wins (Immediate Impact)
1. Delete the 3 redirect-only files
2. Update `mkdocs.yml` navigation to remove deleted files
3. Merge installation content into `complete-setup-guide.md`

### Phase 2: CLI Consolidation
1. Create new `cli-reference.md` combining content from:
   - `cli-usage.md`
   - `command_line_tools.md`
2. Structure with clear sections:
   - Basic command structure
   - Complete parameter reference
   - Common examples
   - Link to command builder
3. Delete the original files after consolidation

### Phase 3: Parser Documentation
1. Consolidate ParserAppealsAL documentation
2. Merge parser creation guides
3. Ensure no information is lost in consolidation

### Phase 4: Court Extractor Reorganization
1. Extract implementation code to new class reference documentation
2. Refocus design document on architecture
3. Update cross-references between documents

## Expected Benefits

- **30% Reduction in Files**: From 35+ to ~25 files
- **Eliminate Redundancy**: Single source of truth for each topic
- **Improved Navigation**: Logical flow from setup → usage → reference → development
- **Better User Experience**: Users find information without jumping between files
- **Easier Maintenance**: Updates only needed in one place

## Success Metrics

- Reduced time to find information
- Fewer support questions about documentation
- Easier onboarding for new users
- Simplified documentation maintenance

## Notes

- All content should be preserved during consolidation
- Update all cross-references when moving content
- Test navigation paths after each phase
- Consider user feedback during implementation