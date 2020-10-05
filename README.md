# Weather Stations
A weather station is a location where meteorological data is measured. Most countries operate public weather station networks in order to monitor weather and climate. This repository provides a list of public weather stations everyone can contribute to. The data is maintained by the Meteostat project.
## Data Structure
The `stations` directory contains one JSON file per weather station. The files are named after the station's Meteostat ID and hold one JSON object which describes the respective weather station.
### Properties
* `id`: The Meteostat ID of the weather station
* `name`: Object containing the name of the weather stations in different languages
* `country`: ISO 3166-1 alpha-2 country code of the weather station
* `region`: The state or region of the weather station
* `national`: The national ID of the weather station
* `wmo`: The WMO ID of the weather station
* `ghcn`: The GHCN ID of the weather station
* `wban`: The WBAN ID of the weather station
* `usaf`: The USAF ID of the weather station
* `mosmix`: The MOSMIX ID of the weather station
* `icao`: The ICAO ID of the weather station
* `iata`: The IATA ID of the weather station
* `latitude`: The latitude of the weather station
* `longitude`: The longitude of the weather station
* `elevation`: The elevation of the weather station in meters above sea level
* `timezone`: The time zone of the weather station
## Contributing
If you want to add a new weather station, update some information or correct an error, please either correct/update the affected file(s) & create a pull request or fill an issue & describe your concern. We will review each request and update the list accordingly. Once your changes are merged into the `master` branch they will be visible in all Meteostat products within 24 hours.
## Data License
The list of weather stations is available under the [Creative Commons Attribution 4.0 International Public License](https://creativecommons.org/licenses/by/4.0/legalcode).
