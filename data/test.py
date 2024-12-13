import os
import json
import jsonschema
import uuid
from jsonschema import validate
from datetime import datetime, timedelta
import random

# Path to the schema file
SCHEMA_FILE = "schema.json"

# Folder containing JSON files to validate
JSON_FOLDER = "./"  # Current directory

def load_schema(schema_file):
    """Load the JSON schema."""
    with open(schema_file, "r") as f:
        return json.load(f)

def ensure_field_completeness(data, schema):
    """Ensure all required fields are present in the JSON data."""
    for key, value in schema.get("properties", {}).items():
        if key not in data:
            if value.get("type") == "array":
                data[key] = []
            elif value.get("type") == "object":
                data[key] = {}
            elif value.get("type") == "number":
                data[key] = 0
            else:
                data[key] = ""
        elif isinstance(value.get("properties"), dict):
            ensure_field_completeness(data[key], value)

def generate_random_future_date():
    """Generate a random date in the future within 1 to 365 days from today."""
    future_days = random.randint(1, 365)
    future_date = datetime.now() + timedelta(days=future_days)
    return future_date.strftime("%Y-%m-%d")

def ensure_date_format(data, date_fields):
    """Ensure date fields are in the correct ISO 8601 format."""
    for field in date_fields:
        if field in data:
            try:
                # Attempt to parse and reformat the date
                parsed_date = datetime.strptime(data[field], "%Y-%m-%d")
                data[field] = parsed_date.strftime("%Y-%m-%d")
            except (ValueError, TypeError):
                print(f"Fixing invalid date format for field '{field}'...")
                data[field] = generate_random_future_date()
        else:
            # If the date field is missing, populate it with a random future date
            print(f"Adding missing date for field '{field}'...")
            data[field] = generate_random_future_date()

def validate_and_fix_json(json_file, schema, used_uuids):
    """Validate a JSON file against the schema, fix issues, and ensure UUID uniqueness."""
    with open(json_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as err:
            print(f"❌ {json_file} is invalid JSON.")
            print(f"Error: {err.msg}")
            return

    try:
        validate(instance=data, schema=schema)

        # Check if the UUID is unique
        if data["uuid"] in used_uuids:
            print(f"❌ {json_file} has a duplicate UUID: {data['uuid']}.")
            print(f"Fixing duplicate UUID in {json_file}...")
            # Generate a new valid UUID
            data["uuid"] = str(uuid.uuid4())

        # Ensure completeness of fields
        ensure_field_completeness(data, schema)

        # Ensure date format for specific fields
        ensure_date_format(data, ["availability"])

        used_uuids.add(data["uuid"])

        # Save the fixed file
        with open(json_file, "w") as f:
            json.dump(data, f, indent=4)

        print(f"✅ {json_file} is valid and fixed where necessary.")

    except jsonschema.exceptions.ValidationError as err:
        print(f"❌ {json_file} is invalid.")
        print(f"Error: {err.message}")

        # Attempt to fix issues
        if "uuid" in err.path:
            print(f"Fixing UUID in {json_file}...")
            data["uuid"] = str(uuid.uuid4())

        ensure_field_completeness(data, schema)
        ensure_date_format(data, ["availability"])

        # Save the fixed file
        with open(json_file, "w") as f:
            json.dump(data, f, indent=4)
        print(f"✔ Fixed issues for {json_file}.")

def main():
    # Load the schema
    schema = load_schema(SCHEMA_FILE)

    # Get all JSON files in the folder except schema.json
    json_files = [f for f in os.listdir(JSON_FOLDER) if f.endswith(".json") and f != SCHEMA_FILE]

    # Set to keep track of used UUIDs
    used_uuids = set()

    # Validate and fix each JSON file
    for json_file in json_files:
        validate_and_fix_json(os.path.join(JSON_FOLDER, json_file), schema, used_uuids)

if __name__ == "__main__":
    main()
