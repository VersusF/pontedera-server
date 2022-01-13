import os
import json
import time
from services import RedisService

SERVER_LOCAL_IP = '192.168.178.69'
COD_MAC = os.environ.get("COD_MAC")
REMOTE_FOLDER = "/home/cod/to_print/"
QUEUED_JOB_LIST = "QUEUED_JOBS"
PRINTED_JOB_LIST = "PRINTED_JOBS"


def wake_on_lan():
    """
    Launch wake on lan command to wake up print server
    """
    # Lanciare pacchetto
    os.system('wakeonlan {} > /dev/null'.format(COD_MAC))


def is_server_on():
    """
    Ping server to determine if is up
    """
    command = 'timeout 0.2s ping {} -c 1 > /dev/null'.format(SERVER_LOCAL_IP)
    return True if os.system(command) == 0 else False


def send_and_print(filename: str, n_copies):
    local_file_path = "../tmp/" + filename
    copy = "scp {} cod@{}:{} > /dev/null".format(local_file_path, SERVER_LOCAL_IP, REMOTE_FOLDER)
    os.system(copy)
    os.remove(local_file_path)
    remote_print = "ssh cod@{} 'lp -n {} {}' > /dev/null".format(SERVER_LOCAL_IP, n_copies, REMOTE_FOLDER + filename)
    os.system(remote_print)


if __name__ == "__main__":
    if RedisService.get_list_length(QUEUED_JOB_LIST) > 0:
        if not is_server_on():
            wake_on_lan()
            while not is_server_on():
                time.sleep(5)
        while True:
            job = RedisService.pop_from_list(QUEUED_JOB_LIST)
            send_and_print(job["filename"], job["copies"])
            RedisService.push_to_fifo(PRINTED_JOB_LIST, job)
