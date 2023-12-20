
from django.contrib.auth.decorators import login_required
import csv
import io

from django.shortcuts import render
from django.contrib import messages

from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Basic.Utilities.messages.messages import *
from django.utils.datastructures import MultiValueDictKeyError

from eProc_Upload.Utilities.upload_data.upload_pk_tables import UploadBasicTables
from eProc_Upload.Utilities.upload_specific.upload_prod_services import upload_prod_services


@login_required
def data_upload(req):
    """
    on click of Data upload in nav bar liked to data upload page
    :param req: request data from UI
    :return: render data_upload.html and context
    """
    context = {'inc_nav': True, 'nav_title': 'Upload data'}
    return render(req, 'Upload/data_upload.html', context)


def upload_prod_services_data(request):

        template = "Upload/upload_csv_attachment.html"
        msgid = 'MSG180'
        error_msg = get_message_desc(msgid)[1]

        prompt = {
            'order': error_msg
        }

        if request.method == "GET":
            return render(request, template, prompt)
        if request.method == 'POST':
            Test_mode = request.POST.get('test')

            try:
                csv_file = request.FILES['file']
                if not csv_file.name.endswith('.csv'):
                    error_msg = get_message_desc(MSG044)[1]
                    # msgid = 'MSG044'
                    # error_msg = get_msg_desc(msgid)
                    # msg = error_msg['message_desc'][0]
                    # error_msg = msg

                    messages.error(request, error_msg)
                    # messages.error(request, MSG044)

                    return render(request, template, prompt)

                data_set = csv_file.read().decode('utf8')

                fin_prod_upld_data = io.StringIO(data_set)
                next(fin_prod_upld_data)

                is_saved = upload_prod_services(request, fin_prod_upld_data, Test_mode)

                if is_saved:
                    # messages.success(request,MSG037)
                    return render(request, template, prompt)
                else:
                    return render(request, template, prompt)

            except MultiValueDictKeyError:
                csv_file = False
                # messages.error(request, MSG063)

                return render(request, template, prompt)
        context = {
        }
        return render(request, template, prompt)

