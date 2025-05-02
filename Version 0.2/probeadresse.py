from geopy.geocoders import Nominatim

def get_address_from_coordinates(lat, lon):
    geolocator = Nominatim(user_agent="coordinate_to_address")
    location = geolocator.reverse((lat, lon), exactly_one=True)
    if location:
        return location.address
    else:
        return "Address not found"

# Example usage
latitude = 48.2082
longitude = 16.3738

address = get_address_from_coordinates(latitude, longitude)
print(f"Coordinates: ({latitude}, {longitude})")
print(f"Address: {address}")