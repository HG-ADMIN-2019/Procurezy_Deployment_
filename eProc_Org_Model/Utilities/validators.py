import re


class Validators:
    """
    Custom validator class
    """
    def name_valid(self, inp):
        """
        Checks for alphanumeric with '_'
        :param inp: input value
        :return: True / False
        """
        if re.match("^[A-Za-z0-9 _-]+$", inp):
            return True
        return False

    def alpha_num(self, inp):
        """
        Checks for alphanumeric
        :param inp: input value
        :return: True / False
        """
        if str(inp).isalnum():
            return True
        return False

    def alphabets(self, inp):
        """
        Checks for only alphabets
        :param inp: input value
        :return: True / False
        """
        if str(inp).isalpha():
            return True
        return False
