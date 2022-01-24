import os
import time
from services import RedisService

WORKER_MAC = os.getenv("WORKER_MAC")
WORKER_IP = os.getenv("WORKER_IP")
WORKER_USER = os.getenv("WORKER_USER")
WORKER_REQUESTS_KEY = "worker_requests"
WORKER_WOL_RETRIES = 15
WORKER_WOL_PING_INT = 7


def request_worker():
    """
    Register a new process that requires the worker machine
    """
    RedisService.incr(WORKER_REQUESTS_KEY)
    return _startup_and_wait()


def release_worker():
    """
    De-register a process from the worker machine
    If no more processes are registered, shut down the worker
    """
    active_workers = RedisService.decr(WORKER_REQUESTS_KEY)
    if active_workers <= 0:
        print("WorkerService: shutting down worker by writing special file")
        # The worker has a cron job that checks for this file and, if present, shuts down the pc
        run_command("touch ~/shutdown/shutdown.txt")
    elif active_workers < 0:
        print("WorkerService: Deregistering a process which was not registered")
        RedisService.set(WORKER_REQUESTS_KEY, 0)


def _startup_and_wait():
    """
    Launch wake on lan command to wake up print server and wait for it to be up and running
    """
    os.system('wakeonlan {} > /dev/null'.format(WORKER_MAC))
    print("Magic packet sent")
    ping_command = 'timeout 0.2s ping {} -c 1 > /dev/null'.format(WORKER_IP)
    tries = 1
    while not os.system(ping_command) == 0:
        print("Pinging worker")
        time.sleep(WORKER_WOL_PING_INT)
        tries += 1
        if tries > WORKER_WOL_RETRIES:
            print("Worker not responding")
            return False
    print("Worker responded to ping, wait for ssh to be on")
    tries = 1
    while not run_command("echo ssh-ok") == 0:
        print("SSH-pinging worker")
        time.sleep(WORKER_WOL_PING_INT)
        tries += 1
        if tries > WORKER_WOL_RETRIES:
            print("Worker not responding to SSH")
            return False
    return True


def transfer_file(local_path: str, remote_path: str):
    """
    Execute a SCP command to transfer a file on the worker machine
    """
    copy_cmd = "scp {} {}@{}:{} > /dev/null".format(local_path, WORKER_USER, WORKER_IP, remote_path)
    os.system(copy_cmd)


def run_command(command: str):
    """
    Execute a command on the worker machine and return its result
    """
    sanitized_command = command.replace("'", "\\'")
    remote_print_cmd = "ssh {}@{} '{}' > /dev/null".format(WORKER_USER, WORKER_IP, sanitized_command)
    return os.system(remote_print_cmd)
