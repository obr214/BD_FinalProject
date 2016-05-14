#!/usr/bin/python

import sys
import datetime

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

        start = datetime.datetime.strptime(l[3], '%Y-%m-%d %H:%M:%S')
        end = datetime.datetime.strptime(l[4], '%Y-%m-%d %H:%M:%S')
        weekday = start.weekday()
        
        if weekday<5:
     
            if (start.hour<10 and start.hour>7):
                period = 'morning'
            if (start.hour<20 and start.hour>17):
                period = 'afternoon'

            if period:
                print "%s\t%d" % ((rain, 'start', period, l[6]), 1)
           
            period = None

            if (end.hour<10 and end.hour>7):
                period = 'morning'
            if (end.hour<20 and end.hour>17):
                period = 'afternoon'

            if period:
                 print "%s\t%d" % ((rain, 'end', period, l[10]), 1)

            period = None




