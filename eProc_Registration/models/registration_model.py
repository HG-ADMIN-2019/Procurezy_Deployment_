import os
import re
from django.contrib.auth.models import UserManager, AbstractUser
from django.db import models
from eProc_Configuration.models import OrgClients
from eProc_Org_Model.models import OrgModel
from django.utils.translation import gettext_lazy as _


class DBQueriesUser:

    @staticmethod
    def get_user_details_by_fields(client, obj, username_query, first_name_query, last_name_query, email_query,
                                   user_type_query, employee_id_query, pwd_locked_query, user_locked_query,
                                   is_active_query):
        return list(UserData.objects.filter(username_query, first_name_query, last_name_query, email_query,
                                            user_type_query, employee_id_query, pwd_locked_query,
                                            user_locked_query, is_active_query, client=client,
                                            del_ind=False).values().order_by('username'))


class UserData(AbstractUser, DBQueriesUser):
    email = models.EmailField(db_column='EMAIL', primary_key=True, max_length=100, null=False,
                              error_messages={'unique': _("Email-Id already exists."), })
    username = models.CharField(db_column='USERNAME', null=False, unique=False, max_length=16)
    person_no = models.CharField(db_column='PERSON_NO', max_length=2, blank=True, null=True,
                                 verbose_name='Personal Number')
    form_of_address = models.CharField(db_column='FORM_OF_ADDRESS', max_length=40, null=False)
    first_name = models.CharField(db_column='FIRST_NAME', max_length=30, null=False)
    last_name = models.CharField(db_column='LAST_NAME', max_length=30, null=False)
    gender = models.CharField(db_column='GENDER', max_length=12, null=True, blank=True)
    phone_num = models.CharField(db_column='PHONE_NUM', max_length=30, null=True)
    password = models.CharField(db_column='PASSWORD', max_length=256, null=False)
    date_joined = models.DateTimeField(db_column='DATE_JOINED', null=True)
    first_login = models.DateTimeField(db_column='FIRST_LOGIN', null=True)
    last_login = models.DateTimeField(db_column='LAST_LOGIN', null=True)
    is_active = models.BooleanField(db_column='IS_ACTIVE', default=True,
                                    null=False)  # if user is not login more than few months then set this flag to true
    is_superuser = models.BooleanField(db_column='IS_SUPERUSER', default=False, null=False)
    is_staff = models.BooleanField(db_column='IS_STAFF', default=True, null=False)
    date_format = models.CharField(db_column='DATE_FORMAT', max_length=30, null=True)
    employee_id = models.CharField(db_column='EMPLOYEE_ID', max_length=15, null=True)
    decimal_notation = models.CharField(db_column='DECIMAL_NOTATION', max_length=15, null=True)
    user_type = models.CharField(db_column='USER_TYPE', max_length=25, default=False, null=False)
    login_attempts = models.PositiveIntegerField(db_column='LOGIN_ATTEMPTS', default=False, null=False)
    user_locked = models.BooleanField(default=False, null=False,
                                      db_column='USER_LOCKED')  # Admin user explicitly lock the user
    pwd_locked = models.BooleanField(db_column='PWD_LOCKED', default=False, null=False)
    sso_user = models.BooleanField(default=False, null=True, db_column='SSO_USER')
    user_data_created_at = models.DateTimeField(db_column='USER_DATA_CREATED_AT', blank=True, null=True)
    user_data_created_by = models.CharField(db_column='USER_DATA_CREATED_BY', max_length=30, null=True)
    user_data_changed_at = models.DateTimeField(db_column='USER_DATA_CHANGED_AT', blank=True, null=True)
    user_data_changed_by = models.CharField(db_column='USER_DATA_CHANGED_BY', max_length=30, null=True)
    valid_from = models.DateTimeField(db_column='VALID_FROM', blank=True, null=True)
    valid_to = models.DateTimeField(db_column='VALID_TO', blank=True, null=True)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=True)
    currency_id = models.ForeignKey('eProc_Configuration.Currency', models.DO_NOTHING, db_column='CURRENCY', null=True)
    language_id = models.ForeignKey('eProc_Configuration.Languages', db_column='LANGUAGE_ID', max_length=5, null=True,
                                    on_delete=models.PROTECT)
    object_id = models.ForeignKey('eProc_Org_Model.OrgModel', db_column='OBJECT_ID', on_delete=models.PROTECT,
                                  null=True)
    time_zone = models.ForeignKey('eProc_Configuration.TimeZone', db_column='TIME_ZONE', on_delete=models.PROTECT,
                                  null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'employee_id']
    objects = UserManager()

    # Defining the meta data for User table
    class Meta:
        managed = True
        unique_together = ('client', 'username')
        db_table = 'MMD_USER_INFO'

    # Get creator id and requester id by first name
    @staticmethod
    def get_usrid_by_first_name(fname: object) -> object:
        if '*' in fname:
            created_by = re.search(r'[a-zA-Z0-9]+', fname)
            if fname[0] == '*' and fname[-1] == '*':
                queryset = UserData.objects.values_list('username', flat=False).filter(
                    first_name__icontains=created_by.group(0))
            elif fname[0] == '*':
                queryset = UserData.objects.values_list('username', flat=False).filter(
                    first_name__iendswith=created_by.group(0))
            else:
                queryset = UserData.objects.values_list('username', flat=False).filter(
                    first_name__istartswith=created_by.group(0))
        else:
            queryset = UserData.objects.values_list('username', flat=False).filter(first_name=fname)
        user_list = []
        for field in queryset:
            user_list.append(field[0])
        return user_list


class UserDataHistory(models.Model):
    email_key = models.AutoField(primary_key=True, db_column='EMAIL_KEY', null=False)
    email = models.EmailField(db_column='EMAIL', max_length=100, null=False)
    username = models.CharField(db_column='USERNAME', null=False, max_length=16)
    person_no = models.CharField(db_column='PERSON_NO', max_length=2, blank=True, null=True,
                                 verbose_name='Personal Number')
    form_of_address = models.CharField(db_column='FORM_OF_ADDRESS', max_length=40, null=False)
    first_name = models.CharField(db_column='FIRST_NAME', max_length=30, null=False)
    last_name = models.CharField(db_column='LAST_NAME', max_length=30, null=False)
    gender = models.CharField(db_column='GENDER', max_length=12, null=True, blank=True)
    phone_num = models.CharField(db_column='PHONE_NUM', max_length=30, null=True)
    password = models.CharField(db_column='PASSWORD', max_length=256, null=False)
    date_joined = models.DateTimeField(db_column='DATE_JOINED', null=True)
    first_login = models.DateTimeField(db_column='FIRST_LOGIN', null=True)
    last_login = models.DateTimeField(db_column='LAST_LOGIN', null=True)
    is_active = models.BooleanField(db_column='IS_ACTIVE', default=True,
                                    null=False)  # if user is not login more than few months then set this flag to true
    is_superuser = models.BooleanField(db_column='IS_SUPERUSER', default=False, null=False)
    is_staff = models.BooleanField(db_column='IS_STAFF', default=True, null=False)
    date_format = models.CharField(db_column='DATE_FORMAT', max_length=30, null=True)
    employee_id = models.CharField(db_column='EMPLOYEE_ID', max_length=15, null=True)
    decimal_notation = models.CharField(db_column='DECIMAL_NOTATION', max_length=15, null=True)
    user_type = models.CharField(db_column='USER_TYPE', max_length=25, default=False, null=False)
    login_attempts = models.PositiveIntegerField(db_column='LOGIN_ATTEMPTS', default=False, null=False)
    user_locked = models.BooleanField(default=False, null=False,
                                      db_column='USER_LOCKED')  # Admin user explicitly lock the user
    pwd_locked = models.BooleanField(db_column='PWD_LOCKED', default=False, null=False)
    sso_user = models.BooleanField(default=False, null=True, db_column='SSO_USER')
    user_data_created_at = models.DateTimeField(db_column='USER_DATA_CREATED_AT', blank=True, null=True)
    user_data_created_by = models.CharField(db_column='USER_DATA_CREATED_BY', max_length=30, null=True)
    user_data_changed_at = models.DateTimeField(db_column='USER_DATA_CHANGED_AT', blank=True, null=True)
    user_data_changed_by = models.CharField(db_column='USER_DATA_CHANGED_BY', max_length=30, null=True)
    valid_from = models.DateTimeField(db_column='VALID_FROM', blank=True, null=True)
    valid_to = models.DateTimeField(db_column='VALID_TO', blank=True, null=True)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.CharField(max_length=8, db_column='CLIENT', null=True)
    currency_id = models.CharField(db_column='CURRENCY_ID', max_length=3, null=True)
    language_id = models.CharField(db_column='LANGUAGE_ID', max_length=2, null=True)
    object_id = models.PositiveBigIntegerField(db_column='OBJECT_ID',null=True)
    time_zone = models.CharField(db_column='TIME_ZONE', max_length=6,null=True)

    # Defining the meta data for User table
    class Meta:
        managed = True
        db_table = 'MTD_USER_INFO_HISTORY'
