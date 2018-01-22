# Home Assistant Cracow Air quality sensor

Fetch information about air quality from http://monitoring.krakow.pios.gov.pl/
Each metric will receive its own sensor that will be update every 30 minutes

# Installation

Copy `sensor/cracow_air_quality.py` to `<config>/custom_components/` directory. Then add this to your configuration.yaml

``` YAML
sensor:
  - platform: cracow_air_quality
    station_id: 7 # where is id of station 
    name: 'nowa_huta' # prefix for name of the sensor
```

Now you see this sensors:

- sensor.nowa_huta_bzn
- sensor.nowa_huta_co
- sensor.nowa_huta_no
- sensor.nowa_huta_no2
- sensor.nowa_huta_nox
- sensor.nowa_huta_pm10
- sensor.nowa_huta_pm25
- sensor.nowa_huta_so2