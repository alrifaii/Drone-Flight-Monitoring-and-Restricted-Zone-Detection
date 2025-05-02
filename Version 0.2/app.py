from flask import Flask, render_template, jsonify
from random import uniform
import random
import time
from threading import Thread
from datetime import datetime
import math
from pymongo import MongoClient
from driver_setup import init_driver
from zone_checker import get_zone_info, get_info_div
from geopy.geocoders import Nominatim

app = Flask(__name__)

# MongoDB URI
MONGO_URI = "mongodb+srv://alrifaim005:2V0EIHs52erDKubu@cluster0.y2ldvix.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Connect to MongoDB Atlas
client = MongoClient(MONGO_URI)
db = client["Clusters"]
locations_collection = db["locations"]

# Configuration
VIENNA_CENTER = (48.2082, 16.3738)
RADIUS_KM = 2  # 200km radius
UPDATE_INTERVAL = 5  # seconds

# Store locations with timestamps
locations = []
driver = init_driver()

# Function to load previous locations from MongoDB to avoid re-uploading
def load_locations_from_db():
    global locations
    # Fetch all locations from DB, excluding the _id field
    locations = list(locations_collection.find({}, {"_id": 0}))  # Exclude _id field


# Function to insert new location into MongoDB
def insert_new_location(location):
    try:
        # Insert the new location into MongoDB
        locations_collection.insert_one(location)
        print("New location inserted into MongoDB.")
    except Exception as e:
        print(f"Error inserting data into MongoDB: {e}")

# Load previous locations from MongoDB on startup
load_locations_from_db()

def get_address_from_coordinates(lat, lon):
    geolocator = Nominatim(user_agent="coordinate_to_address")
    location = geolocator.reverse((lat, lon), exactly_one=True)
    if location:
        return location.address
    else:
        return "Address not found"

def generate_random_location():
    """Generate random point within RADIUS_KM of the last generated point"""
    lat, lng = VIENNA_CENTER

    while True:
        # Convert km to degrees (approx)
        radius_deg = RADIUS_KM / 111  # 1° latitude ≈ 111km
        
        # Generate random point in a circle around the current point
        angle = 4.8  # Random angle (0 to 2π)
        distance = uniform(0, radius_deg)  # Random distance within radius_deg
        # Calculate new coordinates based on angle and distance
        new_lat = lat + (distance * math.cos(angle))
        new_lng = lng + (distance * math.sin(angle))

        # Get the permission for the new location
        checkpermission = (get_zone_info(driver, f"{new_lat}/{new_lng}")).get("permission", "Unknown!")
        InfoData = (get_info_div(driver, f"{new_lat}/{new_lng}")).get("info_html")
        # Get the current time as timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        droneheight = random.randint(3, 200)
        print(f"Generated height: {droneheight}")
        address = get_address_from_coordinates(new_lat, new_lng)

        # 1New location data
        new_location = {
            "lat": new_lat,
            "lng": new_lng,
            "time": timestamp,
            "permission": checkpermission,
            "InfoHtml": InfoData,
            "Height": droneheight,
            "address": address,
            "id": len(locations) + 1  # Ensure the ID is unique
        }

        # Check if this location already exists in MongoDB
        if not locations_collection.find_one({"lat": new_lat, "lng": new_lng, "time": timestamp}):
            # Insert new location if not found
            insert_new_location(new_location)
            locations.append(new_location)

        # Update the current lat, lng for the next iteration
        lat, lng = new_lat, new_lng
        
        time.sleep(UPDATE_INTERVAL)

load_locations_from_db()
Thread(target=generate_random_location, daemon=True).start()

@app.route('/')
def observer():
    return render_template('observer.html')
from bson import ObjectId

def serialize_objectid(location):
    """Converts ObjectId to string."""
    if isinstance(location, dict):
        for key, value in location.items():
            if isinstance(value, ObjectId):
                location[key] = str(value)  # Convert ObjectId to string
    return location

@app.route('/get_locations')
def get_locations():
    # Serialize ObjectId to string before returning
    serialized_locations = [serialize_objectid(loc) for loc in locations]
    return jsonify(serialized_locations)

if __name__ == '__main__':
    try:
        app.run(debug=True)
    finally:
        driver.quit()
