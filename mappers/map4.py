#!/usr/bin/python

import sys

# input comes from STDIN (stream data that goes to the program)
for line in sys.stdin:
    l = line.strip().split(',')
    
    if len(l)>30:
  
        dist_lat = (float(l[7]) - float(l[11]))**2
        dist_lon = (float(l[8]) - float(l[12]))**2
        dist = (dist_lat + dist_lon)**0.5

        if l[31] == '1.0':
            rain = 'no'

        if l[30] == '1.0':
            rain = 'low'

        if l[29] == '1.0':
            rain = 'high'
  
        print "%s\t%.10f" % (rain, dist)
 

