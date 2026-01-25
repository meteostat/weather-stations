# Copilot Custom Instructions

## Project Context

This is a Python-based repository that maintains a comprehensive list of public weather stations worldwide. The data is maintained by [Meteostat](https://meteostat.net) and includes meteorological station information in JSON format.

### Repository Structure
- `stations/`: Contains one JSON file per weather station, named after the station's Meteostat ID
- `lib/`: Python library with helper functions (checks, generators, mutations, utils)
- `scripts/`: Utility scripts for data processing and validation
- `database.py`: Converts JSON files to SQLite database
- `tables.sql`: Database schema definitions

## Guidelines

### Code Style
- Follow PEP 8 Python style guidelines
- Use pylint for code quality checks (configuration in `.pylintrc`)
- Allowed good names: `f`, `df`, `uid`
- Type hints are encouraged for function parameters and returns

### Data Structure & Formatting

#### Weather Station JSON Files
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

#### Naming Conventions
- Weather station names are capitalized
- Use short and descriptive names
- Airports: Use "Airport" for aerodromes with air cargo/passengers
- Airfields: Use "Airfield" for aerodromes without commercial operations
- All files in `stations/` directory are named after the station's Meteostat ID with `.json` extension

### Testing & Validation
- Run `python database.py` to test JSON to SQLite conversion
- Use `scripts/qa_check.py` for quality assurance checks
- Validate JSON syntax and structure before creating pull requests
- Check for duplicate stations using the `lib/checks.py` helpers

### Dependencies
- Python 3.5+
- Core dependencies: `mysql-to-sqlite3`, `pandas`
- Package dependencies: `meteostat==1.5.7`
- Install via: `pip install -r requirements.txt`

## Contribution Workflow
1. Validate JSON structure matches the data format specifications
2. Run linter: `pylint <file>` for Python code changes
3. Test database conversion if modifying station files: `python database.py`
4. Run QA checks: `python scripts/qa_check.py`
5. Ensure station data follows naming conventions and formatting rules

## Data License
The weather station data is licensed under Creative Commons Attribution 4.0 International Public License (CC BY 4.0).

## Important Notes
- Missing values are defined as `null`, not empty strings
- Only include optional properties (like identifier entries) if they have values
- Do not modify the database schema without careful consideration
- Inactive stations (active: false) are skipped during database conversion
