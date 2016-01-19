# A collection of python scripts

Note: Only tested on Linux and Mac OS X.

## DMI forecast
Computes the average of a user defined parameter forecasted by the Danish Metrological 
Institut (DMI) over a given interval,

```
python dmi_forecast.py <start> <end> <parameter>
```

i.e. compute the average forecasted wind speed between 15:00 and 16:59,

```
python dmi_forecast.py 15 17 wind_speed
```

Possible parameters are temp, wind_speed, precip and wind_gust.

##  Road conditions
Get current road conditions from trafikken.dk.
First edit the param variable

```
python3 roadCondtions.py <parameter>
```

Possible parameters are air (air temperature) or road (road surface temperature). 

This script works great with [Home Assistant](https://www.home-assistant.io). 
Just add the following sensors to your configuration.yaml,

```
sensor #:
  platform: command_sensor
  name: Bike air temperature
  command: "python3 <PATH TO SCRIPT>/roadConditions.py air"
  unit_of_measurement: "\u2103"

sensor #:
  platform: command_sensor
  name: Bike air temperature
  command: "python3 <PATH TO SCRIPT>/roadConditions.py air"
  unit_of_measurement: "\u2103"
```
