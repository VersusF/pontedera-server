import json
import time
import os
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from . import RedisService
from utils.config import PRINTED_JOB_LIST, QUEUED_JOB_LIST


def add_job_to_queue(file: FileStorage, copies: int):
    if not os.path.isdir("./tmp"):
        print("Creating tmp folder")
        os.mkdir("./tmp")
    print(os.system("pwd"))
    filename = secure_filename(file.filename)
    path = "./tmp/" + filename
    file.save(path)
    job = {
        "filename": file.filename,
        "path": path,
        "copies": copies,
        "timestamp": int(time.time() * 1000)
    }
    strjob = json.dumps(job)
    RedisService.push_to_fifo(QUEUED_JOB_LIST, strjob)
    return job


def get_queued_jobs():
    strjobs = RedisService.get_list(QUEUED_JOB_LIST)
    jobs = list(map(json.loads, strjobs))
    return jobs


def get_printed_jobs():
    strjobs = RedisService.get_list(PRINTED_JOB_LIST)
    jobs = list(map(json.loads, strjobs))
    return jobs
