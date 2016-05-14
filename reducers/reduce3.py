#!/usr/bin/python

import sys

current_key = None
current_sum = 0
current_count = 0 

# input comes from STDIN (stream data that goes to the program)
for line in sys.stdin:
    
    key, tripduration = line.split("\t", 1)
    
    try:
        tripduration = int(tripduration)
    except ValueError:
        continue
 
    
    if key == current_key:
        current_sum += tripduration
        current_count += 1
    else:
        if current_key:
            # output goes to STDOUT (stream data that the program writes)
            avg = current_sum/current_count
            print "%s\t%d" %( current_key, avg )
        current_key = key
        current_sum = tripduration
        current_count = 1

avg = current_sum/current_count
print "%s\t%d" %( current_key, avg )

