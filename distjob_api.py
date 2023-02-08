from typing import Optional, Any, List, Dict, Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel


from distjob_context import djc


import uvicorn

import datetime

description = """
This API helps you to distribute jobs among many machines via API requests. 🚀
"""


tags_metadata=[
    {"name": "Get Methods", "description": ""},
    {"name": "Post Methods", "description": ""},
    {"name": "Delete Methods", "description": ""},
    {"name": "Put Methods", "description": ""},
]

app = FastAPI(title="Distjob API",
    description=description,
    version="1.0.0",
    openapi_tags=tags_metadata
    )

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
import json

class APIJob(BaseModel):
    url:Any="/api/v1/jobs"
    data:Any='{"url": "test","data": {},"priority": 0,"start_datetime": "2023-01-01T12:00:00.000Z","check_condition_request_url": "/api/v1/test_condition","method": "POST"}'
    priority:int
    start_datetime:datetime.datetime
    check_condition_request_url:str="/api/v1/test_condition"
    method:str="POST"
    
    
class APIMachine(BaseModel):
    host:str="127.0.0.1"
    port:int=10100  
    
    
    
    
    
    
    
    
    
    
 
import datetime

@app.get("/api/v1/jobs")
def get_jobs():
    """
    Returns all jobs in a given server
    """
    return {"jobs": djc.jobs}


@app.get("/api/v1/job/{uid}")
def get_job(uid: Optional[int]=None):
    """
    uid: unique id of a job is required
    """
    matching_jobs=[x for x in djc.jobs if x.uid==uid]
    if len(matching_jobs)==1:
        job=matching_jobs[0]
        return {
            "uid":job.uid,
            "url":job.url,
            "data":job.data,
            "priority":job.priority,
            "start_datetime":job.start_datetime,
            "check_condition_request_url":job.check_condition_request_url,
            "method":job.method
            }
    else:
        return {"ok":False}
        
  
@app.post("/api/v1/jobs")
def new_job(job : APIJob):
    job=djc.new_job(job.url,job.data,job.priority,job.start_datetime,job.check_condition_request_url)
    return {
        "uid":job.uid,
        "url":job.url,
        "data":job.data,
        "priority":job.priority,
        "start_datetime":job.start_datetime,
        "check_condition_request_url":job.check_condition_request_url,
        "method":job.method
        }

@app.delete("/api/v1/job/{uid}")
def delete_job(uid: Optional[int]=None):  
    djc.delete_job_by_uid(uid)  
    return {"ok":True}

@app.delete("/api/v1/jobs")
def delete_jobs():  
    djc.jobs=[]
    return {"ok":True}

@app.put("/api/v1/job/{uid}")
def update_job(uid: Optional[int]=None, job:APIJob=None):
    djc.update_job_by_uid(uid, job.url,job.data,job.priority,job.start_datetime,job.check_condition_request_url)  
    return {"ok":True}



@app.get("/api/v1/machines")
def get_machines():
    """
    Returns all machines in a given server
    """
    return {"machines": djc.machines}


@app.get("/api/v1/machine/{uid}")
def get_machine(uid: Optional[int]=None):
    """
    uid: unique id of a machine is required
    """
    matching_machines=[x for x in djc.machines if x.uid==uid]
    if len(matching_machines)==1:
        machine=matching_machines[0]
        return {
            "uid":machine.uid,
            "host":machine.host,
            "port":machine.port,
            }
    else:
        return {"ok":False}
        
  
@app.post("/api/v1/machines")
def new_machine(machine : APIMachine):
    machine=djc.new_machine(machine.host,machine.port)
    return {
        "uid":machine.uid,
        "host":machine.host,
        "port":machine.port,
        }

@app.delete("/api/v1/machine/{uid}")
def delete_machine(uid: Optional[int]=None):  
    djc.delete_machine_by_uid(uid)  
    return {"ok":True}

@app.delete("/api/v1/machines")
def delete_machines():  
    djc.machines=[]
    return {"ok":True}

@app.put("/api/v1/machine/{uid}")
def update_machine(uid: Optional[int]=None, machine:APIMachine=None):
    djc.update_machine_by_uid(uid, machine.host,machine.port)  
    return {"ok":True}


@app.get("/api/v1/test_condition")
def test_condition():
    """
    Returns sample test condition
    """
    print("TEST_CONDITION",djc.test_condition)
    if djc.test_condition: #return True just once - turn off on get request
        djc.test_condition=False
        return {"condition": True}
    else:
        return {"condition": False}




def run_api():
    uvicorn.run(app, host=djc.host, port=djc.port)

if __name__=="__main__":
    run_api()