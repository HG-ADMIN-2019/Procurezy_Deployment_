import re
from Majjaka_eProcure import settings
from eProc_Basic.Utilities.constants.constants import CONST_CLIENT, CONST_USER_NAME, CONST_PASSWORD, CONST_PWD, \
    CONST_FIRST_NAME
from eProc_Configuration.models import NotifSettings
from eProc_Registration.models import UserData


def email():
    tmp = UserData.objects.filter(client='700').values()
    uname = tmp['username']
    firstname = tmp['first_name']
    email = tmp['email']
    # client = getClients(req)
    # gets the email content based on the variant name
    emailDetail = NotifSettings.objects.filter(variant_name='user_reg', client='700').values('notif_subject',
                                                                                                'notif_body')
    # loop to separate the subject and body from query set
    for subValue in emailDetail:
        subject = subValue['notif_subject']
    for bodyValue in emailDetail:
        body = bodyValue['notif_body']
    #  this function separates the keywords from the content.
    subjectKeys = re.findall('\&.*?\&', subject)
    bodyKeys = re.findall('\&.*?\&', body)
    # loop to assign the respective values based on the keywords from the email content
    for data in subjectKeys and bodyKeys:
        if data == CONST_CLIENT:
            client = '700'
            subject = subject.replace(data, client)
            body = body.replace(data, client)
        if data == CONST_USER_NAME:
            username = uname
            subject = subject.replace(data, username)
            body = body.replace(data, username)
        if data == CONST_PASSWORD:
            password = CONST_PWD
            body = body.replace(data, password)
        if data == CONST_FIRST_NAME:
            first_name = firstname
            subject = subject.replace(data, first_name)
            body = body.replace(data, first_name)
    # assigns to and from email
    to_mail = email
    From_Email = settings.EMAIL_HOST_USER
    To_Email = [to_mail]
    # main function to send an email.

    # schedule.every(10).seconds.do(send_mail(subject, body, From_Email, To_Email, fail_silently=True))
    # while 1:
    #     schedule.run_pending()
    #     time.sleep(1)