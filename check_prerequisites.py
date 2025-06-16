#!/usr/bin/env python3
"""
OPAL Prerequisites Checker

This script verifies that your system is ready to run OPAL.
Run this script before installing OPAL to catch potential issues early.

Usage:
    python check_prerequisites.py
"""

import sys
import subprocess
import platform
import urllib.request
import ssl
import json
from pathlib import Path


class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

    @classmethod
    def disable(cls):
        """Disable colors for non-terminal environments"""
        cls.GREEN = cls.RED = cls.YELLOW = cls.BLUE = cls.BOLD = cls.END = ''


class PrerequisitesChecker:
    def __init__(self):
        self.results = []
        self.warnings = []
        self.errors = []
        
        # Disable colors on Windows without colorama
        if platform.system() == 'Windows':
            try:
                import colorama
                colorama.init()
            except ImportError:
                Colors.disable()
    
    def print_header(self):
        """Print the checker header"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}")
        print("OPAL Prerequisites Checker")
        print(f"{'='*60}{Colors.END}\n")
    
    def print_section(self, title):
        """Print a section header"""
        print(f"{Colors.BOLD}{Colors.BLUE}📋 {title}{Colors.END}")
        print("-" * (len(title) + 3))
    
    def check_result(self, name, status, message, fix_suggestion=None):
        """Record and display a check result"""
        if status == "pass":
            print(f"{Colors.GREEN}✅ {name}: {message}{Colors.END}")
            self.results.append({"name": name, "status": "pass", "message": message})
        elif status == "warn":
            print(f"{Colors.YELLOW}⚠️  {name}: {message}{Colors.END}")
            if fix_suggestion:
                print(f"   💡 Fix: {fix_suggestion}")
            self.warnings.append({"name": name, "message": message, "fix": fix_suggestion})
        else:  # fail
            print(f"{Colors.RED}❌ {name}: {message}{Colors.END}")
            if fix_suggestion:
                print(f"   💡 Fix: {fix_suggestion}")
            self.errors.append({"name": name, "message": message, "fix": fix_suggestion})
        print()
    
    def check_python_version(self):
        """Check Python version compatibility"""
        self.print_section("Python Environment")
        
        version = sys.version_info
        version_str = f"{version.major}.{version.minor}.{version.micro}"
        
        if version.major == 3 and version.minor >= 8:
            self.check_result(
                "Python Version", 
                "pass", 
                f"Python {version_str} (compatible)"
            )
        elif version.major == 3 and version.minor >= 6:
            self.check_result(
                "Python Version", 
                "warn", 
                f"Python {version_str} (minimum supported, but 3.8+ recommended)",
                "Consider upgrading to Python 3.8 or higher for best compatibility"
            )
        else:
            self.check_result(
                "Python Version", 
                "fail", 
                f"Python {version_str} (incompatible)",
                "Install Python 3.8 or higher from https://python.org"
            )
    
    def check_pip(self):
        """Check if pip is available"""
        try:
            import pip
            # Get pip version
            result = subprocess.run([sys.executable, "-m", "pip", "--version"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                pip_version = result.stdout.strip().split()[1]
                self.check_result(
                    "Package Installer (pip)", 
                    "pass", 
                    f"pip {pip_version} available"
                )
            else:
                self.check_result(
                    "Package Installer (pip)", 
                    "fail", 
                    "pip command failed",
                    "Run: python -m ensurepip --upgrade"
                )
        except ImportError:
            self.check_result(
                "Package Installer (pip)", 
                "fail", 
                "pip not found",
                "Install pip: python -m ensurepip --upgrade"
            )
        except Exception as e:
            self.check_result(
                "Package Installer (pip)", 
                "warn", 
                f"Could not verify pip: {e}",
                "Ensure pip is working: python -m pip --version"
            )
    
    def check_virtual_environment(self):
        """Check if running in virtual environment"""
        in_venv = (
            hasattr(sys, 'real_prefix') or 
            (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
        )
        
        if in_venv:
            venv_path = sys.prefix
            self.check_result(
                "Virtual Environment", 
                "pass", 
                f"Active virtual environment: {venv_path}"
            )
        else:
            self.check_result(
                "Virtual Environment", 
                "warn", 
                "Not running in virtual environment",
                "Create virtual environment: python -m venv venv && source venv/bin/activate"
            )
    
    def check_required_packages(self):
        """Check if required packages can be imported"""
        self.print_section("Required Packages")
        
        required_packages = {
            "requests": "HTTP library for web requests",
            "beautifulsoup4": "HTML parsing library",
            "selenium": "Web browser automation",
            "webdriver-manager": "Automatic ChromeDriver management"
        }
        
        for package, description in required_packages.items():
            try:
                if package == "beautifulsoup4":
                    import bs4
                    version = getattr(bs4, '__version__', 'unknown')
                    import_name = "bs4"
                elif package == "webdriver-manager":
                    import webdriver_manager
                    version = getattr(webdriver_manager, '__version__', 'unknown')
                    import_name = "webdriver_manager"
                else:
                    module = __import__(package)
                    version = getattr(module, '__version__', 'unknown')
                    import_name = package
                
                self.check_result(
                    f"{package}", 
                    "pass", 
                    f"Version {version} installed"
                )
            except ImportError:
                self.check_result(
                    f"{package}", 
                    "warn", 
                    f"Not installed ({description})",
                    f"Install with: pip install {package}"
                )
            except Exception as e:
                self.check_result(
                    f"{package}", 
                    "warn", 
                    f"Import error: {e}",
                    f"Reinstall with: pip install --upgrade {package}"
                )
    
    def check_chrome_browser(self):
        """Check if Chrome browser is available"""
        self.print_section("Browser Requirements")
        
        system = platform.system()
        chrome_found = False
        chrome_paths = []
        
        if system == "Windows":
            chrome_paths = [
                "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
                "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
                "C:\\Users\\%USERNAME%\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe"
            ]
        elif system == "Darwin":  # macOS
            chrome_paths = [
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
            ]
        else:  # Linux
            chrome_paths = [
                "/usr/bin/google-chrome",
                "/usr/bin/chromium-browser",
                "/usr/bin/chromium",
                "/snap/bin/chromium"
            ]
        
        # Check common installation paths
        for path in chrome_paths:
            if Path(path.replace("%USERNAME%", Path.home().name)).exists():
                chrome_found = True
                self.check_result(
                    "Google Chrome", 
                    "pass", 
                    f"Found at {path}"
                )
                break
        
        # Try command line check
        if not chrome_found:
            try:
                if system == "Windows":
                    result = subprocess.run(["where", "chrome"], capture_output=True, timeout=5)
                else:
                    result = subprocess.run(["which", "google-chrome"], capture_output=True, timeout=5)
                
                if result.returncode == 0:
                    chrome_found = True
                    self.check_result(
                        "Google Chrome", 
                        "pass", 
                        "Found in system PATH"
                    )
            except:
                pass
        
        if not chrome_found:
            self.check_result(
                "Google Chrome", 
                "fail", 
                "Google Chrome not found",
                "Install Chrome from https://google.com/chrome for court scraping functionality"
            )
    
    def check_chromedriver(self):
        """Check ChromeDriver availability"""
        try:
            from selenium import webdriver
            from webdriver_manager.chrome import ChromeDriverManager
            
            # webdriver-manager should handle this automatically
            self.check_result(
                "ChromeDriver Management", 
                "pass", 
                "webdriver-manager will handle ChromeDriver automatically"
            )
            
        except ImportError:
            self.check_result(
                "ChromeDriver Management", 
                "warn", 
                "Cannot verify - selenium/webdriver-manager not installed",
                "Install required packages first"
            )
        except Exception as e:
            self.check_result(
                "ChromeDriver Management", 
                "warn", 
                f"Cannot verify ChromeDriver setup: {e}",
                "This should work automatically when selenium is properly installed"
            )
    
    def check_network_connectivity(self):
        """Check network connectivity to target websites"""
        self.print_section("Network Connectivity")
        
        test_urls = [
            ("1819news.com", "https://1819news.com/"),
            ("Alabama Daily News", "https://www.aldailynews.com/"),
            ("Alabama Appeals Court", "https://publicportal.alappeals.gov/"),
            ("Python Package Index", "https://pypi.org/")
        ]
        
        for name, url in test_urls:
            try:
                # Create SSL context that's more permissive for testing
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                
                request = urllib.request.Request(url, headers={
                    'User-Agent': 'OPAL Prerequisites Checker/1.0'
                })
                
                with urllib.request.urlopen(request, timeout=10, context=ctx) as response:
                    if response.status == 200:
                        self.check_result(
                            f"Connection to {name}", 
                            "pass", 
                            f"Successfully connected ({response.status})"
                        )
                    else:
                        self.check_result(
                            f"Connection to {name}", 
                            "warn", 
                            f"Unexpected status code: {response.status}",
                            "Website may be temporarily unavailable"
                        )
            except urllib.error.HTTPError as e:
                if e.code == 403:
                    self.check_result(
                        f"Connection to {name}", 
                        "warn", 
                        "Access forbidden (403) - may block automated requests",
                        "This is normal - OPAL uses proper headers during scraping"
                    )
                else:
                    self.check_result(
                        f"Connection to {name}", 
                        "warn", 
                        f"HTTP error: {e.code}",
                        "Website may be temporarily unavailable"
                    )
            except Exception as e:
                self.check_result(
                    f"Connection to {name}", 
                    "warn", 
                    f"Connection failed: {str(e)[:50]}...",
                    "Check your internet connection"
                )
    
    def check_file_permissions(self):
        """Check file system permissions"""
        self.print_section("File System Permissions")
        
        try:
            # Test writing to current directory
            test_file = Path("opal_test_write.tmp")
            test_file.write_text("test")
            test_file.unlink()
            
            self.check_result(
                "Write Permissions", 
                "pass", 
                "Can write files in current directory"
            )
        except Exception as e:
            self.check_result(
                "Write Permissions", 
                "fail", 
                f"Cannot write to current directory: {e}",
                "Ensure you have write permissions in the OPAL directory"
            )
        
        # Check home directory access
        try:
            home_test = Path.home() / "opal_test_write.tmp"
            home_test.write_text("test")
            home_test.unlink()
            
            self.check_result(
                "Home Directory Access", 
                "pass", 
                "Can write to home directory"
            )
        except Exception as e:
            self.check_result(
                "Home Directory Access", 
                "warn", 
                f"Cannot write to home directory: {e}",
                "This may affect some OPAL operations"
            )
    
    def check_system_resources(self):
        """Check available system resources"""
        self.print_section("System Resources")
        
        try:
            import psutil
            
            # Check memory
            memory = psutil.virtual_memory()
            memory_gb = memory.total / (1024**3)
            
            if memory_gb >= 4:
                self.check_result(
                    "Memory (RAM)", 
                    "pass", 
                    f"{memory_gb:.1f} GB available"
                )
            elif memory_gb >= 2:
                self.check_result(
                    "Memory (RAM)", 
                    "warn", 
                    f"{memory_gb:.1f} GB available (minimum for basic operation)",
                    "4GB+ recommended for large scraping tasks"
                )
            else:
                self.check_result(
                    "Memory (RAM)", 
                    "warn", 
                    f"{memory_gb:.1f} GB available (may be insufficient)",
                    "Consider closing other applications while running OPAL"
                )
            
            # Check disk space
            disk = psutil.disk_usage('.')
            disk_gb = disk.free / (1024**3)
            
            if disk_gb >= 1:
                self.check_result(
                    "Disk Space", 
                    "pass", 
                    f"{disk_gb:.1f} GB free space available"
                )
            else:
                self.check_result(
                    "Disk Space", 
                    "warn", 
                    f"{disk_gb:.1f} GB free space",
                    "Consider freeing up disk space for output files"
                )
                
        except ImportError:
            self.check_result(
                "System Resources", 
                "warn", 
                "Cannot check system resources (psutil not available)",
                "Install psutil for system monitoring: pip install psutil"
            )
        except Exception as e:
            self.check_result(
                "System Resources", 
                "warn", 
                f"Cannot check resources: {e}",
                "Manual check recommended"
            )
    
    def print_summary(self):
        """Print final summary and recommendations"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}📊 Summary{Colors.END}")
        print("=" * 60)
        
        total_checks = len(self.results) + len(self.warnings) + len(self.errors)
        passed = len(self.results)
        warned = len(self.warnings)
        failed = len(self.errors)
        
        print(f"Total checks: {total_checks}")
        print(f"{Colors.GREEN}✅ Passed: {passed}{Colors.END}")
        print(f"{Colors.YELLOW}⚠️  Warnings: {warned}{Colors.END}")
        print(f"{Colors.RED}❌ Failed: {failed}{Colors.END}")
        
        if failed == 0 and warned == 0:
            print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 Perfect! Your system is ready for OPAL!{Colors.END}")
            print("\nNext steps:")
            print("1. Install OPAL: pip install -e .")
            print("2. Try the quick start tutorial")
            
        elif failed == 0:
            print(f"\n{Colors.YELLOW}{Colors.BOLD}✅ Good to go with minor warnings!{Colors.END}")
            print("\nYour system should work with OPAL, but consider addressing the warnings above.")
            print("\nNext steps:")
            print("1. Install OPAL: pip install -e .")
            print("2. Try the quick start tutorial")
            
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}⚠️  Issues need attention before using OPAL{Colors.END}")
            print("\nPlease fix the failed checks above before proceeding.")
            print("Each error includes suggested fixes.")
        
        print(f"\n{Colors.BLUE}📚 For help with setup:{Colors.END}")
        print("- Complete Setup Guide: docs/getting-started/complete-setup-guide.md")
        print("- Environment-specific guides: docs/getting-started/environment-guides.md")
        print("- Troubleshooting: docs/user-guide/understanding-errors.md")
        
        print(f"\n{Colors.BOLD}Happy scraping! 🚀{Colors.END}\n")
    
    def run_all_checks(self):
        """Run all prerequisite checks"""
        self.print_header()
        
        self.check_python_version()
        self.check_pip()
        self.check_virtual_environment()
        
        self.check_required_packages()
        
        self.check_chrome_browser()
        self.check_chromedriver()
        
        self.check_network_connectivity()
        
        self.check_file_permissions()
        
        self.check_system_resources()
        
        self.print_summary()
        
        # Return overall status
        return len(self.errors) == 0


def main():
    """Main entry point"""
    checker = PrerequisitesChecker()
    
    try:
        success = checker.run_all_checks()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠️  Check interrupted by user{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}❌ Unexpected error during checks: {e}{Colors.END}")
        print("Please report this issue with your system details.")
        sys.exit(1)


if __name__ == "__main__":
    main()