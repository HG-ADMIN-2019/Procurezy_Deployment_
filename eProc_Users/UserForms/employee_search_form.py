from django import forms


class EmployeeSearchFrom(forms.Form):

    username = forms.CharField(label='Username', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='First Name', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Last Name', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    employee_id = forms.CharField(label='Employee ID', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    emp_user_type = forms.ChoiceField(label='User Type', required=False)

    user_locked = forms.CharField(label='User Locked', required=False)
    password_locked = forms.CharField(label='Password Locked', required=False)
    active = forms.CharField(label='Active', required=False)
