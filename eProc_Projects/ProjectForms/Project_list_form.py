from django import forms
from eProc_Configuration.models import Country


class ProjectListForm(forms.Form):
    user_types = (
        ('Project', 'Project'),
        ('ProjectDesc', 'ProjectDesc')
    )

    select_type = forms.ChoiceField(label='Select User Type', required=False, choices=user_types, widget=forms.Select(
        attrs={"onchange": 'userTypeChanged(this.value)', 'class': 'form-control', 'style': 'width:28%; '
                                                                                            'margin-bottom:40px;'}))

    project_id = forms.CharField(label='Project ID', required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'style': 'width:100%;float:left;margin-right: 30px;'}))
    Projectname = forms.CharField(label='Projectname', required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'style': 'width:100%;float:left;margin-right: 30px;'}))

    start_date = forms.DateField(label='Start Date', required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'style': 'width:100%;float:left;margin-right: 30px;'}))
    end_date = forms.DateField(label='End Date', required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'style': 'width:100%;float:left;margin-right: 30px;'}))

    def clean(self):
        cleaned_data = super(ProjectListForm, self).clean()
