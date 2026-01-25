"""
Import weather stations from GeoSphere Austria
"""

import os
import json
import random
import string
import requests
from string import capwords
import numpy as np
from urllib import request, error

# Map Austrian state names to ISO 3166-2 codes
REGION_CODES = {
    "Burgenland": "1",
    "Kärnten": "2",
    "Niederösterreich": "3",
    "Oberösterreich": "4",
    "Salzburg": "5",
    "Steiermark": "6",
    "Tirol": "7",
    "Vorarlberg": "8",
    "Wien": "9",
}

# API URL
API_URL = "https://dataset.api.hub.geosphere.at/v1/station/historical/klima-v2-1d/metadata"

# Path of the stations directory
STATIONS_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', '..', 'stations'
))

# Partial matches file
PARTIAL_MATCHES_FILE = os.path.join(
    os.path.dirname(__file__), 'partial_matches.md'
)


def generate_uid(private: bool = False) -> str:
    """
    Generate a unique station identifier
    """
    while True:
        uid = "".join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(5)
        )
        
        if private:
            uid = "$" + uid[1:]
        
        url = f"https://github.com/meteostat/weather-stations/blob/master/stations/{uid}.json"
        
        try:
            request.urlopen(url)
        except error.HTTPError:
            return uid


def get_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate distance between weather station and geo point
    """
    # Earth radius in meters
    radius = 6371000
    
    # Degrees to radian
    lat1, lon1, lat2, lon2 = map(np.deg2rad, [lat1, lon1, lat2, lon2])
    
    # Deltas
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    # Calculate distance
    arch = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    arch_sin = 2 * np.arcsin(np.sqrt(arch))
    
    return radius * arch_sin


def create_station_dict(data: dict) -> dict:
    """
    Create a station dict from provided data
    """
    result = {}
    
    # Add fields in the correct order
    result["id"] = data.get("id", None)
    
    if "active" in data:
        result["active"] = data["active"]
    
    result["name"] = data.get("name", {"en": None})
    result["country"] = data.get("country", None)
    result["region"] = data.get("region", None)
    result["identifiers"] = data.get("identifiers", {})
    result["location"] = {
        "latitude": data["location"].get("latitude", None)
        if "location" in data
        else None,
        "longitude": data["location"].get("longitude", None)
        if "location" in data
        else None,
        "elevation": data["location"].get("elevation", None)
        if "location" in data
        else None,
    }
    result["timezone"] = data.get("timezone", None)
    
    return result


def merge_dicts(source: dict, destination: dict) -> None:
    """
    Deep merge two dicts
    """
    for key, value in source.items():
        if isinstance(value, dict):
            node = destination.setdefault(key, {})
            merge_dicts(value, node)
        else:
            destination[key] = value


def create(data: dict) -> None:
    """
    Write a new weather station into a JSON file
    """
    # Get file path
    file = os.path.join(STATIONS_PATH, data["id"] + ".json")
    
    # Merge with template
    data = create_station_dict(data)
    
    # Write into file
    with open(file, "w", encoding="utf-8") as f:
        f.write(json.dumps(data, indent=4, default=str, ensure_ascii=False))


def update(data: dict) -> None:
    """
    Update an existing weather station
    """
    # Get file path
    file = os.path.join(STATIONS_PATH, data["id"] + ".json")
    
    # Read file and parse JSON
    with open(file, "r", encoding="utf-8") as f:
        state: dict = json.load(f)
    
    # Deep merge
    merge_dicts(data, state)
    
    # Write into file
    with open(file, "w", encoding="utf-8") as f:
        f.write(json.dumps(state, indent=4, default=str, ensure_ascii=False))


def load_existing_austrian_stations():
    """
    Load all existing Austrian stations from the repository
    """
    stations = []
    for filename in os.listdir(STATIONS_PATH):
        if filename.endswith('.json'):
            filepath = os.path.join(STATIONS_PATH, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                station = json.load(f)
                if station.get('country') == 'AT':
                    stations.append(station)
    return stations


def fetch_geosphere_stations():
    """
    Fetch stations from GeoSphere Austria API
    """
    response = requests.get(API_URL, timeout=30)
    response.raise_for_status()
    data = response.json()
    # Filter only active stations
    return [s for s in data['stations'] if s.get('is_active', False)]


def stations_match(geosphere_station, meteostat_station):
    """
    Check if two stations match based on the criteria:
    - Maximum distance of 100 meters
    - Maximum elevation difference of 20 meters
    - If names equal: max distance 1000m and max elevation diff 100m
    
    All criteria must be fulfilled for a match.
    
    Returns: (is_match, distance, elevation_diff)
    """
    # Calculate distance
    distance = get_distance(
        geosphere_station['lat'],
        geosphere_station['lon'],
        meteostat_station['location']['latitude'],
        meteostat_station['location']['longitude']
    )
    
    # Calculate elevation difference
    elevation_diff = abs(
        geosphere_station['altitude'] - meteostat_station['location']['elevation']
    )
    
    # Check if names match (case-insensitive comparison)
    geosphere_name = geosphere_station['name'].lower()
    meteostat_name = meteostat_station['name'].get('en', '').lower()
    names_match = geosphere_name == meteostat_name
    
    # Apply matching criteria
    if names_match:
        # If names match, allow larger tolerances
        is_match = distance <= 1000 and elevation_diff <= 100
    else:
        # Otherwise, use strict criteria
        is_match = distance <= 100 and elevation_diff <= 20
    
    return is_match, distance, elevation_diff


def find_match(geosphere_station, meteostat_stations):
    """
    Find a matching Meteostat station for a GeoSphere station
    
    Returns: (matched_station, is_exact, distance, elevation_diff) or (None, False, None, None)
    """
    for meteostat_station in meteostat_stations:
        is_match, distance, elevation_diff = stations_match(
            geosphere_station, meteostat_station
        )
        if is_match:
            return meteostat_station, True, distance, elevation_diff
    
    return None, False, None, None


def find_partial_match(geosphere_station, meteostat_stations):
    """
    Find a partial match (close but doesn't meet all criteria)
    
    Returns: list of (meteostat_station, distance, elevation_diff) tuples
    within reasonable proximity (e.g., distance < 5000m)
    """
    partial_matches = []
    
    for meteostat_station in meteostat_stations:
        distance = get_distance(
            geosphere_station['lat'],
            geosphere_station['lon'],
            meteostat_station['location']['latitude'],
            meteostat_station['location']['longitude']
        )
        
        elevation_diff = abs(
            geosphere_station['altitude'] - meteostat_station['location']['elevation']
        )
        
        # Check if it's a near miss (close but not exact match)
        if distance <= 5000 and elevation_diff <= 200:
            is_match, _, _ = stations_match(geosphere_station, meteostat_station)
            if not is_match:  # Only include if not an exact match
                partial_matches.append((meteostat_station, distance, elevation_diff))
    
    return partial_matches


def main():
    """
    Main import function
    """
    print("Fetching GeoSphere Austria stations...")
    geosphere_stations = fetch_geosphere_stations()
    print(f"Found {len(geosphere_stations)} active stations from GeoSphere Austria")
    
    print("Loading existing Austrian stations from Meteostat...")
    meteostat_stations = load_existing_austrian_stations()
    print(f"Found {len(meteostat_stations)} existing Austrian stations in Meteostat")
    
    updated_count = 0
    created_count = 0
    partial_matches_list = []
    matched_meteostat_ids = set()
    
    for geosphere_station in geosphere_stations:
        # Find matching Meteostat station
        matched_station, is_match, distance, elevation_diff = find_match(
            geosphere_station, meteostat_stations
        )
        
        if is_match and matched_station:
            # Update existing station
            print(f"Updating station {matched_station['id']} - {geosphere_station['name']}")
            
            update_data = {
                "id": matched_station['id'],
                "name": {"en": capwords(geosphere_station['name'])},
                "region": REGION_CODES.get(geosphere_station.get('state')),
                "location": {
                    "latitude": round(geosphere_station['lat'], 4),
                    "longitude": round(geosphere_station['lon'], 4),
                    "elevation": int(round(geosphere_station['altitude']))
                },
                "identifiers": {
                    "national": str(geosphere_station['id'])
                }
            }
            
            update(update_data)
            updated_count += 1
            matched_meteostat_ids.add(matched_station['id'])
        else:
            # Check for partial matches
            partial_matches = find_partial_match(geosphere_station, meteostat_stations)
            
            if partial_matches:
                # Log partial match for manual review
                partial_matches_list.append({
                    'geosphere': geosphere_station,
                    'meteostat_matches': partial_matches
                })
            else:
                # Create new station
                print(f"Creating new station for {geosphere_station['name']}")
                
                new_station_data = {
                    "id": generate_uid(),
                    "active": True,
                    "name": {"en": capwords(geosphere_station['name'])},
                    "country": "AT",
                    "region": REGION_CODES.get(geosphere_station.get('state')),
                    "identifiers": {
                        "national": str(geosphere_station['id'])
                    },
                    "location": {
                        "latitude": round(geosphere_station['lat'], 4),
                        "longitude": round(geosphere_station['lon'], 4),
                        "elevation": int(round(geosphere_station['altitude']))
                    },
                    "timezone": "Europe/Vienna"
                }
                
                create(new_station_data)
                created_count += 1
    
    print(f"\nSummary:")
    print(f"Updated: {updated_count} stations")
    print(f"Created: {created_count} new stations")
    print(f"Partial matches: {len(partial_matches_list)} stations")
    
    # Write partial matches to markdown file
    if partial_matches_list:
        with open(PARTIAL_MATCHES_FILE, 'w', encoding='utf-8') as f:
            f.write("# Partial Matches for Manual Review\n\n")
            f.write("The following GeoSphere Austria stations could not be automatically matched ")
            f.write("but have potential matches in Meteostat that require manual review.\n\n")
            
            for item in partial_matches_list:
                geosphere = item['geosphere']
                f.write(f"## GeoSphere Station: {geosphere['name']}\n\n")
                f.write(f"- **ID**: {geosphere['id']}\n")
                f.write(f"- **State**: {geosphere.get('state', 'N/A')}\n")
                f.write(f"- **Location**: {geosphere['lat']}, {geosphere['lon']}\n")
                f.write(f"- **Elevation**: {geosphere['altitude']}m\n\n")
                
                f.write("### Possible Meteostat Matches:\n\n")
                for meteostat_station, dist, elev_diff in item['meteostat_matches']:
                    f.write(f"- **{meteostat_station['id']}** - {meteostat_station['name'].get('en', 'N/A')}\n")
                    f.write(f"  - Distance: {dist:.0f}m\n")
                    f.write(f"  - Elevation difference: {elev_diff:.0f}m\n")
                    f.write(f"  - Location: {meteostat_station['location']['latitude']}, {meteostat_station['location']['longitude']}\n")
                    f.write(f"  - Elevation: {meteostat_station['location']['elevation']}m\n\n")
        
        print(f"Partial matches written to {PARTIAL_MATCHES_FILE}")


if __name__ == "__main__":
    main()
