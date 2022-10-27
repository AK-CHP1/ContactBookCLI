import os
import sys

# Adding the previous directory to path so that tests can import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import cbook


