# The purpose of a form is to give users a chance to enter data and submit it to a server.
# Form for User Reports

# Importing the Django standard libraries
from django import forms
from django.utils.safestring import mark_safe
from datetime import date

from eProc_Configuration.Utilities.application_settings_generic import get_configuration_data
from eProc_Configuration.models import OrgCompanies, FieldTypeDesc


class UserReportForm(forms.Form):
    # User report fields
    user_rep_types = (
        ('Users_in_company', 'Users in Company'),
        ('Substitute', 'Substitute'),
        ('Approval Hierarchy', 'Approval Hierarchy')
    )
    # user_status = FieldTypeDesc.objects.filter(del_ind=False, field_name='ACTIVE_INACTIVE').values('field_type_id')
    # print(user_status['field_type_id'])
    # for status in user_status:
    #     user_status_data = ((status['field_type_id'], status['field_type_id']))
    user_status_data = (('Active', 'Active'), ('Inactive', 'Inactive'))
    userrep_type = forms.ChoiceField(label='Select Report', choices=user_rep_types, required=False, disabled=True,
                                     widget=forms.Select(
                                         attrs={'class': 'form-control', "onchange": 'getSubReport(this.value)'}))

    # Users in Company search fields
    company_code = forms.ModelChoiceField(
        label='Company Code',
        required=False,
        queryset=OrgCompanies.objects.filter(del_ind=False),
        empty_label=None,
        widget=forms.Select(attrs={'class': 'form-control'}),
        to_field_name='company_id',  # Use the 'company_id' field as the value for the form field
    )

    username = forms.CharField(label='Username', required=False, widget=forms.TextInput(attrs={
        'class': 'form-control check_for_search mandatory_fields'}))

    active = forms.ChoiceField(label='User Status', choices=user_status_data, required=False, disabled=False,
                               widget=forms.Select(attrs={'class': 'form-control'}))
    ####################################################

    ######## Substitutes in Company search fields ################################
    substitute_types = (
        ('Approval', 'Approval'),
        ('Goods_Receipt', 'Goods Receipt')
    )
    substitute_sub_type = forms.ChoiceField(label='Substitute Type', choices=substitute_types, required=False,
                                            widget=forms.Select(attrs={'class': 'hg_choiceField'}))

    ##############################################################

    def clean(self):
        cleaned_data = super(UserReportForm, self).clean()

    def __init__(self, *args, **kwargs):
        super(UserReportForm, self).__init__(*args, **kwargs)

        # Customize the choices for the company_code field
        self.fields['company_code'].choices = [
            (obj.company_id, f"{obj.company_id} - {obj.name1}")
            for obj in OrgCompanies.objects.filter(del_ind=False)
        ]