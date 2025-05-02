# location_generator.py
import math, time
from random import uniform
from datetime import datetime
from driver_setup import init_driver
from zone_checker import get_zone_info

def generate_random_location(center_lat, center_lng, radius_km, update_interval, max_locations, locations):
    """Generate random point within radius_km of center coordinates"""
    driver = init_driver()
    
    while True:
        # Convert km to degrees (approx)
        radius_deg = radius_km / 111
        
        # Generate random point in circle
        angle = uniform(0, 100 * math.pi)
        distance = uniform(0, radius_deg)
        
        lat = center_lat + distance * math.pi / 180 * math.cos(angle)
        lng = center_lng + distance * math.pi / 180 * math.sin(angle)
        checkpermission = (get_zone_info(driver, f"{lat}/{lng}")).get("permission")
        timestamp = datetime.now().strftime("%H:%M:%S")
        locations.append({
            "lat": lat,
            "lng": lng,
            "time": timestamp,
            "permission": checkpermission,
            "id": len(locations) + 1
        })
        
        # Keep only last max_locations
        if len(locations) > max_locations:
            locations.pop(0)
        
        time.sleep(update_interval)