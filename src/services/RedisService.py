from typing import Union
from redis import Redis

redisClient = Redis(host="redis", port=6379, db=0, decode_responses=True)


def get(key: str):
    return redisClient.get(key)


def set(key: str, value: Union[str, int, float], expiration_sec=None):
    return redisClient.set(key, value=value, ex=expiration_sec)
