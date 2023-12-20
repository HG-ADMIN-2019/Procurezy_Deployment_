from django import forms


class ProjectSearchFrom(forms.Form):

    Projectname = forms.CharField(label='ProjectName', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Project_Desc = forms.CharField(label='Project Desc', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Start_Date = forms.DateField(label='Start Date', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    End_Date = forms.DateField(label='End date', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    Project_id = forms.CharField(label='Project ID', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))