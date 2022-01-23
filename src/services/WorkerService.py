import os
import time
from services import RedisService

WORKER_MAC = os.getenv("WORKER_MAC")
WORKER_IP = os.getenv("WORKER_IP")
WORKER_REQUESTS_KEY = "worker_requests"


def request_worker():
    """
    Register a new process that requires the worker machine
    """
    RedisService.incr(WORKER_REQUESTS_KEY)
    _startup_and_wait()


def release_worker():
    """
    De-register a process from the worker machine
    If no more processes are registered, shut down the worker
    """
    active_workers = RedisService.decr(WORKER_REQUESTS_KEY)
    if active_workers <= 0:
        run_command("shutdown now")
    elif active_workers < 0:
        print("WorkerService: Deregistering a process which was not registered")
        RedisService.set(WORKER_REQUESTS_KEY, 0)


def _startup_and_wait():
    """
    Launch wake on lan command to wake up print server and wait for it to be up and running
    """
    os.system('wakeonlan {} > /dev/null'.format(WORKER_MAC))
    ping_command = 'timeout 0.2s ping {} -c 1 > /dev/null'.format(WORKER_IP)
    while not os.system(ping_command) == 0:
        time.sleep(5)


def transfer_file(local_path: str, remote_path: str):
    """
    Execute a SCP command to transfer a file on the worker machine
    """
    copy_cmd = "scp {} cod@{}:{} > /dev/null".format(local_path, WORKER_IP, remote_path)
    os.system(copy_cmd)


def run_command(command: str):
    """
    Execute a command on the worker machine and return its result
    """
    sanitized_command = command.replace("'", "\\'")
    remote_print_cmd = "ssh cod@{} '{}' > /dev/null".format(WORKER_IP, sanitized_command)
    return os.system(remote_print_cmd)
