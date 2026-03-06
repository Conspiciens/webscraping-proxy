from dataclasses import dataclass, asdict

@dataclass
class Car: 
    link: str
    vehicle: str
    battery_type: str
    battery_size: str
    combined_mileage_km: int
    port: str 
    acceleration_0_60: int
    discontinued: bool

