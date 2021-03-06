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

**Note: You need to set the locations to use for computing forecasted values in the python script!** Read the file header for more information.

### Integrate DMI Forecast into home assistant
Using the commandline sensor component you can get forecasted values directly into your HASS. Just add the sensors like so,

```
sensor:
  platform: command_sensor
  name: Temperature morning forecast
  command: "python3 /home/christian/life-automation/python/dmi_forecast.py 7 9 temp"
  unit_of_measurement: "\u2103"
  scan_interval: 3600

sensor 1:
  platform: command_sensor
  name: Windspeed morning forecast
  command: "python3 /home/christian/life-automation/python/dmi_forecast.py 7 9 wind_speed"
  unit_of_measurement: "m/s"
  scan_interval: 3600

sensor 2:
  platform: command_sensor
  name: Precipitation morning forecast
  command: "python3 /home/christian/life-automation/python/dmi_forecast.py 7 9 precip"
  unit_of_measurement: "mm"
  scan_interval: 3600
```

If you group then together you will get something like this,

![DMI forecast](http://fredborg-braedstrup.dk/images/HASS_forecast.png)

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
  name: Bike road surface temperature
  command: "python3 <PATH TO SCRIPT>/roadConditions.py road"
  unit_of_measurement: "\u2103"
```
