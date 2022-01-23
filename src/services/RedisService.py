from typing import Union
from redis import Redis
import random
import time

redisClient = Redis(host="redis", port=6379, db=0, decode_responses=True)


def get(key: str):
    return redisClient.get(key)


def set(key: str, value: Union[str, int, float], expiration_sec=None):
    return redisClient.set(key, value=value, ex=expiration_sec)


def push_to_fifo(key: str, value: str):
    return redisClient.lpush(key, value)


def pop_from_fifo(key: str) -> str:
    return redisClient.rpop(key)


def reset_fifo(key: str, *values: str):
    redisClient.delete(key)
    redisClient.lpush(key, *values)


def get_list(key: str):
    return redisClient.lrange(key, 0, 1000)


def incr(key: str):
    return redisClient.incr(key)


def decr(key: str):
    return redisClient.decr(key)


def get_lock(resource: str, expiration_sec: int = 10):
    """
    Set a lock with expiration
    """
    lock = str(random.randrange(0, 1000)) + "-" + str(time.time())
    while not redisClient.set(resource, lock, ex=expiration_sec, nx=True):
        time.sleep(0.1)
    return lock


def release_lock(resource: str, lock: str):
    """
    Release a lock. Return 0 if the lock expired, else 1
    """
    curlock = redisClient.get(resource)
    if curlock != lock:
        return 0
    else:
        redisClient.delete(resource)
        return 1
