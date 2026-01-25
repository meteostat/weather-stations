# Copilot Custom Instructions

## Project Context

This repository maintains a comprehensive list of public weather stations worldwide. The data is maintained by [Meteostat](https://meteostat.net) and includes meteorological station information in JSON format.

## Repository Structure

- `stations/`: Contains one JSON file per weather station, named after the station's Meteostat ID

## Data Structure & Formatting

### Weather Station JSON Files

Each weather station JSON file must include:

- `id`: Meteostat ID (String)
- `active`: Boolean indicating if station is active
- `name`: Object with names in different languages (at least "en")
- `country`: ISO 3166-1 alpha-2 country code (String)
- `region`: ISO 3166-2 state/region code (String or null)
- `identifiers`: Object with external IDs (wmo, icao, ghcn, usaf, mosmix, etc.)
- `location`: Object with:
  - `latitude`: Float
  - `longitude`: Float  
  - `elevation`: Integer (meters)
- `timezone`: Timezone string (e.g., "Europe/Oslo")

### Naming Conventions

- Weather station names are capitalized
- Use short and descriptive names
- Airports: Use "Airport" for aerodromes with air cargo/passengers
- Airfields: Use "Airfield" for aerodromes without commercial operations
- All files in `stations/` directory are named after the station's Meteostat ID with `.json` extension

### Important Notes

- Missing values are defined as `null`, not empty strings
- Only include optional properties (like identifier entries) if they have values
