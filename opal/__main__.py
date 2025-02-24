"""
Entry point for running the OPAL parser as a module (python -m opal)
"""
import sys
from opal.main import main

if __name__ == "__main__":
    # Call the main function and use its return code as the exit code
    sys.exit(main())
