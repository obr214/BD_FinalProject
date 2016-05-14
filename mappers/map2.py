#!/usr/bin/python

import sys

# input comes from STDIN (stream data that goes to the program)
for line in sys.stdin:
    l = line.strip().split(',')
    
    if len(l)>30:
  
        if l[14] == 'Subscriber':
            customer = 'sus'
        else:
            customer = 'cus'

        if l[31] == '1.0':
            rain = 'no'

        if l[30] == '1.0':
            rain = 'low'

        if l[29] == '1.0':
            rain = 'high'

        key = customer + rain
  
        print "%s\t%s" % (key, 1)
   

  

   
   
