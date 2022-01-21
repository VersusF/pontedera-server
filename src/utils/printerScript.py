import os
import json
from services import RedisService, WorkerService
from utils.config import PRINTED_JOB_LIST, QUEUED_JOB_LIST

REMOTE_FOLDER = os.getenv("PRINTER_REMOTE_FOLDER")


def send_and_print(filename: str, copies: int):
    """
    Send file to remote host and invoke print command
    """
    local_file_path = "./tmp/" + filename
    WorkerService.transfer_file(local_file_path, REMOTE_FOLDER)
    os.remove(local_file_path)
    print_cmd = "lp -n {} {}".format(copies, REMOTE_FOLDER + filename)
    WorkerService.run_command(print_cmd)


if __name__ == "__main__":
    strjob = RedisService.pop_from_fifo(QUEUED_JOB_LIST)
    if strjob is not None:
        WorkerService.request_worker()
    while strjob is not None:
        job = json.loads(strjob)
        send_and_print(job["filename"], job["copies"])
        RedisService.push_to_fifo(PRINTED_JOB_LIST, strjob)
        print("Printed", job["filename"], "with", job["copies"], "copies")
        strjob = RedisService.pop_from_fifo(QUEUED_JOB_LIST)
    WorkerService.release_worker()
