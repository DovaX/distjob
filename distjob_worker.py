"""
This file assigns jobs to available machines based on triggers
"""

import time

import sys
from distjob_context import djc

import datetime

print(datetime.datetime.now().timestamp()>datetime.datetime.now().timestamp())


def run():
    
    done=False
    
    i=0
    while not done:
        
        
        try:
            print("JOBS",djc.jobs)
            print(i)
            time.sleep(1)
            i+=1
            
            ready_jobs=[x for x in djc.jobs if x.start_datetime.timestamp()<=datetime.datetime.now().timestamp() and not x.is_assigned]
            if len(ready_jobs)>0:
                machine=djc.assign_job_to_idle_machine(ready_jobs[0])
                print(machine,ready_jobs[0])
            
            
            assigned_jobs=[x for x in djc.jobs if x.is_assigned]
            for i,job in enumerate(assigned_jobs):
                print("CHECKING JOB",job.uid)
                is_job_done=djc.check_if_job_done(job)
                if is_job_done:
                    matching_machine=[x for x in djc.machines if x.assigned_job==job][0]
                    matching_machine.processing_job=None
                    
            
                
            
            
            
            
            
            if i>50:
                done=True
                
        except (KeyboardInterrupt, SystemExit): #close thread on CTRL+C
            djc.ARE_ALL_THREADS_FINISHED=True
            sys.exit()