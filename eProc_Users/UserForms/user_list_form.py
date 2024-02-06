from django import forms
from eProc_Configuration.models import Country


class UserListForm(forms.Form):
    user_types = (
        ('USER', 'USER'),
        ('SUPPLIER', 'SUPPLIER')
    )

    select_type = forms.ChoiceField(label='Select User Type', required=False, choices=user_types, widget=forms.Select(
        attrs={"onchange": 'userTypeChanged(this.value)', 'class': 'form-control', 'style': 'width:28%; '
                                                                                            'margin-bottom:40px;'}))

    employee_id = forms.CharField(label='Employee ID', required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'style': 'width:100%;float:left;margin-right: 30px;'}))
    username = forms.CharField(label='Username', required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'style': 'width:100%;float:left;margin-right: 30px;'}))

    emp_user_type = forms.ChoiceField(label='User Type', required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'style': 'width:100%;float:left;margin-right: 30px;'}), disabled=True)

    first_name = forms.CharField(label='First Name', required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'style': 'width:100%;float:left;margin-right: 30px;'}))
    last_name = forms.CharField(label='Last Name', required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'style': 'width:100%;float:left;margin-right: 30px;'}))

    user_locked = forms.CharField(label='User Locked', required=False, widget=forms.CheckboxInput(
        attrs={'class': 'form-control', 'style': 'width:20px; height:20px; float:left;margin-right: 30px;'}))
    password_locked = forms.CharField(label='Password Locked', required=False, initial=False,
                                      widget=forms.CheckboxInput(attrs={'class': 'form-control',
                                                                        'style': 'width:20px; height:20px; '
                                                                                 'float:left;margin-right: 30px;'}))
    active = forms.CharField(label='Active', required=False, widget=forms.CheckboxInput(
        attrs={'class': 'form-control', 'style': 'width:20px; height:20px; float:left;margin-right: 30px;'}))

    supplier_id = forms.CharField(label='Supplier ID', max_length=20, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'style': 'width:100%;float:left;margin-right: 30px;'}))
    search_term1 = forms.CharField(label='Search Term1', max_length=20, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'style': 'width:100%;float:left;margin-right: 30px;'}))
    search_term2 = forms.CharField(label='Search Term2', max_length=20, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'style': 'width:100%;float:left;margin-right: 30px;'}))
    country = forms.ModelChoiceField(queryset=Country.objects.all(), empty_label='Select', label='Country',
                                     required=False, widget=forms.Select(
            attrs={'class': 'form-control', 'style': 'width:100%;float:left;margin-right: 30px;'}))
    city = forms.CharField(label='City', required=False, max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control', 'style': 'width:100%;float:left;margin-right: 30px;'}))
    purch_org = forms.CharField(label='Purchasing Org', required=False, max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control', 'style': 'width:100%;float:left;margin-right: 30px;'}), disabled=True)
    purch_org_id = forms.CharField(label='Purchasing Org id', max_length=20, required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'style': 'width:100%;float:left;margin-right: 30px;'}), disabled=True)
    purch_block = forms.CharField(label='Purchase Block', required=False,
                                  widget=forms.CheckboxInput(attrs={'style': 'float:left;margin-right: 30px;'}),
                                  disabled=True)

    def clean(self):
        cleaned_data = super(UserListForm, self).clean()
