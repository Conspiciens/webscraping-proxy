import asyncio
import requests
import ijson
import json
import time

from dynamic_json import JsonHandler

from requests_html import AsyncHTMLSession, MaxRetries
from bs4 import BeautifulSoup
from collections import deque 
from dataclasses import asdict
from typing import Optional, TextIO
from requests import RequestException, HTTPError, ConnectionError, Timeout, TooManyRedirects
from collections import deque
from dataclasses_types import Car

user_agents = [
 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36", 
 "", 
 "" 
] 

async def request_link(assesion, link: str) -> Optional[requests.Response]: 
    stand_off = 6
    tries = 0 
    response = None

    while tries < 5: 
        try: 
            print(f"Requesting link: {link}") 
            await asyncio.sleep(20) 
            response = await assesion.get(link, timeout=30)
            await response.html.arender(wait=2.0, timeout=20)
            response.raise_for_status()
            return response
        except HTTPError as e: 
            print(f"Error: {e}") 
            print(f"Seconds waiting: { 2 ** stand_off }") 
            await asyncio.sleep(2 ** stand_off)
            stand_off += 1
            print(f"Issue with attempting to connect: {link}, Attempt: {tries}") 
            tries += 1 
            continue 
        except Timeout as e: 
            print(f"Timeout Occured: {e}");
            tries += 1
        except ConnectionError as e:
            print(f"Connection Error Occured: {e}");
            tries += 1
            break
        except MaxRetries as e: 
            print(f"Max Retries: {e}")
            await asynico.sleep(stand_off)
            stand_off = stand_off ** 3
            tries += 1
        except TooManyRedirects as e: 
            print(f"Too Many Redirects Occured: {e}");
            print(f"Request Error Occured: {e}");
            tries += 1 
    
    return None 

def check_num_pages(response: str) -> str: 
    soup = BeautifulSoup(response, 'lxml') 
    
    txt = soup.find(class_='jplist-label').text
    return txt.split(' ')[-1] 


def fetch_car_links(response: requests.Response) -> list: 
    soup = BeautifulSoup(response.html.raw_html, 'lxml')
    
    car_links = soup.find_all('a', href=True) 
    car_links = [car_link['href'] for car_link in car_links if "/car/" in car_link['href']]  

    return car_links 
    
def fetch_car_info(link: str, response: requests.Response) -> Car:
    soup = BeautifulSoup(response.text, 'lxml')

    vehicle_name = link.split("/")[-1] 
    discontinued_div = soup.find(class_='sub-header').find_all('span') 
    range_table = soup.find('div', {'id': 'range'}) 
    battery_table = soup.find('div', {'id': 'battery'})
    charging_table = soup.find('div', {'id': 'charging'})
    performance_table = soup.find('div', {'id': 'performance'})

    is_discontinued = fetch_discontinued(discontinued_div)
    combined_range = fetch_combined_range(range_table) 
    (kw, battery_type) = fetch_battery_info(battery_table)
    car_port = fetch_charging_port(charging_table) 
    acceleration = fetch_performance_port(performance_table) 
    
    return Car(link, vehicle_name, battery_type, 
        kw, combined_range, car_port, acceleration, is_discontinued)  
    
def fetch_discontinued(spans: list) -> bool: 
    return False if "available" in spans[-1].text.lower() else True  

def fetch_combined_range(range_table: str) -> str:
    range_rows = range_table.find_all('td') 

    combined_range = None 
    combined_range = range_rows[5].text

    return combined_range

def fetch_battery_info(battery_table: str) -> tuple: 
    battery_rows = battery_table.find_all('td')

    battery_capacity = battery_rows[1].text
    battery_type = battery_rows[3].text

    return (battery_capacity, battery_type)

def fetch_charging_port(charging_table: str) -> str: 
    charging_rows = charging_table.find_all('td') 
    charging_type = charging_rows[11].text 

    return charging_type
    

def fetch_performance_port(performance_table: str) -> str: 
    performance_rows = performance_table.find_all('td')

    acceleration_60 = performance_rows[1].text

    return acceleration_60 

async def main(): 
    asession = AsyncHTMLSession() 
    asession.headers.update({
        "User-Agent" : '''Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36''',
        "Connection": "keep-alive",
    })

    JSON_FILENAME = "ev.json"
    # NOTE: rs-y is in relation to the year of the vehicle, should be updated 5 years ahead of current year
    car_link = "https://ev-database.org"
    page_list_links = "https://ev-database.org/#group=vehicle-group&rs-pr=10000_100000&rs-er=0_1000&rs-ld=0_1000&rs-ac=2_23&rs-dcfc=0_400&rs-ub=10_200&rs-tw=0_3000&rs-ef=100_350&rs-sa=-1_5&rs-w=1000_3500&rs-c=0_5000&rs-y=2010_2030&s=1"

    manager = JsonHandler(JSON_FILENAME) 
    car_page_links = deque()
    page_num = 0

    # Fetch total Pages
    response = await request_link(asession, page_list_links + f"&p={page_num}-10") 
    if response is None: 
        return 

    total_pages = check_num_pages(response.html.raw_html)
    total_pages = int(total_pages)

    while page_num <= total_pages: 
        response = await request_link(asession, page_list_links + f"&p={page_num}-10")

        if response is None:
            return

        car_links = fetch_car_links(response)
        car_page_links.extend(car_links)
        page_num += 1
 
    car_page_links = deque(list(set(car_page_links)))

    # Sleep a minute before making the next request
    await asyncio.sleep(60) 

    while len(car_page_links) > 0: 
         link = car_page_links.popleft(); 
         print(link)
         response = await request_link(asession, car_link + link)
         if response == None: 
            print(f"Breaking early due to {car_link + link}") 
            break 
         ev = fetch_car_info(link, response) 
        
         await asyncio.sleep(30) 
         if len(car_page_links) % 2 == 0: 
            await asyncio.sleep(10)
          
         if len(car_page_links) == 0: 
            manager.to_json_file(ev, link, True)    
            break

         manager.to_json_file(ev, link, False)
    manager.close_json_file()

    await asession.close() 

if __name__ == '__main__':
    asyncio.run(main())
