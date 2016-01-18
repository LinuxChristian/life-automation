#!/usr/bin/env python
# roadConditions.py
# Copyleft (C) 2016 Christian Braedstrup
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
# This script scrapes current road conditions
# from trafikken.dk and returns an average 
# for a set of locations defined by param
#
# SETUP
#----------------
# Adjust the param variable to one or several of your
# locations. Read the blog post on www.fredborg-braedstrup.dk
# to find values.
#
# USAGE
# ---------------
#
# python3 roadCondtions.py <parameter>
#
# EXAMPLE
# --------------
# Compute the average current air temperature
#
# python3 roadCondtions.py air
#
# Possible parameters are air (air temperature) or 
# road (road surface temperature).
#
# NOTES
# --------------
# This script only works on Linux and Mac systems!
#
# 

import json
import sys
import os
import time
from urllib.request import urlopen

N = 10 # minutes
updatefile = False
outFile = '/tmp/temperatures.point.json'
trafikUrl = 'http://trafikkort.vejdirektoratet.dk/geojson/temperatures.point.json'

# Spare the trafikken.dk servers and only update
# once every N minutes
if os.path.isfile(outFile):
    mt = os.path.getmtime(outFile)

    # Update about every hour
    if (time.time() - mt)/(60) >= N:
        updatefile = True
else:
    updatefile = True

if True:
    # Get json from server
    try:
        with open(outFile, 'w') as f:
            response = urlopen(trafikUrl).read().decode('utf-8')
            data = json.loads(response)
            f.write(response)
    except:
        exit
else:
    # Get json from disk
    try:
        with open(outFile, 'r') as f:
            data = json.loads(f.read())
    except:
        exit

parsed_json = data 
#json.loads(open('/tmp/temperatures.point.json', 'r').read())

stations = {'Farum'           : {'id':5 , 'coor':[12.380186, 55.80534], 'air':0, 'road':0}, 
	    'Gladsaxe'        : {'id':25, 'coor':[12.455449, 55.73854], 'air':0, 'road':0},
	    'UtterslevMose_S' : {'id':63, 'coor':[12.49094, 55.71686] , 'air':0, 'road':0},
	    'UtterslevMose_N' : {'id':72, 'coor':[12.516491, 55.72286], 'air':0, 'road':0},
}

tempAir = []
meanAir = 0
tempRoad = []
meanRoad = 0

for i, s1 in enumerate(parsed_json['features']):
    for k2, s2 in list(stations.items()):
        if s1['geometry']['coordinates'] == s2['coor']:
            tempAir.append(int(s1['properties']['airTemperature']))
            tempRoad.append(int(s1['properties']['roadSurfaceTemperature']))
            s2['air'] = int(s1['properties']['airTemperature'])
            s2['road'] = int(s1['properties']['roadSurfaceTemperature'])

if len(sys.argv) > 1 and sys.argv[1] == "air":
	meanAir = sum(tempAir, 0.0)/len(tempAir)
	print("{:.2f}".format(meanAir))
elif sys.argv[1] == "road":
	meanRoad = sum(tempRoad, 0.0)/len(tempRoad)
	print("{:.2f}".format(meanRoad))
else:
	print("False")
