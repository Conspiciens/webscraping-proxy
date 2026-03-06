import json 
import ijson
import os
import dataclasses

from typing import Iterator
from dataclasses_types import Car

class JsonHandler:
    def __init__(self, filename: str): 
        self.json_file = open(filename, "w+") 
        self.json_file.write("{\n")
        
    def to_json_file(self, car: Car, link: str, is_last: bool) -> None: 
        car_json = json.dumps(dataclasses.asdict(car), indent=4)
        car_json = f"\"{link}\": " + car_json
    
        self.json_file.write(car_json) 

        if is_last: return 
        self.json_file.write(",\n")

    def close_json_file(self) -> None: 
        self.json_file.write("\n}") 

    def get_json_objects(self) -> Iterator[dict]: 
        self.json_file.seek(0) 
        return ijson.kvitems(self.json_file, "") 

    def __del__(self): 
        if not self.json_file.closed: 
            self.json_file.close() 
        if not os.path.exists(self.json_file.name):
            return 
        # os.remove(filename)
        
    

