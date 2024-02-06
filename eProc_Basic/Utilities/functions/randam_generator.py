import random
import string


def random_alpha_numeric(length):
    random_value = ''.join(random.choices(string.ascii_uppercase +
                           string.digits, k=length))
    return random_value