import requests
import json
import datetime 

class Job:
    instance_counter=0
    def __init__(self, url, data, priority, start_datetime, check_condition_request_url, method="POST"):
        self.url=url
        self.data=data
        self.priority=priority
        self.start_datetime=start_datetime
        self.check_condition_request_url=check_condition_request_url #should return True or False if job is done
        self.method=method
        self.is_assigned=False
        self.is_done=False
        
        self.__class__.instance_counter += 1
        self.uid = self.instance_counter
        


class Machine:
    instance_counter=0
    def __init__(self, host, port):
        self.host=host
        self.port=port
        self.processing_job=None
        
        self.__class__.instance_counter += 1
        self.uid = self.instance_counter
        
        
        


    


class DistJobContext:
    def __init__(self,host="0.0.0.0",port=10100):
        self.ARE_ALL_THREADS_FINISHED=False
        
        self.host=host
        self.port=port        
        
        
        self.jobs=[]
        self.machines=[]
        self.triggers=[]
        self.test_condition=False
        self.test_jobs_progress_dict={}
        
        #self.create_test_job()
        #self.create_test_job()
        #self.create_test_job()
        
    def create_test_job(self):
        data={"url": "test","data": {},"priority": 0,"start_datetime": "2023-01-01T12:00:00.000Z","check_condition_request_url": "/api/v1/test_condition","method": "POST"}
        self.jobs.append(Job("/api/v1/jobs",data,0,datetime.datetime.now(),"/api/v1/test_condition"))
        
    
    
    
        
    def process_test_job(self,job):
        print("TEST_PROGRESS",self.test_jobs_progress_dict)
        if job.uid in self.test_jobs_progress_dict:
            if self.test_jobs_progress_dict[job.uid]<10:
                
                self.test_jobs_progress_dict[job.uid]+=1
                self.test_condition=False
            else:
                job.is_done=True
                job.is_assigned=False  
                self.test_condition=True #len([x for x in self.jobs if x.is_done])==len(self.jobs) #True if all jobs done
                print("TEST CONDITION SET",self.test_condition)
        else:
            self.test_jobs_progress_dict[job.uid]=0
                     
            
        
    
        
        
        
    def assign_job_to_idle_machine(self,job):
        
        for i,machine in enumerate(self.machines):
            if machine.processing_job is None:
                if job.url=="test":
                    self.machines[i].processing_job=job
                    job.is_assigned=True
                    print("Machine",i,"was assigned")
                    return(self.machines[i])
                
                response=None
                url="http://"+machine.host+":"+str(machine.port)+job.url
                #job.data should be in dict format (json)
                print("URL",job.url)
                print("DATA",job.data,type(job.data))
                try:
                    if job.method=="POST":
                        response=requests.post(url,json.dumps(job.data))
                        result=json.loads(response.content)
                    elif job.method=="GET":
                        response=requests.post(job.url,json.dumps(job.data))
                        result=json.loads(response.content)
                    elif job.method=="DELETE":
                        response=requests.delete(job.url,json.dumps(job.data))
                        result=json.loads(response.content)
                    elif job.method=="PUT":
                        response=requests.put(job.url,json.dumps(job.data))
                        result=json.loads(response.content)
                
                
                    print("JOB ASSIGNMENT RESPONSE:",response)
                    if response is not None:
                        if response.status_code==200:
                            
                            self.machines[i].processing_job=job
                            job.is_assigned=True
                            print("Machine",i,"was assigned")
                            return(self.machines[i])
                        else:
                            print("Machine couldnt be assigned, wrong status code",response.status_code)
                            return(None)
                    
                except requests.exceptions.ConnectionError:
                    print("Connection error")
                
        print("No machine could be assigned")
        return(None)
    
    def unassign_job_from_machine(self,job):
        
        for i,machine in enumerate(self.machines):
            if machine.processing_job==job:
                self.machines[i].processing_job=None
                job.is_assigned=False
                print("Machine",machine.uid,"was unassigned")
                return(self.machines[i])
        print("No machine could be unassigned")
        return(None)
    
    
    
    def check_if_job_done(self, machine, job):
        
        is_running_locally_on_this_port=False
        if self.host.strip() in ["0.0.0.0","127.0.0.1"] and machine.host.strip() in ["0.0.0.0","127.0.0.1"]:
            is_running_locally_on_this_port=True
        if machine.host==self.host:
            is_running_locally_on_this_port=True
        
        
        if is_running_locally_on_this_port and machine.port==self.port: #if executed on this machine (e.g. test task), dont check test condition
            return(False)
        else:   
            url="http://"+machine.host+":"+str(machine.port)+job.check_condition_request_url
            print(url)
            response=requests.get(url=url)
            result=json.loads(response.content)
            print(result)
            is_job_done=result["condition"]
            print(job,"IS_JOB_DONE",is_job_done)
            
            if is_job_done:
                index=self.machines.index(machine)
                self.machines[index].processing_job=None
                job.is_assigned=False
                job.is_done=True
            
            return(result["condition"])
        
        
        
        
    
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



    def new_job(self, url, data, priority, start_datetime, check_condition_request_url):
        job=Job(url, data, priority, start_datetime, check_condition_request_url)
        
        self.jobs.append(job)
        return(job)
        
    
    def delete_job(self,job):
        index=self.jobs.index(job)
        self.jobs.pop(index)
        
     
        

    def update_job(self,job,url=None, data=None, priority=None, start_datetime=None, check_condition_request_url=None):
        index=self.jobs.index(job)
        if url is not None:
            self.jobs[index].url=url
        if data is not None:
            self.jobs[index].data=data
        if priority is not None:
            self.jobs[index].priority=priority
        if start_datetime is not None:
            self.jobs[index].start_datetime=start_datetime
        if check_condition_request_url is not None:
            self.jobs[index].check_condition_request_url=check_condition_request_url
            
       
        
    def update_job_by_uid(self,job_uid, url=None, data=None, priority=None, start_datetime=None, check_condition_request_url=None):
        job=self.get_job_by_uid(job_uid)
        try:
            self.update_job(job,url, data, priority, start_datetime, check_condition_request_url)
        except Exception as e:
            print(f"Job couldn't be updated: {e}")
        
    def delete_job_by_uid(self,job_uid):
        job=self.get_job_by_uid(job_uid)
        try:
            self.delete_job(job)
        except Exception as e:
            print(f"Job couldn't be deleted: {e}")
    
    
    
       
    
    ###### Machines #####

    def get_machine_by_uid(self,machine_uid):
        matching_machines=[machine for machine in self.machines if machine.uid==machine_uid]
        assert len(matching_machines)<=1
        if len(matching_machines)==1:
            return(matching_machines[0])
        elif len(matching_machines)==0:
            print("machine was not found, couldn't be deleted")
            return(None)
        else:
            print("Multiple machines with duplicate uid exist")
            return(None)



    def new_machine(self, host, port):
        machine=Machine(host, port)
        
        self.machines.append(machine)
        return(machine)
        
    
    def delete_machine(self,machine):
        index=self.machines.index(machine)
        self.machines.pop(index)
        
     
        

    def update_machine(self,machine,host=None, port=None):
        index=self.machines.index(machine)
        if host is not None:
            self.machines[index].host=host
        if port is not None:
            self.machines[index].port=port
       
        
    def update_machine_by_uid(self,machine_uid, host=None, port=None):
        machine=self.get_machine_by_uid(machine_uid)
        try:
            self.update_machine(machine, host, port)
        except Exception as e:
            print(f"machine couldn't be updated: {e}")
        
    def delete_machine_by_uid(self,machine_uid):
        machine=self.get_machine_by_uid(machine_uid)
        try:
            self.delete_machine(machine)
        except Exception as e:
            print(f"machine couldn't be deleted: {e}")
    
    
 
djc=DistJobContext()
