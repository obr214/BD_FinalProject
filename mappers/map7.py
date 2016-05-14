#!/usr/bin/python

import sys
import datetime

# input comes from STDIN (stream data that goes to the program)
for line in sys.stdin:
    l = line.strip().split(',')
    
    if l[6]=='Penn Station Valet' or l[10]== 'Penn Station Valet':
	print line
    else:
	pass


        
   
