import random
import string
from . import RedisService

TOKEN_LENGTH = 32
TOKEN_KEY_PREFIX = "token:"
TOKEN_TTL = 24 * 3600  # 24 hours


def generate_token():
    token = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(TOKEN_LENGTH))
    RedisService.set(TOKEN_KEY_PREFIX + token, "pontedera", TOKEN_TTL)
    return token


def check_token(token: str):
    value = RedisService.get(TOKEN_KEY_PREFIX + token)
    return value == "pontedera"
