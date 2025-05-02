from pymongo import MongoClient
import json

# MongoDB URI
MONGO_URI = "mongodb+srv://alrifaim005:V0EIHs52erDKubu@cluster0.y2ldvix.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Connect to MongoDB Atlas
client = MongoClient(MONGO_URI)

# Access the "Clusters" database
db = client["Clusters"]

# Create or access the "locations" collection
locations_collection = db["locations"]

# Function to load a test JSON file and insert it into MongoDB
def load_and_insert_json(file_path):
    # Load the JSON data from a file
    with open(file_path, "r") as file:
        data = json.load(file)  # Convert JSON data into a Python dictionary
    
    # Insert the data into the MongoDB collection
    locations_collection.insert_many(data)  # Use insert_many for inserting multiple records

    print("Data inserted successfully.")

# Call the function and provide the path to your test JSON file
load_and_insert_json("locations.json")
