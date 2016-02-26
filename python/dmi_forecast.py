# dmi_forcast.py
# Copyleft (C) 2016 Christian Brædstrup
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

#
# DESCRIPTION
# ---------------
# This script scrapes current forcast information
# from the Danish Metrological Institute (DMI)
# and allows the user to specify a time interval
# to compute average parameters.
#
# SETUP
#----------------
# Adjust the param variable to one or several of your local forcast
# locations. This involves changing the station name as needed (can be anything)
# and the ID variable which should be 4500+<zipcode> (i.e. for 45008900 for Randers C)
#
# USAGE
# ---------------
#
# python3 dmi_forcast.py <Start time> <Stop time> <parameter>
#
# EXAMPLE
# --------------
# Compute the average temperature on your commute to work
# for the interval 6 - 9 AM
#
# python3 dmi_forcast.py 6 9 temp
#
# Possible parameters are temp, wind_speed, precip and wind_gust.
#
# If the current time is after the start time, but before the end time,
# the average will be from current time until end time. Otherwise the next
# possible time fitting the interval will be used (either on the current day or
# the next day).
#
# NOTES
# --------------
# This script only works on Linux and Mac systems!
#
# Forcasts are only updated every hour. To spare the DMI servers station information is saved
# to the /tmp folder. If the file is older than 1 hour it is updated.
#
# It is not possible to compute averages across day boundaries (i.e. from 23 - 03).
# 

import json
try:
    from requests import get
except ImportError:
    raise ImportError("Could not load requests library.")

import sys, os
import time

def comidx(ct, st, et):
    '''
    This function converts a current time (ct) in 24 hour
    format into the index for the start time (st) or end time (et)
    depending on the current time
    '''

    nextDay = False
    if et - ct < 0:
        # The end time is not today
        # Then pull the first interval for tommorow
        nextDay = True
        idx = int(st)
        
    elif (st - ct < 0) and (et - ct >= 0):
        # We are currently between the start and end time
        idx = int(0)
    else:
        # The start time is today
        idx = int(st - ct)

    return idx, nextDay

dmiUrl = 'http://www.dmi.dk/Data4DmiDk/getData'

#
# Params - Set before usage
# 
params     = {'dyssegaard' : {'by_hour':'true', 'id':'45002870', 'country':'DK'},
              'farum'      : {'by_hour':'true', 'id':'45003520', 'country':'DK'},
              'soborg'     : {'by_hour':'true', 'id':'45002860', 'country':'DK'},
              'bagsvaerd'  : {'by_hour':'true', 'id':'45002880', 'country':'DK'}
              }

if len(sys.argv) < 3:
    print("Please supply a start time, end time and variable to measure")
    exit()

s = sys.argv[1] # Start time
e = sys.argv[2] # End time
v = sys.argv[3] # Variable name

if s.isdigit() is False or int(s) < 0 or int(s) > 24:
    print('The start time is not formatted correctly')
    print(s)
    print('type {}'.format(type(s)))
    print('isdigit {}'.format(s.isdigit()))
    exit()

s = int(s)

if e.isdigit() is False or int(e) < 0 or int(e) > 24:
    print('The end time is not formatted correctly')
    print(e)
    print('type {}'.format(type(e)))
    print('isdigit {}'.format(e.isdigit()))
    exit()

e = int(e)

if s > e:
    print('The start time is after the end time!')
    print('The code does not support intervals beyound the 24 hour mark!')
    exit()
    
if type(v) != str or  (v != 'precip' and v != 'wind_speed' and v != 'temp' and v != 'wind_gust'):
    print('The variable name is not formatted correctly')
    print('Possible values are: temp, wind_speed, precip, wind_gust')
    print(v)
    print('type {}'.format(type(v)))
    print('isdigit {}'.format(v.isdigit()))    
    exit()

# Data variables
commuteweather = {'start'    : s,  # Morning commute starts 6 AM
                  'stop'     : e,  # And lasts until 9 AM (excluded)
                  'var'      : 0.0
}

# Example
# cummteweather = {'afternoon': {'start'    : 15, # Afternoon commute starts 3 PM
#                                'stop'     : 18, # And lasts until 6 PM (excluded)
#                                'temp'     : 0.0 # Temperature
#                                }}

for place, p in list(params.items()):

    # Spare the DMI servers and only update
    # once a hour
    updatefile = False
    data = None
    if os.path.isfile('/tmp/%s.json' % place):
        mt = os.path.getmtime('/tmp/%s.json' % place)

        # Update about every hour
        if (time.time() - mt)/(60*60) >= 0.9:
            updatefile = True
    else:
        print('File does not exist')
        updatefile = True

    if updatefile:
        # Get json from DMI
        with open(('/tmp/%s.json' % place), 'w') as f:
            response = get(dmiUrl, p)
            data = response.json()
            f.write(str(response.text))
        if data is None:
            raise IOError("Unable to read from DMI and store to disk.")
    else:
        # Get json from disk
        with open(('/tmp/%s.json' % place), 'r') as f:
            data = json.loads(f.read())
        if data is None:
            raise IOError("Unable to read data from disk.")

    forcast = data['weather_data']['day1'] # Get forcast for today
    currenttime = 24-len(forcast)          # 24 hourly forcast pr. day (00 - 23)
    idx, nextday = comidx(currenttime,
                          commuteweather['start'],
                          commuteweather['stop'])   # Compute index

    interval    = commuteweather['stop'] - commuteweather['start'] # Compute lenght of interval
    if commuteweather['start'] - currenttime < 0 and currenttime < commuteweather['stop']:
        interval    = commuteweather['stop'] - currenttime # Compute lenght of interval
    
    if nextday is True:
        forcast = data['weather_data']['day2']

    for i in range(idx,idx+interval):
        if v == 'precip':
            commuteweather['var'] += float(forcast[i][v].replace(',', '.'))
        else:
            commuteweather['var'] += forcast[i][v]

commuteweather['var'] /= (interval+len(params))
print(commuteweather)
