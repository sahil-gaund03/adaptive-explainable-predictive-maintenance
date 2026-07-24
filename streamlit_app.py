"""
Streamlit Community Cloud Root Deployment Entry Point
Delegates execution to src/dashboard/app.py
"""

import os
import sys
from pathlib import Path

# Add project root directory to Python path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

# Execute main Streamlit dashboard application
if __name__ == "__main__":
    import runpy
    dashboard_path = PROJECT_ROOT / "src" / "dashboard" / "app.py"
    runpy.run_path(str(dashboard_path), run_name="__main__")
