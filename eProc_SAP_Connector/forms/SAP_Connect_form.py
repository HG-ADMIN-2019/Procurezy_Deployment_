from django import forms


class SapConnectorForm(forms.Form):

    ashost           = forms.CharField(max_length=40,
                                          required=True,
                                          widget = forms.TextInput(attrs={'style' : 'width:469px; height:25px; border-radius:2px;'}))
    sysnr = forms.CharField(required=True,
                             widget=forms.TextInput(attrs={'style': 'width:469px; height:25px; border-radius:2px;'}))
    client = forms.CharField(max_length=40,
                             required=True,
                             widget=forms.TextInput(attrs={'style': 'width:469px; height:25px; border-radius:2px;'}))
    user = forms.CharField(max_length=40,
                             required=True,
                             widget=forms.TextInput(attrs={'style': 'width:469px; height:25px; border-radius:2px;'}))
    passwd = forms.CharField(max_length=40,
                             required=True,
                             widget=forms.TextInput(attrs={'style': 'width:469px; height:25px; border-radius:2px;'}))