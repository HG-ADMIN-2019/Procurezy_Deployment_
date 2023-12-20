"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    notes_attachments_specific.py
Usage:
    Consists of validation functions and some special character handling functions
    validation for checking a string contains Mathematical symbols

Author:
    Shilpa Ellur
"""

import re


def validationMathSymbols(input):
    """
    Functions which checks the input is having mathematical symbols
    :return: Boolean
    """
    regex = re.compile('[+/=%<>*-]')
    if regex.search(input) is None:
        return False
    else:
        return True
