# Jekyll Documentation Setup Instructions

## GitHub Pages Configuration

Since you want to serve from the main branch, follow these steps:

### 1. Repository Settings
1. Go to your repository on GitHub
2. Click on **Settings** → **Pages**
3. Under **Source**, select:
   - **Deploy from a branch**
   - Branch: **main**
   - Folder: **/ (root)**
4. Click **Save**

### 2. Files Created
- `_config.yml` - Jekyll configuration
- `index.md` - Main documentation page with navigation
- All docs files now have Jekyll front matter

### 3. Important Notes
- GitHub Pages will automatically build your Jekyll site from the main branch
- No GitHub Actions needed for this simple setup
- Your site will be available at: `https://[your-username].github.io/opal_beautifulsoup/`

### 4. Update _config.yml
Replace `yourusername` in the config file with your actual GitHub username:
```yaml
url: "https://yourusername.github.io"
```

### 5. Local Testing (Optional)
To test locally:
```bash
gem install jekyll bundler
jekyll serve
```

## Next Steps
1. Commit all changes
2. Push to main branch
3. Wait 5-10 minutes for GitHub Pages to build
4. Visit your documentation site

## Troubleshooting
- If you see a 404, check that GitHub Pages is enabled in settings
- Ensure the repository is public (or you have GitHub Pro for private repos)
- Check the Actions tab for any build errors