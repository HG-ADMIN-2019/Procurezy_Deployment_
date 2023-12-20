from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
import re


# Customized password validator which override the django in-built validations.
class CustomPasswordValidator():

    def __init__(self, min_length=1):
        self.min_length = min_length

    def validate(self, password, user=None):
        special_characters = "[!@#$]"
        # Should contain atleast one Digit
        if not (len( password ) > 9 and len( password ) < 16 and re.search( "[a-z]", password ) and
                re.search( "[0-9]",password ) and re.search("[A-Z]", password ) and re.search( "[$#@!]", password )):
            raise ValidationError('Your password must contain atleast 8 characters including a number, '
                                  'uppercase letter, lowercase letter and atleast one of these !@#$ ')
        # Should not contain White spaces
        if re.search("\s",password):
            raise ValidationError('Password cannot contain white spaces')

    def get_help_text(self):
        return "Your password must contain any one of these !@#$"

# Function to check any special charecters in string or input box
def check_spl_characters():
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    return regex
