import numpy as np
import json
import requests
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

# Params
params     = {'dyssegaard' : {'by_hour':'true', 'id':'45002870', 'country':'DK'},
              'farum'     : {'by_hour':'true', 'id':'45003520', 'country':'DK'},
              'soborg'    : {'by_hour':'true', 'id':'45002860', 'country':'DK'},
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

#for timeofday, weather in list(commuteweather.items()):
for place, p in params.iteritems():

    # Spare the DMI servers and only update
    # once a hour
    updatefile = False
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
        try:
            with open(('/tmp/%s.json' % place), 'w') as f:
                response = requests.get(dmiUrl, p)
                data = json.loads(response.text.encode('utf8'))
                f.write(response.text.encode('utf8'))
#                print('Saving file %s' % place)
        except:
            exit
    else:
        # Get json from disk
        try:
            with open(('/tmp/%s.json' % place), 'r') as f:
                data = json.loads(f.read())
        except:
            exit

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
#        print(forcast[i]['time_text'])
        if v == 'precip':
            commuteweather['var'] += float(forcast[i][v].replace(',', '.'))
        else:
            commuteweather['var'] += forcast[i][v]

commuteweather['var'] /= (interval+len(params))
print(commuteweather)
