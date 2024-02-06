import datetime

from django.db.models import Q
from eProc_Basic.Utilities.constants.constants import CONST_ANNOUNCEMENT_ACTIVE
from eProc_Basic.Utilities.functions.django_query_set import DjangoQueries
from eProc_Basic.Utilities.functions.sort_dictionary import sort_list_dictionary_key_values
from eProc_Basic.Utilities.global_defination import global_variables
from eProc_Org_Support.models import OrgAnnouncements

django_query_instance = DjangoQueries()


class ShopHome:
    def __init__(self):
        self.client = global_variables.GLOBAL_CLIENT
        self.username = global_variables.GLOBAL_LOGIN_USERNAME

    def org_announcement_filter_query(self, filter_based_on):
        filter_based_on['client'] = self.client
        filter_based_on['del_ind'] = False
        return django_query_instance.django_filter_only_query(OrgAnnouncements, filter_based_on)

    # def get_org_announcements(self):
    #     # current_date = datetime.datetime.now()
    #     current_date = datetime.date.today()
    #
    #     # update completed announcement status to Inactive
    #     # org_announcements_data_completed = self.org_announcement_filter_query({
    #     #     'status': CONST_ANNOUNCEMENT_ACTIVE,
    #     #     'announcement_to_date__lte': current_date
    #     # })
    #
    #     # if org_announcements_data_completed.exists():
    #     #     org_announcements_data_completed.update(status=CONST_ANNOUNCEMENT_INACTIVE)
    #
    #     # Update current announcement status to Active if set initially to Inactive
    #     # org_announcements_query = self.org_announcement_filter_query({
    #     #     'announcement_from_date__lte': current_date,
    #     #     'announcement_to_date__gte': current_date
    #     # })
    #     # org_announcements_query.update(status=CONST_ANNOUNCEMENT_ACTIVE)
    #
    #     # Get announcements which fall under today's date and  status set to Active
    #     # org_announcements_data = self.org_announcement_filter_query({
    #     #     'status': CONST_ANNOUNCEMENT_ACTIVE,
    #     #     'announcement_from_date__lte': current_date,
    #     #     'announcement_to_date__gte': current_date,
    #     #
    #     # })
    #     priority_list = ['High', 'Medium', 'Low']
    #
    #     # org_announcements_data_list1 = list(OrgAnnouncements.objects.filter(
    #     #     Q(announcement_from_date__gte=current_date) | Q(announcement_from_date__isnull=True),
    #     #     Q(announcement_to_date__lte=current_date) | Q(announcement_to_date__isnull=True),
    #     #     status=CONST_ANNOUNCEMENT_ACTIVE,
    #     #     client=self.client, del_ind=False).values())
    #
    #     # org_announcements_data_list = list(OrgAnnouncements.objects.filter(
    #     #     announcement_from_date__gte=datetime.date(2021, 1, 18),
    #     #     announcement_to_date__lte=datetime.date(2022, 12, 31)
    #     # ).values())
    #
    #     announcement_dates = list(OrgAnnouncements.objects.filter(client=self.client, del_ind=False).values())
    #     org_announcements_data_list = list(OrgAnnouncements.objects.filter(
    #         announcement_from_date__lte=current_date,
    #         announcement_to_date__gte=current_date
    #     ).values())
    #
    #     for key in announcement_dates:
    #         start_date = key['announcement_from_date']
    #         end_date = key['announcement_to_date']
    #
    #     org_announcements_data = sort_list_dictionary_key_values(priority_list, org_announcements_data_list, 'priority')
    #
    #     return org_announcements_data

    def get_org_announcements(self):
        current_date = datetime.date.today()

        # Get announcements which fall under today's date and have status set to Active
        org_announcements_data = list(OrgAnnouncements.objects.filter(
            status=CONST_ANNOUNCEMENT_ACTIVE,  # Assuming CONST_ANNOUNCEMENT_ACTIVE is defined elsewhere
            announcement_from_date__lte=current_date,
            announcement_to_date__gte=current_date,
            client=self.client, del_ind=False
        ).values())

        priority_list = ['High', 'Medium', 'Low']

        # Sort announcements based on priority
        org_announcements_data = sort_list_dictionary_key_values(priority_list, org_announcements_data, 'priority')

        return org_announcements_data

