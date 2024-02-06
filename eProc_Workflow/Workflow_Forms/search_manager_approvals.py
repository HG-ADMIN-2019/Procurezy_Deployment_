from django import forms


class SearchManagerApprovalsForm(forms.Form):
    doc_types = (
        ('DOC01', 'Shopping Cart'),
        ('DOC02', 'Purchase Order')
    )
    document_type = forms.ChoiceField(label='Select Document Type', choices=doc_types,
                                      widget=forms.Select(attrs={'class': 'form-control'}))
    document_number = forms.CharField(label='Document Number', required=False,
                                      widget=forms.TextInput(attrs={'class': 'form-control check_number_search mandatory_fields'}))
    cart_name = forms.CharField(label='Cart Name', required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control check_for_search mandatory_fields'}))
    timeframe = (
        ('Today', 'Today'),
        ('7', 'Last 7 Days'),
        ('30', 'Last 30 Days'),
        ('90', 'Last 90 Days')
    )
    time_frame = forms.ChoiceField(
        label='Select Time Frame', choices=timeframe, widget=forms.Select(attrs={'class': 'form-control'}),
    )
    status = forms.ChoiceField(label='Status', widget=forms.Select(attrs={'class': 'form-control'}))
