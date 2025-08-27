# flake8: noqa

from fastapi import FastAPI, Query,Path
from .connection import queue
from .worker import process_query

app = FastAPI()

@app.get("/")
def root():
    return {"status":"Server is up and running"}

@app.post("/chat")
def chat(query: str = Query(...,description = "chat Message")):
    job = queue.enqueue(process_query, query)
    return {"status" : "Queued" , "job_id" : job.id}



@app.get("/result/{job_id}")
def get_result(
    job_id: str = Path(..., description="Job Id")
):
    job = queue.fetch_job(job_id=job_id)
    result = job.return_value()
    return {"result": result}