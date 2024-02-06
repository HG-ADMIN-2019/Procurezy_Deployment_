import re
from re import sub


def convert_to_camel_case(s):
    s = sub(r"(_|-)+", " ", s).title().replace(" ", " ")
    return ''.join([s[0], s[1:]])


def convert_to_camel_case_v2(s):
    s = re.sub(r"(_|-)+", " ", s).title().replace(" ", "")
    return s if not s else s[0].upper() + s[1:]
