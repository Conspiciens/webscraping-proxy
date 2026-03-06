import os 
import sys 

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import charger_scraper 
from dynamic_json import JsonHandler


def test_request(): 
    charger_scraper.
