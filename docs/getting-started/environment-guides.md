# Environment-Specific Setup Guides

This guide provides detailed setup instructions for different operating systems and environments. Choose your platform below for specific instructions.

## Quick Platform Selection

- **[Windows Setup](#windows-setup)** - PowerShell, Command Prompt, PATH configuration
- **[macOS Setup](#macos-setup)** - Terminal, Homebrew, security settings
- **[Linux Setup](#linux-setup)** - Ubuntu, CentOS, Debian, and others
- **[Cloud Environments](#cloud-environments)** - Google Colab, GitHub Codespaces

---

## Windows Setup

### Prerequisites

Before starting, ensure you have:
- Windows 10 or newer
- Administrator access (for Python installation)
- Internet connection

### Step 1: Install Python

#### Option A: From Microsoft Store (Easiest)
1. Open Microsoft Store
2. Search for "Python 3.11" or "Python 3.10"
3. Click "Install"
4. Python will be automatically added to PATH

#### Option B: From Python.org (Recommended)
1. Go to [python.org/downloads](https://python.org/downloads)
2. Download Python 3.8+ for Windows
3. **IMPORTANT**: Check "Add Python to PATH" during installation
4. Choose "Install Now"

#### Verify Installation
Open Command Prompt or PowerShell and run:
```cmd
python --version
pip --version
```

**Troubleshooting**:
- If "python is not recognized": Reinstall Python with "Add to PATH" checked
- If PowerShell shows execution policy errors: Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### Step 2: Create Project Directory

```cmd
# Create and navigate to project folder
mkdir C:\opal-project
cd C:\opal-project

# Download OPAL
git clone https://github.com/your-repo/opal .
# OR download and extract ZIP file to this folder
```

### Step 3: Set Up Virtual Environment

**Command Prompt:**
```cmd
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# You should see (venv) in your prompt
```

**PowerShell:**
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\Activate.ps1

# If you get execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\Activate.ps1
```

### Step 4: Install OPAL

```cmd
# With virtual environment activated
pip install -e .

# Or install requirements first:
pip install -r requirements.txt
```

### Step 5: Install Google Chrome

1. Download from [google.com/chrome](https://google.com/chrome)
2. Install normally
3. Chrome will be automatically detected by OPAL

### Step 6: Test Installation

```cmd
# Check prerequisites
python check_prerequisites.py

# Test OPAL
python -m opal --help
```

### Windows-Specific Issues

#### PATH Problems
```cmd
# Check if Python is in PATH
where python

# If not found, add manually:
# 1. Open "Environment Variables" in Windows settings
# 2. Add Python installation path (e.g., C:\Python39\)
# 3. Add Scripts folder (e.g., C:\Python39\Scripts\)
```

#### Virtual Environment Issues
```cmd
# If activation fails:
python -m venv --clear venv
venv\Scripts\activate
```

#### Permission Errors
```cmd
# Run Command Prompt as Administrator if needed
# Or use user-level installation:
pip install --user -e .
```

#### Chrome Driver Issues
- OPAL automatically manages ChromeDriver
- Ensure Chrome is updated to latest version
- Windows Defender may sometimes block automated browsers - add exceptions if needed

---

## macOS Setup

### Prerequisites

- macOS 10.15 (Catalina) or newer
- Terminal access
- Internet connection

### Step 1: Install Python

#### Option A: Using Homebrew (Recommended)

First, install Homebrew if you don't have it:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Then install Python:
```bash
# Install Python
brew install python3

# Verify installation
python3 --version
pip3 --version
```

#### Option B: From Python.org
1. Download Python 3.8+ from [python.org/downloads](https://python.org/downloads)
2. Install the .pkg file
3. Python will be available as `python3`

#### Option C: Using pyenv (For Multiple Versions)
```bash
# Install pyenv
brew install pyenv

# Add to your shell profile (.zshrc or .bash_profile):
echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init --path)"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc

# Restart terminal, then:
pyenv install 3.10.0
pyenv global 3.10.0
```

### Step 2: Create Project Directory

```bash
# Create and navigate to project folder
mkdir ~/opal-project
cd ~/opal-project

# Download OPAL
git clone https://github.com/your-repo/opal .
```

### Step 3: Set Up Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# You should see (venv) in your prompt
```

### Step 4: Install OPAL

```bash
# With virtual environment activated
pip install -e .
```

### Step 5: Install Google Chrome

1. Download from [google.com/chrome](https://google.com/chrome)
2. Drag to Applications folder
3. Open Chrome once to complete setup

### Step 6: Handle macOS Security

When OPAL first runs ChromeDriver:

1. macOS may show: "chromedriver cannot be opened because it is from an unidentified developer"
2. Go to System Preferences → Security & Privacy
3. Click "Allow Anyway" next to the ChromeDriver message
4. Or run: `xattr -d com.apple.quarantine /path/to/chromedriver`

### Step 7: Test Installation

```bash
# Check prerequisites
python check_prerequisites.py

# Test OPAL
python -m opal --help
```

### macOS-Specific Issues

#### Command Line Tools
```bash
# If you get compiler errors:
xcode-select --install
```

#### Homebrew Issues
```bash
# If brew command not found:
echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

#### SSL Certificate Issues
```bash
# If you get SSL errors:
/Applications/Python\ 3.x/Install\ Certificates.command
```

#### Permission Issues
```bash
# If pip install fails with permissions:
pip install --user -e .
```

---

## Linux Setup

### Ubuntu/Debian

#### Step 1: Update System
```bash
sudo apt update
sudo apt upgrade -y
```

#### Step 2: Install Python and Dependencies
```bash
# Install Python 3.8+
sudo apt install python3 python3-pip python3-venv python3-dev -y

# Install additional dependencies
sudo apt install build-essential curl git -y

# Verify installation
python3 --version
pip3 --version
```

#### Step 3: Install Google Chrome
```bash
# Download and install Chrome
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt update
sudo apt install google-chrome-stable -y
```

#### Step 4: Set Up OPAL
```bash
# Create project directory
mkdir ~/opal-project
cd ~/opal-project

# Download OPAL
git clone https://github.com/your-repo/opal .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install OPAL
pip install -e .
```

### CentOS/RHEL/Fedora

#### Step 1: Install Python
```bash
# CentOS/RHEL 8+
sudo dnf install python3 python3-pip python3-devel git -y

# CentOS/RHEL 7
sudo yum install python3 python3-pip python3-devel git -y

# Fedora
sudo dnf install python3 python3-pip python3-devel git -y
```

#### Step 2: Install Google Chrome
```bash
# Add Google Chrome repository
sudo tee /etc/yum.repos.d/google-chrome.repo <<EOF
[google-chrome]
name=google-chrome
baseurl=http://dl.google.com/linux/chrome/rpm/stable/x86_64
enabled=1
gpgcheck=1
gpgkey=https://dl.google.com/linux/linux_signing_key.pub
EOF

# Install Chrome
sudo dnf install google-chrome-stable -y
# or: sudo yum install google-chrome-stable -y
```

#### Step 3: Set Up OPAL
```bash
# Same as Ubuntu steps above
mkdir ~/opal-project
cd ~/opal-project
git clone https://github.com/your-repo/opal .
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

### Arch Linux

```bash
# Install dependencies
sudo pacman -S python python-pip git google-chrome

# Set up OPAL
mkdir ~/opal-project
cd ~/opal-project
git clone https://github.com/your-repo/opal .
python -m venv venv
source venv/bin/activate
pip install -e .
```

### Linux Server (Headless)

For servers without GUI:

```bash
# Install Chrome headless
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt update
sudo apt install google-chrome-stable -y

# Install virtual display (if needed)
sudo apt install xvfb -y

# OPAL runs in headless mode by default, so this should work fine
```

### Linux-Specific Issues

#### Missing Dependencies
```bash
# If you get build errors:
sudo apt install build-essential python3-dev libffi-dev libssl-dev

# For CentOS/RHEL:
sudo dnf groupinstall "Development Tools"
sudo dnf install python3-devel libffi-devel openssl-devel
```

#### Chrome Sandbox Issues
```bash
# If Chrome fails to start:
google-chrome --no-sandbox --disable-dev-shm-usage --headless --version
```

#### Virtual Environment Issues
```bash
# If venv creation fails:
sudo apt install python3-venv
# or
pip3 install virtualenv
virtualenv venv
```

---

## Cloud Environments

### Google Colab

Google Colab provides a pre-configured Python environment. Here's how to set up OPAL:

#### Step 1: Install Dependencies
```python
# In a Colab cell:
!pip install requests beautifulsoup4 selenium webdriver-manager

# Install Chrome (already available in Colab)
!apt-get update
!apt install chromium-chromedriver
```

#### Step 2: Download OPAL
```python
# Clone OPAL repository
!git clone https://github.com/your-repo/opal
%cd opal

# Install OPAL
!pip install -e .
```

#### Step 3: Configure for Colab
```python
# Set up Chrome options for Colab
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# OPAL automatically handles headless mode, but you can verify:
import os
os.environ['DISPLAY'] = ':99'  # Virtual display
```

#### Step 4: Test OPAL
```python
# Check prerequisites
!python check_prerequisites.py

# Test basic functionality
!python -m opal --help
```

#### Colab-Specific Notes
- Chrome runs in headless mode (no GUI)
- Files are saved to Colab's temporary storage
- Download results before session ends
- Runtime may reset after inactivity

### GitHub Codespaces

#### Step 1: Create Codespace
1. Go to your OPAL repository on GitHub
2. Click "Code" → "Codespaces" → "Create codespace"
3. Wait for environment to load

#### Step 2: Install Dependencies
```bash
# Codespaces comes with Python pre-installed
python --version

# Install Chrome
sudo apt update
sudo apt install google-chrome-stable -y

# Set up OPAL
pip install -e .
```

#### Step 3: Configure Environment
```bash
# Check prerequisites
python check_prerequisites.py

# Test OPAL
python -m opal --help
```

#### Codespaces-Specific Notes
- Pre-configured development environment
- Persistent storage within the codespace
- Chrome runs in headless mode
- Good for development and testing

### Docker

For containerized deployment:

#### Dockerfile Example
```dockerfile
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Set up Python environment
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN pip install -e .

# Run OPAL
CMD ["python", "-m", "opal", "--help"]
```

#### Building and Running
```bash
# Build container
docker build -t opal .

# Run container
docker run -v $(pwd)/output:/app/output opal python -m opal --url https://1819news.com/ --parser Parser1819 --max_pages 2
```

---

## Environment Verification

After setup on any platform, run these verification steps:

### 1. Prerequisites Check
```bash
python check_prerequisites.py
```

### 2. Basic Functionality Test
```bash
# Test help command
python -m opal --help

# Test small scrape
python -m opal --url https://1819news.com/ --parser Parser1819 --max_pages 1
```

### 3. Court Scraping Test
```bash
# Test court functionality (uses Chrome)
python -m opal --url https://publicportal.alappeals.gov/portal/search/case/results --parser ParserAppealsAL --max_pages 1
```

### 4. Check Output
```bash
# List generated files
ls -la *.json

# View file contents
cat *Parser1819*.json | head -20
```

## Getting Help

If you encounter issues specific to your environment:

1. **Run the prerequisites checker** - It will identify most platform-specific issues
2. **Check the main setup guide** - [Complete Setup Guide](complete-setup-guide.md) for general instructions
3. **Review error solutions** - [Understanding Errors](../user-guide/understanding-errors.md) for troubleshooting
4. **Platform-specific forums** - Each OS has community forums for technical support

Most setup issues are related to:
- Python not being in PATH
- Virtual environment not activated  
- Missing permissions
- Chrome/ChromeDriver configuration

The environment-specific instructions above address the most common issues for each platform!