"""
Server module that re-exports the main server module.

This provides a clean import path for the CLI and other code.
"""

import os
import sys
import importlib.util

# Add the root directory to the Python path to find server module
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, root_dir)

# Import the server module
from server.server import * 