#!/usr/bin/python

import sys

# input comes from STDIN (stream data that goes to the program)
for line in sys.stdin:
    l = line.strip().split(',')
    
    if len(l)>30 and l[15]:

        if l[31] == '1.0':
            rain = 'no'

        if l[30] == '1.0':
            rain = 'low'

        if l[29] == '1.0':
            rain = 'high'
        
        temprature = int(float(l[27]))
        gender= l[16]
        wind=  int(float(l[21]))
  
        print "%s\t%d" % ([temprature,wind, gender], 1)

