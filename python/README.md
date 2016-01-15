# A collection of python scripts

Note: Only tested on Linux and Mac OS X.

## DMI forecast
Computes the average of a user defined parameter forecasted by the Danish Metrological 
Institut (DMI) over a given interval,

```
python3 dmi_forecast.py <start> <end> <parameter>
```

i.e. compute the average forecasted wind speed between 15:00 and 16:59,

```
python3 dmi_forecast.py 15 17 wind_speed
```

Possible parameters are temp, wind_speed, precip and wind_gust.
