import os
import json
import logging
from geopy.geocoders import Nominatim

# Initialize the geolocator
geolocator = Nominatim(user_agent="json_geo_updater")

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Path to the directory containing JSON files
json_dir = os.getcwd()

# Function to update JSON files with missing coordinates
def update_coordinates_in_json():
    for filename in os.listdir(json_dir):
        # Skip non-JSON files, schema.json, and image_list.json
        if not filename.endswith(".json") or filename == "schema.json" or filename == "image_list.json":
            continue

        file_path = os.path.join(json_dir, filename)

        try:
            with open(file_path, "r") as file:
                data = json.load(file)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            logging.error(f"Error loading file {filename}: {e}")
            continue

        # Check if 'location' and 'coordinates' keys exist
        if "location" in data and "coordinates" in data["location"]:
            coordinates = data["location"]["coordinates"]
            # If latitude or longitude is missing
            if not coordinates.get("latitude") or not coordinates.get("longitude"):
                address = data["location"].get("address")
                if address:
                    logging.info(f"Looking up coordinates for address: {address}")
                    try:
                        location = geolocator.geocode(address)
                        if location:
                            # Update the JSON file with the coordinates
                            data["location"]["coordinates"]["latitude"] = location.latitude
                            data["location"]["coordinates"]["longitude"] = location.longitude
                            logging.info(f"Updated {filename} with coordinates: {location.latitude}, {location.longitude}")
                        else:
                            logging.warning(f"Could not find coordinates for: {address}")
                    except Exception as e:
                        logging.error(f"Error during geocoding for {address}: {e}")
                else:
                    logging.warning(f"No address found in {filename} to perform geocoding.")

        # Write the updated data back to the JSON file
        try:
            with open(file_path, "w") as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            logging.error(f"Error writing to file {filename}: {e}")

# Run the function
if __name__ == "__main__":
    update_coordinates_in_json()
