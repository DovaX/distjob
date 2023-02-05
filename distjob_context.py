
class Job:
    def __init__(self, function, function_args, priority, start_datetime):
        self.function=function
        self.function_args=function_args
        self.priority=priority
        self.start_datetime=start_datetime



class Machine:
    def __init__(self, host, port):
        pass
    



class DistJobContext:
    def __init__(self):
        self.ARE_ALL_THREADS_FINISHED=False
        
        
        self.jobs=[]
        self.machines=[]
        self.triggers=[]
        
        
    
    ###### Jobs #####

    def get_job_by_uid(self,job_uid):
        matching_jobs=[job for job in self.jobs if job.uid==job_uid]
        assert len(matching_jobs)<=1
        if len(matching_jobs)==1:
            return(matching_jobs[0])
        elif len(matching_jobs)==0:
            print("Job was not found, couldn't be deleted")
            return(None)
        else:
            print("Multiple jobs with duplicate uid exist")
            return(None)



    def new_job(self, function, function_args, priority, start_datetime):
        job=Job(function, function_args, priority, start_datetime)
        
        self.jobs.append(job)
        return(job)
        
    
    def delete_job(self,job):
        index=self.jobs.index(job)
        self.jobs.pop(index)
        
     
        

    def update_job(self,job,function=None, function_args=None, priority=None, start_datetime=None):
        index=self.jobs.index(job)
        if function is not None:
            self.jobs[index].function=function
        if function_args is not None:
            self.jobs[index].function_args=function_args
        if priority is not None:
            self.jobs[index].priority=priority
        if start_datetime is not None:
            self.jobs[index].start_datetime=start_datetime
       
        
    def update_job_by_uid(self,job_uid, function=None, function_args=None, priority=None, start_datetime=None):
        job=self.get_job_by_uid(job_uid)
        try:
            self.update_job(job,function, function_args, priority, start_datetime)
        except Exception as e:
            print(f"Job couldn't be updated: {e}")
        
    def delete_job_by_uid(self,job_uid):
        job=self.get_job_by_uid(job_uid)
        try:
            self.delete_job(job)
        except Exception as e:
            print(f"Job couldn't be deleted: {e}")
    
    
 
djc=DistJobContext()
