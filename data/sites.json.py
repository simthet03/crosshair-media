import os
import json

def read_json_file(file_path):
    """Reads a JSON file and returns its content."""
    with open(file_path, 'r') as file:
        return json.load(file)

def write_json_file(file_path, data):
    """Writes data to a JSON file."""
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def generate_sites_json(root_directory, output_directory):
    """Generates sites.json in the output directory based on the extracted data."""
    # Define the structure for sites.json
    sites_structure = []

    # Check for JSON files in the root directory, excluding the specified files
    excluded_files = ["sites.json", "schema.json", "image_list.json"]
    files_found = []

    for root, _, files in os.walk(root_directory):
        for file in files:
            if file.endswith(".json") and file not in excluded_files:
                files_found.append(file)
                file_path = os.path.join(root, file)
                print(f"Found {file} at {file_path}")

                # Read the JSON file and extract the necessary data
                data = read_json_file(file_path)

                # Assuming the JSON file contains the necessary site data
                site_info = {
                    "site_id": data.get("site_id", "unknown"),
                    "name": data.get("name", "unknown"),
                    "address": data.get("location", {}).get("address", "unknown"),
                    "format": data.get("format", "unknown"),
                    "location": {
                        "coordinates": {
                            "latitude": float(data.get("location", {}).get("coordinates", {}).get("latitude", 0)),
                            "longitude": float(data.get("location", {}).get("coordinates", {}).get("longitude", 0))
                        }
                    }
                }
                sites_structure.append(site_info)

    # Check if any JSON files were found
    if files_found:
        print("JSON files found and processed.")
    else:
        print("No JSON files found.")

    # Generate the sites.json file in the output directory
    output_file_path = os.path.join(output_directory, "sites.json")
    write_json_file(output_file_path, sites_structure)
    print(f"Generated sites.json at {output_file_path}")

if __name__ == "__main__":
    # Define the root directory and output directory
    root_directory = r"C:\AtlegaTech\CrossHairMedia\data"  # Update this to your actual root directory
    output_directory = r"C:\temp"

    # Generate the sites.json file
    generate_sites_json(root_directory, output_directory)