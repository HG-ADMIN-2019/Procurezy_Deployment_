from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.get_db_query import getClients
from eProc_Configuration.models import OrgClients, SapConnector

django_query_instance = DjangoQueries()


def save_connection(request):
    if request.method == 'POST':
        client = getClients(request)
        sys_id = request.POST.get('sys_id')
        check_exists = django_query_instance.django_existence_check(SapConnector, {'sys_id': sys_id, 'del_ind': False})

        if not check_exists:
            inst = SapConnector()
            inst.ashost = request.POST.get('ashost')
            inst.sys_id = request.POST.get('sys_id')
            inst.sys_name = request.POST.get('sys_name')
            inst.sysnr = request.POST.get('sysnr')
            inst.client = django_query_instance.django_get_query(OrgClients, {'client': client})
            inst.user = request.POST.get('user')
            inst.passwd = request.POST.get('passwd')
            inst.del_ind = False
            inst.save()

        else:
            update_row = django_query_instance.django_get_query(SapConnector,
                                                                {'sys_id': sys_id, 'client': client, 'del_ind': False})
            update_row.sys_name = request.POST.get('sys_name')
            update_row.ashost = request.POST.get('ashost')
            update_row.sysnr = request.POST.get('sysnr')
            update_row.user = request.POST.get('user')
            update_row.passwd = request.POST.get('passwd')
            update_row.save()

        return django_query_instance.django_filter_only_query(SapConnector, {
            'client': client, 'sys_id': sys_id, 'del_ind': False
        })
