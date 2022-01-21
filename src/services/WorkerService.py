import os
import time

WORKER_MAC = os.getenv("WORKER_MAC")
WORKER_IP = os.getenv("WORKER_IP")


def startup_and_wait():
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
