from flask import Flask, render_template, jsonify
from random import uniform
import time
from threading import Thread
from datetime import datetime
import math
from driver_setup import init_driver
from zone_checker import get_zone_info


app = Flask(__name__)

# Configuration
VIENNA_CENTER = (48.2082, 16.3738)
RADIUS_KM = 12  # 200km radius
UPDATE_INTERVAL = 3  # seconds

# Store locations with timestamps
locations = []
driver = init_driver()

def generate_random_location():
    """Generate random point within RADIUS_KM of the last generated point"""
    # Start from Vienna center initially
    lat, lng = VIENNA_CENTER

    while True:
        # Convert km to degrees (approx)
        radius_deg = RADIUS_KM / 111  # 1° latitude ≈ 111km
        
        # Generate random point in a circle around the current point
        angle = uniform(0, 2 * math.pi)  # Random angle (0 to 2π)
        distance = uniform(0, radius_deg)  # Random distance within radius_deg

        # Calculate new coordinates based on angle and distance
        new_lat = lat + (distance * math.cos(angle))
        new_lng = lng + (distance * math.sin(angle))

        # Get the permission for the new location
        checkpermission = (get_zone_info(driver, f"{new_lat}/{new_lng}")).get("permission", "❌ Unbekannt")
        
        # Get the current time as timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Add the new location to the list
        locations.append({
            "lat": new_lat,
            "lng": new_lng,
            "time": timestamp,
            "permission": checkpermission,
            "id": len(locations) + 1
        })
        
        # Update the current lat, lng for the next iteration
        lat, lng = new_lat, new_lng
        
        
        time.sleep(UPDATE_INTERVAL)
Thread(target=generate_random_location, daemon=True).start()

@app.route('/')
def observer():
    return render_template('observer.html')

@app.route('/get_locations')
def get_locations():
    return jsonify(locations)

if __name__ == '__main__':
    try:
        app.run(debug=True)
    finally:
        driver.quit()
