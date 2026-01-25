# GitHub Copilot Automation Prompts

This file contains GitHub Copilot prompts for automating various weather station maintenance tasks.

## Update Austrian Weather Stations

This prompt automates the process of updating and adding Austrian weather stations from GeoSphere Austria.

### Prompt for GitHub Copilot

```
Update Austrian weather stations from GeoSphere Austria API.

Data Source:
- API URL: https://dataset.api.hub.geosphere.at/v1/station/historical/klima-v2-1d/metadata
- Only include stations where is_active = true AND type = 'COMBINED'

Station Matching Criteria (ALL must be fulfilled):
1. For stations with different names:
   - Maximum distance: 100 meters
   - Maximum elevation difference: 20 meters
2. For stations with matching names (case-insensitive):
   - Maximum distance: 1000 meters
   - Maximum elevation difference: 100 meters

Distance calculation formula:
```python
import numpy as np

def get_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two points using Haversine formula"""
    radius = 6371000  # Earth radius in meters
    lat1, lon1, lat2, lon2 = map(np.deg2rad, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    arch = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    arch_sin = 2 * np.arcsin(np.sqrt(arch))
    return radius * arch_sin
```

Austrian State to ISO 3166-2 Region Code Mapping:
```python
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
```

Steps:
1. Fetch active COMBINED type stations from GeoSphere Austria API
2. Load existing Austrian stations (country = "AT") from the repository
3. For each GeoSphere station:
   a. Find matching Meteostat station based on criteria above
   b. If match found:
      - Update name.en from GeoSphere name (DO NOT alter casing or format)
      - Update latitude, longitude (rounded to 4 decimal places)
      - Update elevation (rounded to nearest integer)
      - Update region using REGION_CODES mapping
      - Set identifiers.national to GeoSphere station ID (as string)
   c. If no match but close (distance < 5000m, elevation diff < 200m):
      - Add to partial_matches.md for manual review
   d. If no match at all:
      - Create new station with:
        - Generated unique ID (5 random uppercase letters/digits)
        - active: true
        - country: "AT"
        - timezone: "Europe/Vienna"
        - All other fields from GeoSphere data (DO NOT alter name casing)

4. Generate partial_matches.md with:
   - GeoSphere station details
   - List of nearby Meteostat stations with distance and elevation difference
   - Include instructions to research additional information online or through applicable MCP servers

Output:
- Update existing station JSON files in stations/ directory
- Create new station JSON files in stations/ directory
- Generate scripts/austria/partial_matches.md
- Print summary of updates and new stations

For partial matches in the markdown file, instruct users to:
- Research station information online (Google Maps, Wikipedia, official sources)
- Use MCP servers if available to gather additional context
- Verify locations using satellite imagery
- Check official station databases for cross-references
```

### Example Usage

Ask GitHub Copilot:
> "Update Austrian weather stations following the process in AGENTS.md"

or simply:

> "Run the Austrian weather stations update"

### Notes

- The script should be idempotent - running it multiple times should not create duplicates
- All JSON files should use 4-space indentation
- Station names should be used as-is from GeoSphere (DO NOT alter casing)
- Only COMBINED type stations should be included
- The script should be saved in scripts/austria/import.py
