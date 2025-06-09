import os
import sys

# Get absolute path to current directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Construct path to data files
DATA_PATH = os.path.join(BASE_DIR, '..', 'data')