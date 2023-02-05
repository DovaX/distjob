import requests
import json

class Job:
    instance_counter=0
    def __init__(self, function, function_args, priority, start_datetime, check_condition_request_url):
        self.function=function
        self.function_args=function_args
        self.priority=priority
        self.start_datetime=start_datetime
        self.check_condition_request_url=check_condition_request_url #should return True or False if job is done
        self.is_assigned=False
        
        self.__class__.instance_counter += 1
        self.uid = self.instance_counter
        


class Machine:
    def __init__(self, host, port):
        self.host=host
        self.port=port
        self.processing_job=None
        
        
        


    


class DistJobContext:
    def __init__(self):
        self.ARE_ALL_THREADS_FINISHED=False
        
        
        self.jobs=[]
        self.machines=[Machine("0.0.0.0",10101),Machine("0.0.0.0",10102)]
        self.triggers=[]
        
        
        
        
    def assign_job_to_idle_machine(self,job):
        
        for i,machine in enumerate(self.machines):
            if machine.processing_job is None:
                self.machines[i].processing_job=job
                job.is_assigned=True
                print("Machine",i,"was assigned")
                return(self.machines[i])
        print("No machine could be assigned")
        return(None)
    
    def check_if_job_done(self, job):
        response=requests.get(url=job.check_condition_request_url)
        result=json.loads(response.content)
        print(result)
        
        
        
        
    
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



    def new_job(self, function, function_args, priority, start_datetime, check_condition_request_url):
        job=Job(function, function_args, priority, start_datetime, check_condition_request_url)
        
        self.jobs.append(job)
        return(job)
        
    
    def delete_job(self,job):
        index=self.jobs.index(job)
        self.jobs.pop(index)
        
     
        

    def update_job(self,job,function=None, function_args=None, priority=None, start_datetime=None, check_condition_request_url=None):
        index=self.jobs.index(job)
        if function is not None:
            self.jobs[index].function=function
        if function_args is not None:
            self.jobs[index].function_args=function_args
        if priority is not None:
            self.jobs[index].priority=priority
        if start_datetime is not None:
            self.jobs[index].start_datetime=start_datetime
        if check_condition_request_url is not None:
            self.jobs[index].check_condition_request_url=check_condition_request_url
            
       
        
    def update_job_by_uid(self,job_uid, function=None, function_args=None, priority=None, start_datetime=None, check_condition_request_url=None):
        job=self.get_job_by_uid(job_uid)
        try:
            self.update_job(job,function, function_args, priority, start_datetime, check_condition_request_url)
        except Exception as e:
            print(f"Job couldn't be updated: {e}")
        
    def delete_job_by_uid(self,job_uid):
        job=self.get_job_by_uid(job_uid)
        try:
            self.delete_job(job)
        except Exception as e:
            print(f"Job couldn't be deleted: {e}")
    
    
 
djc=DistJobContext()
