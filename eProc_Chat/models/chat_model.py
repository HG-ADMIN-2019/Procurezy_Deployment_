from django.db import models


class ChatParticipants(models.Model):
    chat_participants_guid = models.CharField(db_column='CHAT_PARTICIPANTS_GUID', primary_key=True,
                                                  max_length=32)
    room_no = models.CharField(db_column='ROOM_NO', max_length=60, null=False)
    room_name = models.CharField(db_column='room_name', max_length=300, blank=True, null=True)
    username = models.CharField(db_column='USERNAME', null=False, unique=False, max_length=16)
    chat_type = models.CharField(db_column='CHAT_TYPE', null=False, max_length=30)
    Chat_created_at = models.DateTimeField(db_column='CHAT_CREATED_AT', blank=True, null=True,
                                           verbose_name='Created At')
    Chat_created_by = models.CharField(db_column='CHAT_CREATED_BY', max_length=30, null=True, verbose_name='Created by')
    Chat_changed_at = models.DateTimeField(db_column='CHAT_CHANGED_AT', blank=True, null=True,
                                           verbose_name='Changed At')
    Chat_changed_by = models.CharField(db_column='CHAT_CHANGED_BY', max_length=30, null=True, verbose_name='Changed By')
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    language_id = models.ForeignKey('eProc_Configuration.Languages', db_column='LANGUAGE_ID', max_length=5, null=True,
                                    on_delete=models.PROTECT)

    class Meta:
        db_table = 'MTD_CHAT_PARTICIPANTS'
        managed = True
        unique_together = ('room_no', 'client', 'username', 'chat_type')


class ChatContent(models.Model):
    chat_content_guid = models.CharField(db_column='CHAT_CONTENT_GUID', primary_key=True, max_length=32)
    room_no = models.CharField(db_column='ROOM_NO', max_length=60, null=False)
    username = models.CharField(db_column='USERNAME', null=False, max_length=16)
    chat_content = models.CharField(db_column='CHAT_CONTENT', max_length=2000, blank=True, null=True,
                                       verbose_name='Chat content')
    chat_timestamp = models.DateTimeField(auto_now_add=True, db_column='CHAT_TIMESTAMP')
    Chat_content_created_at = models.DateTimeField(db_column='CHAT_CONTENT_CREATED_AT', blank=True, null=True)
    Chat_content_created_by = models.CharField(db_column='CHAT_CONTENT_CREATED_BY', max_length=30, null=True)
    Chat_content_changed_at = models.DateTimeField(db_column='CHAT_CONTENT_CHANGED_AT', blank=True, null=True)
    Chat_content_changed_by = models.CharField(db_column='CHAT_CONTENT_CHANGED_BY', max_length=30, null=True)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    sc_header_guid = models.ForeignKey('eProc_Shopping_Cart.ScHeader', models.DO_NOTHING, db_column='SC_HEADER_GUID',
                                       blank=True, null=True)

    class Meta:
        db_table = 'MTD_CHAT_CONTENT'
        managed = True

