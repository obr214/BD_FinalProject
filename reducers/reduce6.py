#!/usr/bin/python

import sys

current_key = None
current_sum = 0

# input comes from STDIN (stream data that goes to the program)
for line in sys.stdin:
    
    key, count = line.split("\t", 1)
    
    try:
        count = int(count)
    except ValueError:
        continue
 
    
    if key == current_key:
        current_sum += count
    else:
        if current_key:
            # output goes to STDOUT (stream data that the program writes)
            att = eval(str(current_key))
            print "%s\t%s\t%s\t%s\t%d" %( att[0], att[1], att[2], att[3], current_sum )
        current_key = key
        current_sum = count

att = eval(str(current_key))
print "%s\t%s\t%s\t%s\t%d" %( att[0], att[1], att[2], att[3], current_sum )
