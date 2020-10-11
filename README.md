# Weather Stations
A weather station is a location where meteorological data is measured. Most countries operate public weather station networks in order to monitor weather and climate. This repository provides a list of public weather stations everyone can contribute to. The data is maintained by the [Meteostat project](https://meteostat.net/en).

You can download the list of weather stations, including Meteostat inventory data, in JSON format:
* [**Full dump**](https://bulk.meteostat.net/stations/full.json.gz) with all weather stations
* [**Lite dump**](https://bulk.meteostat.net/stations/lite.json.gz) with weather stations which did report at least one observation to Meteostat

Additional information about the Meteostat bulk data interface is available in the [documentation](https://dev.meteostat.net/bulk).
## Data Structure
The `stations` directory contains one JSON file per weather station. The files are named after the station's Meteostat ID and hold one JSON object which describes the respective weather station.
### Properties
Each weather station must provide the following properties. Missing values are defined as `null`.
* `id`: The Meteostat ID of the weather station
* `name`: Object containing the name of the weather station in different languages
* `country`: ISO 3166-1 alpha-2 country code of the weather station (e.g. CA for Canada)
* `region`: The ISO 3166-2 state or region code of the weather station (e.g. TX for Texas)
* `identifiers`: Object containing different identifiers of the weather station
    * `national`: The national ID of the weather station
    * `wmo`: The WMO ID of the weather station
    * `ghcn`: The GHCN ID of the weather station
    * `wban`: The WBAN ID of the weather station
    * `usaf`: The USAF ID of the weather station
    * `mosmix`: The MOSMIX ID of the weather station
    * `icao`: The ICAO ID of the weather station
    * `iata`: The IATA ID of the weather station
* `location`: Object describing the location of the weather station
    * `latitude`: The latitude of the weather station
    * `longitude`: The longitude of the weather station
    * `elevation`: The elevation of the weather station in meters above sea level
* `timezone`: The time zone of the weather station
* `history`: An array that provides previous locations, identifiers or names of the weather station
## Formatting
* All files in the `stations` directory are named after the station's Meteostat ID.
* Names of weather stations are capitalized.
* Use short and descriptive names for a weather station.
* Many weather stations are located at aerodromes. When naming weather stations please refer to aerodromes, which involve air cargo or passengers, as *airports* and use the term *airfield* if they don't.
## Contributing
If you want to add a new weather station, update some information or correct an error, please either correct/update the affected file(s) & create a pull request or fill an issue & describe your concern. We will review each request and update the list accordingly. Once your changes are merged into the `master` branch they will be visible in all Meteostat products within a few days.
## Data License
The list of weather stations is available under the [Creative Commons Attribution 4.0 International Public License](https://creativecommons.org/licenses/by/4.0/legalcode).
