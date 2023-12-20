from django.core.mail import send_mail
from Majjaka_eProcure import settings
from eProc_Basic.Utilities.functions.encryption_util import encrypt, decrypt
from eProc_Basic.Utilities.functions.guid_generator import random_int
from eProc_Basic.Utilities.functions.messages_config import *
from eProc_Basic.Utilities.messages.messages import MSG055, MSG0122
from eProc_Generate_OTP.models import OtpGenerator
from twilio.rest import Client
django_query_instance = DjangoQueries()


def send_otp(generated_otp, email):
    """

    """
    From_Email = settings.EMAIL_HOST_USER
    to_email = [email]
    body = 'Dear User,\nYour Majjaka Admin verification code is' + str(generated_otp) + '\n Regards,\n Majjaka'
    if to_email:
        send_mail('Admin Login OTP:' + str(generated_otp), body, From_Email, to_email, fail_silently=True)
    # Find your Account SID and Auth Token at twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    # account_sid = 'ACec15265aacc56338bff847d5a6536cae'
    # auth_token = 'c5ae266c5d1b557e092c0b48f0beb3cf'
    # client = Client(account_sid, auth_token)
    #
    # message = client.messages.create(
    #     from_='+14125346832',
    #     body='Dear User,\nYour Majjaka Admin verification code is' + str(generated_otp) + ' \n Regards,\n Majjaka',
    #     to='+919845648568'
    # )


def otp_generator(email):
    """

    """
    generate_otp = random_int(4)
    print(generate_otp)
    django_query_instance.django_update_query(OtpGenerator, {'email': email, 'del_ind': False},
                                              {'otp': generate_otp})
    send_otp(generate_otp, email)


def otp_verification(data):
    """

    """
    verification_flag = False
    if django_query_instance.django_existence_check(OtpGenerator, {'email': data['email']}):
        generate_otp = django_query_instance.django_filter_value_list_query(OtpGenerator,
                                                                            {'email': data['email']},
                                                                            'otp')[0]
        if generate_otp:
            if generate_otp == data['otp']:
                verification_flag = True
    return verification_flag


def authentication_check(user_data):
    """

    """
    error_msg = ''
    authentication_flag = False
    if django_query_instance.django_existence_check(OtpGenerator, {'email': user_data['email']}):
        user_details = django_query_instance.django_get_query(OtpGenerator, {
            'email': user_data['email']
        })
        password = decrypt(user_details.password)
        if user_data['password'] == password:
            authentication_flag = True
        else:
            error_msg = MSG0122

    else:
        error_msg = MSG0122

    return authentication_flag, error_msg
