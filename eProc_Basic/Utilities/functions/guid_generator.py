import random
import uuid


def guid_generator():
    return uuid.uuid4().hex.upper()


def random_int(N):
    min = pow(10, N - 1)
    max = pow(10, N) - 1
    return random.randint(min, max)


def dynamic_guid_generator(length):
    """

    """
    return str(uuid.uuid4().hex[:int(length)].upper())
