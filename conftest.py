import sys
import os

# Add the project root and src/ to sys.path so that:
# - "from src.X import ..." works in tests
# - "from helper.config import ..." works inside duplicate_checking.py
sys.path.insert(0, os.path.dirname(__file__))          # project root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))  # src/
