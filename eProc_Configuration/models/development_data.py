from django.db import models


class AccountAssignmentCategory(models.Model):
    """
    Contains AccountAssignmentCategory List for user settings
    """
    account_assign_cat = models.CharField(db_column='ACCOUNT_ASSIGN_CAT', primary_key=True, max_length=10,
                                          verbose_name='AccountAssignmentCat')
    description = models.CharField(db_column='DESCRIPTION', max_length=255, null=True, verbose_name='description')
    account_assignment_category_created_by = models.CharField(db_column='ACCOUNT_ASSIGNMENT_CATEGORY_CREATED_BY',
                                                              max_length=30, null=True)
    account_assignment_category_created_at = models.DateTimeField(db_column='ACCOUNT_ASSIGNMENT_CATEGORY_CREATED_AT',
                                                                  max_length=50, null=True)
    account_assignment_category_changed_by = models.CharField(db_column='ACCOUNT_ASSIGNMENT_CATEGORY_CHANGED_BY',
                                                              max_length=30, null=True)
    account_assignment_category_changed_at = models.DateTimeField(db_column='ACCOUNT_ASSIGNMENT_CATEGORY_CHANGED_AT',
                                                                  max_length=50, null=True)
    del_ind = models.BooleanField(default=False, null=False)

    class Meta:
        db_table = "MDD_ACC_AST_CAT"
        managed = True


class AddressPartnerType(models.Model):
    """
    (1=Organization, 2=Person, 3=Contact person)
    """
    address_partner_type = models.CharField(primary_key=True, db_column='ADDRESS_PARTNER_TYPE', max_length=32)
    address_partner_type_desc = models.CharField(db_column='ADDRESS_PARTNER_TYPE_DESC', max_length=40)
    del_ind = models.BooleanField(default=False, null=False, db_column='DEL_IND')

    class Meta:
        managed = True
        db_table = 'MDD_ADDRESS_PARTNER_TYPE'


class ApproverType(models.Model):
    app_types = models.CharField(db_column='APP_TYPES', primary_key=True, max_length=30, null=False)
    appr_type_desc = models.CharField(db_column='APPROVAL_TYPE_DESC', max_length=30, null=False)
    approver_type_created_by = models.CharField(db_column='APPROVER_TYPE_CREATED_BY', max_length=30, null=True)
    approver_type_created_at = models.DateTimeField(db_column='APPROVER_TYPE_CREATED_AT', max_length=50, null=True)
    approver_type_changed_by = models.CharField(db_column='APPROVER_TYPE_CHANGED_BY', max_length=30, null=True)
    approver_type_changed_at = models.DateTimeField(db_column='APPROVER_TYPE_CHANGED_AT', max_length=50, null=True)
    del_ind = models.BooleanField(default=False, null=False)

    class Meta:
        db_table = "MDD_APPROVAL_TYPES"
        managed = True


class Authorization(models.Model):
    auth_guid = models.CharField(db_column='AUTH_GUID', primary_key=True, max_length=32)
    auth_obj_grp = models.CharField(db_column='AUTH_OBJ_GRP', max_length=40, null=False)
    auth_type = models.CharField(db_column='AUTH_TYPE', max_length=10, null=False)
    authorization_created_by = models.CharField(db_column='AUTHORIZATION_CREATED_BY', max_length=30, null=True)
    authorization_created_at = models.DateTimeField(db_column='AUTHORIZATION_CREATED_AT', max_length=50, null=True)
    authorization_changed_by = models.CharField(db_column='AUTHORIZATION_CHANGED_BY', max_length=30, null=True)
    authorization_changed_at = models.DateTimeField(db_column='AUTHORIZATION_CHANGED_AT', max_length=50, null=True)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    role = models.ForeignKey('eProc_Configuration.UserRoles', db_column='ROLE', on_delete=models.PROTECT)

    class Meta:
        db_table = 'MDD_AUTHORIZATION'
        managed = True
        unique_together = ('client', 'role')


class AuthorizationObject(models.Model):
    auth_obj_id = models.CharField(db_column='AUTH_OBJ_ID', primary_key=True, max_length=20)
    auth_level = models.CharField(db_column='AUTH_LEVEL', max_length=10, null=False)
    auth_level_ID = models.CharField(db_column='AUTH_LEVEL_ID', unique=True, max_length=40, null=False)
    auth_level_desc = models.CharField(db_column='AUTH_LEVEL_DESC', max_length=60, null=True)
    authorization_object_created_by = models.CharField(db_column='AUTHORIZATION_OBJECT_CREATED_BY', max_length=30,
                                                       null=True)
    authorization_object_created_at = models.DateTimeField(db_column='AUTHORIZATION_OBJECT_CREATED_AT', max_length=50,
                                                           null=True)
    authorization_object_changed_by = models.CharField(db_column='AUTHORIZATION_OBJECT_CHANGED_BY', max_length=30,
                                                       null=True)
    authorization_object_changed_at = models.DateTimeField(db_column='AUTHORIZATION_OBJECT_CHANGED_AT', max_length=50,
                                                           null=True)
    del_ind = models.BooleanField(default=False, null=False)

    class Meta:
        db_table = 'MDD_AUTHORIZATION_OBJECTS'
        managed = True


class AuthorizationGroup(models.Model):
    auth_grp_guid = models.CharField(db_column='AUTH_GRP_GUID', primary_key=True, max_length=32)
    auth_obj_grp = models.CharField(db_column='AUTH_OBJ_GRP', max_length=40, null=False)
    auth_grp_desc = models.CharField(db_column='AUTH_GRP_DESC', max_length=60, null=False)
    auth_level = models.CharField(db_column='AUTH_LEVEL', max_length=10, null=False)
    authorization_group_created_by = models.CharField(db_column='AUTHORIZATION_GROUP_CREATED_BY', max_length=30,
                                                      null=True)
    authorization_group_created_at = models.DateTimeField(db_column='AUTHORIZATION_GROUP_CREATED_AT', max_length=50,
                                                          null=True)
    authorization_group_changed_by = models.CharField(db_column='AUTHORIZATION_GROUP_CHANGED_BY', max_length=30,
                                                      null=True)
    authorization_group_changed_at = models.DateTimeField(db_column='AUTHORIZATION_GROUP_CHANGED_AT', max_length=50,
                                                          null=True)

    del_ind = models.BooleanField(default=False, null=False)
    auth_obj_id = models.ForeignKey('eProc_Configuration.AuthorizationObject', db_column='AUTH_OBJ_ID',
                                    on_delete=models.PROTECT)

    class Meta:
        db_table = 'MDD_AUTHORIZATION_GROUP'
        managed = True


class OrgClients(models.Model):
    """
    Table contains client details
    """
    client = models.CharField(primary_key=True, max_length=8, db_column='CLIENT')
    description = models.CharField(db_column='DESCRIPTION', max_length=30, null=False)
    org_clients_created_by = models.CharField(db_column='ORG_CLIENTS_CREATED_BY', max_length=30, null=True)
    org_clients_created_at = models.DateTimeField(db_column='ORG_CLIENTS_CREATED_AT', max_length=50, null=True)
    org_clients_changed_by = models.CharField(db_column='ORG_CLIENTS_CHANGED_BY', max_length=30, null=True)
    org_clients_changed_at = models.DateTimeField(db_column='ORG_CLIENTS_CHANGED_AT', max_length=50, null=True)
    del_ind = models.BooleanField(default=False, null=False)

    class Meta:
        db_table = "MDD_CLIENTS"
        managed = True

    def __str__(self):
        return self.pk


class DocumentStatus(models.Model):
    doc_status = models.CharField(db_column='DOC_STATUS', primary_key=True, max_length=40)
    doc_status_desc = models.CharField(db_column='DOC_STATUS_DESC', null=True, max_length=40)
    doc_level_type = models.CharField(db_column='DOC_LEVEL_TYPE', null=True, max_length=40)
    document_type = models.ForeignKey('eProc_Configuration.DocumentType', on_delete=models.DO_NOTHING,
                                      db_column='DOCUMENT_TYPE', null=False)

    class Meta:
        managed = True
        db_table = 'MAD_DOCUMENT_STATUS'


class DocumentType(models.Model):
    document_type = models.CharField(db_column='DOCUMENT_TYPE', primary_key=True, max_length=5)
    document_type_desc = models.CharField(db_column='DOCUMENT_TYPE_DESC', max_length=30, null=False)
    document_type_created_by = models.CharField(db_column='DOCUMENT_TYPE_CREATED_BY', max_length=30, null=True)
    document_type_created_at = models.DateTimeField(db_column='DOCUMENT_TYPE_CREATED_AT', max_length=50, null=True)
    document_type_changed_by = models.CharField(db_column='DOCUMENT_TYPE_CHANGED_BY', max_length=30, null=True)
    document_type_changed_at = models.DateTimeField(db_column='DOCUMENT_TYPE_CHANGED_AT', max_length=50, null=True)
    del_ind = models.BooleanField(default=False, null=False)

    class Meta:
        db_table = "MDD_DOCUMENT_TYPE"
        managed = True


class FieldDesc(models.Model):
    """

    """
    field_name = models.CharField(db_column='FIELD_NAME', primary_key=True, max_length=30, null=False)
    field_desc = models.CharField(db_column='FIELD_DESC', max_length=30, null=False)
    field_desc_created_by = models.CharField(db_column='FIELD_DESC_CREATED_BY', max_length=30, null=True)
    field_desc_created_at = models.DateTimeField(db_column='FIELD_DESC_CREATED_AT', max_length=50, null=True)
    field_desc_changed_by = models.CharField(db_column='FIELD_DESC_CHANGED_BY', max_length=30, null=True)
    field_desc_changed_at = models.DateTimeField(db_column='FIELD_DESC_CHANGED_AT', max_length=50, null=True)
    del_ind = models.BooleanField(default=False, null=False)

    class Meta:
        db_table = 'MDD_FIELD_DESC'
        managed = True


class FieldTypeDesc(models.Model):
    """

    """
    field_type_id = models.CharField(db_column='FIELD_TYPE_ID', primary_key=True, max_length=30, null=False)
    field_type_desc = models.CharField(db_column='FIELD_TYPE_DESC', max_length=30, null=False)
    field_name = models.ForeignKey('eProc_Configuration.FieldDesc', db_column='FIELD_NAME',
                                   on_delete=models.PROTECT)
    used_flag = models.BooleanField(default=False, null=False)
    field_type_desc_created_by = models.CharField(db_column='FIELD_TYPE_DESC_CREATED_BY', max_length=30, null=True)
    field_type_desc_created_at = models.DateTimeField(db_column='FIELD_TYPE_DESC_CREATED_AT', max_length=50, null=True)
    field_type_desc_changed_by = models.CharField(db_column='FIELD_TYPE_DESC_CHANGED_BY', max_length=30, null=True)
    field_type_desc_changed_at = models.DateTimeField(db_column='FIELD_TYPE_DESC_CHANGED_AT', max_length=50, null=True)
    del_ind = models.BooleanField(default=False, null=False)

    class Meta:
        db_table = 'MDD_FIELD_TYPE_DESC'
        managed = True


class FieldTypeDescription(models.Model):
    """

    """
    objects = None
    field_type_description_guid = models.CharField(db_column='FIELD_TYPE_DESCRIPTION_GUID', primary_key=True,
                                                   max_length=32, null=False)
    field_type_id = models.CharField(db_column='FIELD_TYPE_ID',max_length=30, null=False)
    field_type_desc = models.CharField(db_column='FIELD_TYPE_DESC', max_length=30, null=False)
    field_name = models.ForeignKey('eProc_Configuration.FieldDesc', db_column='FIELD_NAME',
                                   on_delete=models.PROTECT)
    used_flag = models.BooleanField(default=False, null=False, db_column='USED_FLAG')
    field_type_desc_created_by = models.CharField(db_column='FIELD_TYPE_DESC_CREATED_BY', max_length=30, null=True)
    field_type_desc_created_at = models.DateTimeField(db_column='FIELD_TYPE_DESC_CREATED_AT', max_length=50, null=True)
    field_type_desc_changed_by = models.CharField(db_column='FIELD_TYPE_DESC_CHANGED_BY', max_length=30, null=True)
    field_type_desc_changed_at = models.DateTimeField(db_column='FIELD_TYPE_DESC_CHANGED_AT', max_length=50, null=True)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    del_ind = models.BooleanField(default=False, null=False)

    class Meta:
        db_table = 'MDD_FIELD_TYPE_DESCRIPTION'
        managed = True


class ImagesType(models.Model):
    images_type_guid = models.CharField(db_column='IMAGES_TYPE_GUID', primary_key=True, max_length=32, null=False,
                                        default=None)
    image_type = models.CharField(db_column="IMAGE_TYPE", max_length=40, null=True)
    image_type_desc = models.CharField(db_column="IMAGE_TYPE_DESC", max_length=40, null=True)
    images_type_created_by = models.CharField(db_column='IMAGES_TYPE_CREATED_BY', max_length=30, null=True)
    images_type_created_at = models.DateTimeField(db_column='IMAGES_TYPE_CREATED_AT', max_length=50, null=True)
    images_type_changed_by = models.CharField(db_column='IMAGES_TYPE_CHANGED_BY', max_length=30, null=True)
    images_type_changed_at = models.DateTimeField(db_column='IMAGES_TYPE_CHANGED_AT', max_length=50, null=True)
    del_ind = models.BooleanField(default=False, null=False)

    class Meta:
        managed = True
        db_table = 'MDD_IMAGES_TYPE'


class MessagesId(models.Model):
    """

    """
    msg_id_guid = models.CharField(db_column='MSG_ID_GUID', primary_key=True, max_length=32)
    messages_id = models.CharField(db_column='MESSAGES_ID', max_length=10, null=False)
    messages_type = models.CharField(db_column='MESSAGES_TYPE', max_length=20, null=False)
    messages_id_created_by = models.CharField(db_column='MESSAGES_ID_CREATED_BY', max_length=30, null=True)
    messages_id_created_at = models.DateTimeField(db_column='MESSAGES_ID_CREATED_AT', max_length=50, auto_now_add=True,
                                                  null=True)
    messages_id_changed_by = models.CharField(db_column='MESSAGES_ID_CHANGED_BY', max_length=30, null=True)
    messages_id_changed_at = models.DateTimeField(db_column='MESSAGES_ID_CHANGED_AT', max_length=50, auto_now=True,
                                                  null=True)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)

    class Meta:
        db_table = 'MDD_MESSAGES_ID'

    managed = True
    unique_together = ('client', 'messages_id', 'messages_type')


class MessagesIdDesc(models.Model):
    """

    """
    msg_id_desc_guid = models.CharField(db_column='MSG_ID_DESC_GUID', primary_key=True, max_length=32)
    messages_id_desc = models.CharField(db_column='MESSAGES_ID_DESC', max_length=700, null=False)
    messages_category = models.CharField(db_column='MESSAGES_CATEGORY', max_length=1, null=True, blank=True)
    messages_id = models.CharField(db_column='MESSAGES_ID', max_length=10, null=False)
    messages_id_desc_created_by = models.CharField(db_column='MESSAGES_ID_DESC_CREATED_BY', max_length=30, null=True)
    messages_id_desc_created_at = models.DateTimeField(db_column='MESSAGES_ID_DESC_CREATED_AT', max_length=50,
                                                       null=True)
    messages_id_desc_changed_by = models.CharField(db_column='MESSAGES_ID_DESC_CHANGED_BY', max_length=30, null=True)
    messages_id_desc_changed_at = models.DateTimeField(db_column='MESSAGES_ID_DESC_CHANGED_AT', max_length=50,
                                                       null=True)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    language_id = models.ForeignKey('eProc_Configuration.Languages', db_column='LANGUAGE_ID', max_length=5, null=True,
                                    on_delete=models.PROTECT)

    class Meta:
        db_table = 'MDD_MESSAGES_ID_DESC'

    managed = True
    unique_together = ('client', 'messages_id', 'language_id')


class NotifKeywords(models.Model):
    """
    Contains keywords based on variant type
    """
    notif_keyword_guid = models.CharField(primary_key=True, db_column='NOTIF_KEYWORD_GUID', max_length=32)
    variant_name = models.CharField(db_column='VARIANT_NAME', max_length=12, null=False)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)

    class Meta:
        unique_together = ('variant_name', 'client')
        db_table = "MDD_NOTIF_KEYWORDS"
        managed = True


class NotifKeywordsDesc(models.Model):
    """
    Contains keywords based on variant type
    """
    notif_desc_keyword_guid = models.CharField(primary_key=True, db_column='NOTIF_DESC_KEYWORD_GUID', max_length=32)
    variant_name = models.CharField(db_column='VARIANT_NAME', max_length=12, null=False)
    keyword = models.CharField(db_column='KEYWORD', max_length=30, null=False)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    language_id = models.ForeignKey('eProc_Configuration.Languages', db_column='LANGUAGE', on_delete=models.PROTECT,
                                    null=False)

    class Meta:
        db_table = "MDD_NOTIF_KEYWORDS_DESC"
        managed = True


class NotifSettings(models.Model):
    """
    Contains notification & email format data
    """
    notif_guid = models.CharField(primary_key=True, db_column='NOTIF_GUID', max_length=32)
    variant_name = models.CharField(db_column='VARIANT_NAME', max_length=12, null=False)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)

    class Meta:
        db_table = "MDD_NOTIF_SETTINGS"
        unique_together = ('variant_name', 'client')
        managed = True

    def __str__(self):
        return self.variant_name


class NotifSettingsDesc(models.Model):
    """
    Contains notification & email format data
    """
    notif_desc_guid = models.CharField(primary_key=True, db_column='NOTIF_DESC_GUID', max_length=32)
    variant_name = models.CharField(db_column='VARIANT_NAME', max_length=12, null=False)
    notif_subject = models.TextField(db_column='NOTIF_SUBJECT', null=False)
    notif_body = models.TextField(db_column='NOTIF_BODY', null=False)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    language_id = models.ForeignKey('eProc_Configuration.Languages', db_column='LANGUAGE_ID', on_delete=models.PROTECT,
                                    null=False)

    class Meta:
        db_table = "MDD_NOTIF_SETTINGS_DESC"
        unique_together = ('variant_name', 'language_id', 'client')
        managed = True


class NotificationType(models.Model):
    """
    Contains notification type
    """
    notification_type_guid = models.CharField(primary_key=True, db_column='NOTIFICATION_TYPE_GUID', max_length=32)
    notification_type_id = models.CharField(db_column='NOTIFICATION_TYPE_ID', max_length=12, null=False)
    notification_app = models.CharField(db_column='NOTIFICATION_APP', max_length=30, null=False)
    notification_group = models.CharField(db_column='NOTIFICATION_GROUP', max_length=30, null=False)
    notification_type = models.CharField(db_column='NOTIFICATION_TYPE', max_length=30, null=False)
    notification_type_created_by = models.CharField(db_column='NOTIFICATION_TYPE_CREATED_BY', max_length=30, null=True)
    notification_type_created_at = models.DateTimeField(db_column='NOTIFICATION_TYPE_CREATED_AT', max_length=50,
                                                        null=True)
    notification_type_changed_by = models.CharField(db_column='NOTIFICATION_TYPE_CHANGED_BY', max_length=30, null=True)
    notification_type_changed_at = models.DateTimeField(db_column='NOTIFICATION_TYPE_CHANGED_AT', max_length=50,
                                                        null=True)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)

    class Meta:
        unique_together = ('notification_type_id', 'client')
        db_table = "MDD_NOTIFICATION_TYPE"
        managed = True


class NotificationTypeDesc(models.Model):
    """
    Contains notification type and its description
    """
    notification_type_desc_guid = models.CharField(primary_key=True, db_column='NOTIFICATION_TYPE_DESC_GUID',
                                                   max_length=32)
    notification_type_id = models.CharField(db_column='NOTIFICATION_TYPE_ID', max_length=12, null=False)
    notification_message = models.CharField(db_column='NOTIFICATION_MESSAGE', max_length=2000, null=False)
    notification_type_desc_created_by = models.CharField(db_column='NOTIFICATION_TYPE_DESC_CREATED_BY', max_length=30,
                                                         null=True)
    notification_type_desc_created_at = models.DateTimeField(db_column='NOTIFICATION_TYPE_DESC_CREATED_AT',
                                                             max_length=50, null=True)
    notification_type_desc_changed_by = models.CharField(db_column='NOTIFICATION_TYPE_DESC_CHANGED_BY', max_length=30,
                                                         null=True)
    notification_type_desc_changed_at = models.DateTimeField(db_column='NOTIFICATION_TYPE_DESC_CHANGED_AT',
                                                             max_length=50, null=True)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    language_id = models.ForeignKey('eProc_Configuration.Languages', db_column='LANGUAGE', on_delete=models.PROTECT,
                                    null=False)

    class Meta:
        unique_together = ('notification_type_id', 'client', 'language_id')
        db_table = "MDD_NOTIFICATION_TYPE_DESC"
        managed = True


class OrgAttributes(models.Model):
    """
    Contains list of attributes in organization
    """
    attribute_id = models.CharField(db_column='ATTRIBUTE_ID', max_length=16, verbose_name='Attribute ID',
                                    primary_key=True)
    attribute_name = models.CharField(db_column='ATTRIBUTE_NAME', max_length=70, null=True,
                                      verbose_name='Attribute name')
    range_indicator = models.BooleanField(default=False, null=False, db_column='RANGE_INDICATOR')
    multiple_value = models.BooleanField(default=False, null=False, db_column='MULTIPLE_VALUE')
    allow_defaults = models.BooleanField(default=False, null=False, db_column='ALLOW_DEFAULTS')
    inherit_values = models.BooleanField(default=False, null=False, db_column='INHERIT_VALUES')
    maximum_length = models.PositiveIntegerField(db_column='MAXIMUM_LENGTH', blank=True, null=True,
                                                 verbose_name='max_length')
    org_attributes_created_by = models.CharField(db_column='ORG_ATTRIBUTES_CREATED_BY', max_length=30, null=True)
    org_attributes_created_at = models.DateTimeField(db_column='ORG_ATTRIBUTES_CREATED_AT', max_length=50, null=True)
    org_attributes_changed_by = models.CharField(db_column='ORG_ATTRIBUTES_CHANGED_BY', max_length=30, null=True)
    org_attributes_changed_at = models.DateTimeField(db_column='ORG_ATTRIBUTES_CHANGED_AT', max_length=50, null=True)
    del_ind = models.BooleanField(default=False, null=False)

    class Meta:
        db_table = "MDD_ORG_ATTRIBUTES"
        managed = True

    def __str__(self):
        return str(self.attribute_id) if self.attribute_id else ''


class OrgAttributesDesc(models.Model):
    attribute_desc_guid = models.CharField(db_column='ATTRIBUTE_DESC_GUID', max_length=32, primary_key=True)
    attribute_name = models.CharField(db_column='ATTRIBUTE_NAME', max_length=70, null=True,
                                      verbose_name='Attribute Name')
    org_attributes_desc_created_by = models.CharField(db_column='ORG_ATTRIBUTES_DESC_CREATED_BY', max_length=30,
                                                      null=True)
    org_attributes_desc_created_at = models.DateTimeField(db_column='ORG_ATTRIBUTES_DESC_CREATED_AT', max_length=50,
                                                          null=True)
    org_attributes_desc_changed_by = models.CharField(db_column='ORG_ATTRIBUTES_DESC_CHANGED_BY', max_length=30,
                                                      null=True)
    org_attributes_desc_changed_at = models.DateTimeField(db_column='ORG_ATTRIBUTES_DESC_CHANGED_AT', max_length=50,
                                                          null=True)
    del_ind = models.BooleanField(default=False, null=False)
    attribute_id = models.ForeignKey('eProc_Configuration.OrgAttributes', on_delete=models.PROTECT,
                                     db_column='ATTRIBUTE_ID', null=False,
                                     verbose_name='attribute_id')
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    language_id = models.ForeignKey('eProc_Configuration.Languages', db_column='LANGUAGE', on_delete=models.PROTECT,
                                    null=False)

    class Meta:
        db_table = "MDD_ORG_ATTRIBUTES_DESC"
        managed = True
        unique_together = ('client', 'attribute_id', 'language_id')


class OrgNodeTypes(models.Model):
    """
    Table contains node types/functions
    """
    node_type_guid = models.CharField(primary_key=True, db_column='NODE_TYPE_GUID', max_length=32)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    node_type = models.CharField(db_column='NODE_TYPE', max_length=10, null=False)
    description = models.CharField(db_column='DESCRIPTION', max_length=30, null=False)
    org_node_types_created_by = models.CharField(db_column='ORG_NODE_TYPES_CREATED_BY', max_length=30, null=True)
    org_node_types_created_at = models.DateTimeField(db_column='ORG_NODE_TYPES_CREATED_AT', max_length=50, null=True)
    org_node_types_changed_by = models.CharField(db_column='ORG_NODE_TYPES_CHANGED_BY', max_length=30, null=True)
    org_node_types_changed_at = models.DateTimeField(db_column='ORG_NODE_TYPES_CHANGED_AT', max_length=50, null=True)
    del_ind = models.BooleanField(default=False, null=False)

    class Meta:
        unique_together = ('client', 'node_type')
        db_table = "MDD_ORG_NODETYPES"
        managed = True

    def __str__(self):
        return self.node_type


class OrgModelNodetypeConfig(models.Model):
    """
    based on node type get node types and attribute  drop down
    """
    org_model_nodetype_config_guid = models.CharField(db_column='ORG_MODEL_NODETYPE_CONFIG_GUID', max_length=32,
                                                      primary_key=True)
    org_model_types = models.CharField(db_column='ORG_MODEL_TYPES', max_length=30)
    node_values = models.CharField(db_column='NODE_VALUES', max_length=50)
    node_type = models.CharField(db_column='NODE_TYPES', max_length=10, null=True)
    org_model_nodetype_config_created_by = models.CharField(db_column='ORG_MODEL_NODETYPE_CONFIG_CREATED_BY',
                                                            max_length=30, null=True)
    org_model_nodetype_config_created_at = models.DateTimeField(db_column='ORG_MODEL_NODETYPE_CONFIG_CREATED_AT',
                                                                max_length=50, null=True)
    org_model_nodetype_config_changed_by = models.CharField(db_column='ORG_MODEL_NODETYPE_CONFIG_CHANGED_BY',
                                                            max_length=30, null=True)
    org_model_nodetype_config_changed_at = models.DateTimeField(db_column='ORG_MODEL_NODETYPE_CONFIG_CHANGED_AT',
                                                                max_length=50, null=True)
    del_ind = models.BooleanField(default=False, null=False)
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)

    class Meta:
        db_table = "MDD_ORG_NODETYPE_CONFIG"
        managed = True
        unique_together = ('client', 'org_model_types', 'node_values', 'node_type')


class UserRoles(models.Model):
    role = models.CharField(db_column='ROLES', primary_key=True, max_length=40)
    role_desc = models.CharField(db_column='ROLE_DESC', max_length=60, null=False)
    user_roles_created_by = models.CharField(db_column='USER_ROLES_CREATED_BY', max_length=30, null=True)
    user_roles_created_at = models.DateTimeField(db_column='USER_ROLES_CREATED_AT', max_length=50, null=True)
    user_roles_changed_by = models.CharField(db_column='USER_ROLES_CHANGED_BY', max_length=30, null=True)
    user_roles_changed_at = models.DateTimeField(db_column='USER_ROLES_CHANGED_AT', max_length=50, null=True)
    del_ind = models.BooleanField(default=False, null=False)

    class Meta:
        db_table = 'MDD_ROLES'
        managed = True


class TransactionTypes(models.Model):
    guid = models.CharField(db_column='GUID', primary_key=True, max_length=32)
    transaction_type = models.CharField(db_column='TRANSACTION_TYPE', null=False, max_length=10)
    description = models.CharField(db_column='DESCRIPTION', max_length=255, null=False)
    sequence = models.CharField(db_column='SEQUENCE', max_length=5, null=False)
    active_inactive = models.BooleanField(db_column='ACTIVE_INACTIVE', null=False)
    transaction_types_created_by = models.CharField(db_column='TRANSACTION_TYPES_CREATED_BY', max_length=30, null=True)
    transaction_types_created_at = models.DateTimeField(db_column='TRANSACTION_TYPES_CREATED_AT', max_length=50,
                                                        null=True)
    transaction_types_changed_by = models.CharField(db_column='TRANSACTION_TYPES_CHANGED_BY', max_length=30, null=True)
    transaction_types_changed_at = models.DateTimeField(db_column='TRANSACTION_TYPES_CHANGED_AT', max_length=50,
                                                        null=True)
    del_ind = models.BooleanField(default=False, null=False, db_column='DEL_IND')
    client = models.ForeignKey('eProc_Configuration.OrgClients', on_delete=models.PROTECT, null=False)
    document_type = models.ForeignKey('eProc_Configuration.DocumentType', on_delete=models.DO_NOTHING,
                                      db_column='DOCUMENT_TYPE', null=False)

    class Meta:
        db_table = 'MDD_TRANSACTION_TYPES'
        unique_together = ('client', 'transaction_type', 'document_type', 'sequence')
        managed = True
