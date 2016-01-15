# A collection of python scripts
1;95;0c
## DMI forcast
Computes the average parameter of an user defined interval,

```
python3 dmi_forcast.py <start> <end> <parameter>
```

i.e. compute the average forcasted wind speed between 15:00 and 17:59,

```
python3 dmi_forcast.py 15 17 wind_speed
```

Possible parameters are temp, wind_speed, precip and wind_gust.