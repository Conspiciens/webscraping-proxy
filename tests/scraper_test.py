import os
import sys 

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import charger_scraper 
from dynamic_json import JsonHandler

HTML_FILE = 'page_test_1.html' 
JSON_FILE = 'ev.json' 
    
json_file = open(JSON_FILE) 
file = open(HTML_FILE, 'r', encoding='utf-8') 
html_content = file.read()


def test_reading_iterator(): 
    pass  

def test_fetch_page_num(): 
    page_num = int(charger_scraper.
        check_num_pages(html_content)) 

    assert page_num == 124
    
def test_json_iterator():         
    json = JsonHandler(JSON_FILE)  
    

    


