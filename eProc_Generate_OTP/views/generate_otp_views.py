from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.guid_generator import random_int
from eProc_Basic.Utilities.functions.json_parser import JsonParser
from eProc_Generate_OTP.Utilities.generate_otp_generic import send_otp, otp_generator, otp_verification
from eProc_Generate_OTP.models import OtpGenerator

django_query_instance = DjangoQueries()
JsonParser_obj = JsonParser()


def generate_otp(request):
    """
        :param request:OTP Request
        :return: Login/login.html
    """
    email = request.POST.get('email')
    otp_generator(email)
    context = {}
    return JsonResponse({}, status=201)


def reset_otp(request):
    email = request.POST.get('email')
    if request.method == 'POST':
        django_query_instance.django_update_query(OtpGenerator, {'del_ind': False, 'email': email}, {'otp': None})

    return JsonResponse({'success': 'success'}, status=200)


def admin_login(request):
    context = {}
    return render(request, 'otp.html', context)


def otp_verification_views(request):
    """

    """
    email = request.POST.get('email')
    otp = request.POST.get('otp')
    data = {'email': email, 'otp': otp}
    verification_flag = otp_verification(data)
    return JsonResponse({'verification_flag': verification_flag}, status=201)
