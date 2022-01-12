import json
import time
from . import RedisService

QUEUED_JOB_LIST = "QUEUED_JOBS"
PRINTED_JOB_LIST = "PRINTED_JOBS"


def add_job_to_queue(filename: str, path: str):
    job = {
        "filename": filename,
        "path": path,
        "timestamp": int(time.time() * 1000)
    }
    strjob = json.dumps(job)
    RedisService.push_to_fifo(QUEUED_JOB_LIST, strjob)
    return job


def get_queued_jobs():
    strjobs = RedisService.get_list(QUEUED_JOB_LIST)
    jobs = list(map(json.loads, strjobs))
    return jobs
