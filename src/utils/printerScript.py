import os
import time
import json
from services import RedisService
from utils.config import PRINTED_JOB_LIST, QUEUED_JOB_LIST

CUPS_IP = os.getenv("CUPS_IP")
COD_MAC = os.getenv("COD_MAC")
REMOTE_FOLDER = os.getenv("PRINTER_REMOTE_FOLDER")


def startup_and_wait():
    """
    Launch wake on lan command to wake up print server and wait for it to be up and running
    """
    os.system('wakeonlan {} > /dev/null'.format(COD_MAC))
    ping_command = 'timeout 0.2s ping {} -c 1 > /dev/null'.format(CUPS_IP)
    while not os.system(ping_command) == 0:
        time.sleep(5)


def send_and_print(filename: str, copies: int):
    local_file_path = "../tmp/" + filename
    copy_cmd = "scp {} cod@{}:{} > /dev/null".format(local_file_path, CUPS_IP, REMOTE_FOLDER)
    os.system(copy_cmd)
    os.remove(local_file_path)
    remote_print_cmd = "ssh cod@{} 'lp -n {} {}' > /dev/null".format(CUPS_IP, copies, REMOTE_FOLDER + filename)
    os.system(remote_print_cmd)


if __name__ == "__main__":
    strjob = RedisService.pop_from_fifo(QUEUED_JOB_LIST)
    if strjob is not None:
        startup_and_wait()
    while job is not None:
        job = json.loads(strjob)
        send_and_print(job["filename"], job["copies"])
        RedisService.push_to_fifo(PRINTED_JOB_LIST, job)
        print("Printed", job["filename"], "with", job["copies"], "copies")
        strjob = RedisService.pop_from_fifo(QUEUED_JOB_LIST)
