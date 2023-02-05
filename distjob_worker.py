"""
This file assigns jobs to available machines based on triggers
"""

import time

import sys
from distjob_context import djc






def run():
    
    done=False
    
    i=0
    while not done:
        
        
        try:
            print("JOBS",djc.jobs)
            print(i)
            time.sleep(1)
            i+=1
            
            if i>50:
                done=True
                
        except (KeyboardInterrupt, SystemExit): #close thread on CTRL+C
            djc.ARE_ALL_THREADS_FINISHED=True
            sys.exit()