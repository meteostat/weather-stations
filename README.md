# Weather Stations

A weather station is a location where meteorological data is measured. Most countries operate public weather station networks in order to monitor weather and climate. This repository provides a list of public weather stations everyone can contribute to. The data is maintained by [Meteostat](https://meteostat.net).

You can download the list of weather stations, including Meteostat inventory data, in JSON format:

* [**Full dump**](https://bulk.meteostat.net/v2/stations/full.json.gz) with all weather stations
* [**Lite dump**](https://bulk.meteostat.net/v2/stations/lite.json.gz) with active weather stations only

Additional information about the Meteostat bulk data interface is available in the [documentation](https://dev.meteostat.net/bulk).

## Data Structure

The `stations` directory contains one JSON file per weather station. The files are named after the station's Meteostat ID and hold one JSON object which describes the respective weather station.

### Properties

Each weather station must provide the following properties. Missing values are defined as `null`. The following properties are mandatory and must be present in a station file. Optional properties are prefixed with a `$` sign (e.g. `identifiers.$icao`).

* `id`: Meteostat ID (_String_)
* `name`: Name in different languages (_Object_)
* `country`: ISO 3166-1 alpha-2 country code, e.g. CA for Canada (_String_)
* `region`: ISO 3166-2 state or region code, e.g. TX for Texas (_String_)
* `identifiers`: Identifiers (_Object_)
* `location`: Geographic location (_Object_)
    * `latitude`: Latitude (_Float_)
    * `longitude`: Longitude (_Float_)
    * `elevation`: Elevation in meters (_Integer_)
* `timezone`: Time zone (_String_)

## Formatting

* All files in the `stations` directory are named after the station's Meteostat ID.
* Names of weather stations are capitalized.
* Use short and descriptive names for a weather station.
* Many weather stations are located at aerodromes. When naming weather stations please refer to aerodromes, which involve air cargo or passengers, as *airports* and use the term *airfield* if they don't.
* Prefix optional properties with a `$` sign.

## Contributing

If you want to add a new weather station, update some information or correct an error, please either correct/update the affected file(s) & create a pull request or fill an issue & describe your concern. We will review each request and update the list accordingly. Once your changes are merged into the `master` branch they will be visible in all Meteostat products within a few days.

## Data License

The list of weather stations is available under the [Creative Commons Attribution 4.0 International Public License](https://creativecommons.org/licenses/by/4.0/legalcode).
