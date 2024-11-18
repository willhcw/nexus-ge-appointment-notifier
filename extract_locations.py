# This python code is use to extract the location id and name from the Nexus and Global Entry APIs
# The extracted data is stored in a locations.json file

import requests
import json

# API URLs for Nexus and Global Entry
API_URLS = {
    "nexus": "https://ttp.cbp.dhs.gov/schedulerapi/locations/?temporary=false&inviteOnly=false&operational=true&serviceName=NEXUS",
    "global_entry": "https://ttp.cbp.dhs.gov/schedulerapi/locations/?temporary=false&inviteOnly=false&operational=true&serviceName=Global%20Entry"
}

# Extract the location data from the API
def fetch_locations(api_url):
    """Fetch the location data from the API"""
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data from {api_url}: {e}")
        return []
    
def generate_locations_json():
    """Generate the locations.json file with the location data from the Nexus and Global Entry APIs"""
    locations_data = {"locations": {}}

    for program, url in API_URLS.items():
        print(f"Fetching locations for {program}...")
        program_locations = fetch_locations(url)
        locations_data["locations"][program] = {
            location["name"]: location["id"] for location in program_locations
        }

    # Save the data to a JSON file
    output_file = "locations.json"
    with open(output_file, "w") as file:
        json.dump(locations_data, file, indent=4)

    print(f"Locations data saved to {output_file}")

if __name__ == "__main__":
    generate_locations_json()