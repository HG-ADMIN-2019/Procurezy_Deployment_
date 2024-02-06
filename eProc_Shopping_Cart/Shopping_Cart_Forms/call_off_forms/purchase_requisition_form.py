from django import forms

from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Basic.Utilities.messages.messages import *
from eProc_Configuration.models import *
from eProc_Shopping_Cart.models import *

regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')


class CreatePurchaseReqForm(forms.Form):
    prod_name = forms.CharField(max_length=40,
                                required=True,
                                label='Product Name',
                                widget=forms.TextInput(attrs={'class': 'form-control'})
                                )

    prod_desc = forms.CharField(
        required=True,
        max_length=250,
        label='Product Description',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    prod_id = forms.CharField(
        required=False,
        max_length=10,
        label='Product ID',
        widget=forms.TextInput(attrs={'class': 'form-control', 'min': 1, 'type': 'number'})
    )

    prod_prz = forms.DecimalField(label='Price',
                                  widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'type': 'number'}),
                                  max_value=9999999999.99,
                                  max_digits=9999999999,
                                  decimal_places=2,
                                  required=True
                                  )

    currency = forms.ModelChoiceField(
        queryset=Currency.objects.order_by('currency_id').values_list('currency_id', flat=True).distinct(),
        empty_label="Please select...", widget=forms.Select(attrs={'class': 'form-control'}))

    lead_time = forms.CharField(
        required=True,
        label='Lead Time',
        max_length=3,
        widget=forms.NumberInput(attrs={'class': 'form-control',
                                        'min': 1})
    )

    quantity = forms.CharField(
        required=True,
        label='Quantity',
        widget=forms.NumberInput(attrs={'class': 'form-control',
                                        'type': 'number',
                                        'min': 1})
    )

    def clean(self):
        preq_cleaned = super().clean()
        prd_name = preq_cleaned.get('prod_name')
        prd_prz = preq_cleaned.get('prod_prz')
        lead_time = preq_cleaned.get('lead_time')

        if len(prd_name) < 3:
            error_msg = get_message_desc(MSG020)[1]
            # msgid = 'MSG020'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            raise forms.ValidationError(error_msg)
            # raise forms.ValidationError(MSG020)

        if regex.search(prd_name):
            error_msg = get_message_desc(MSG026)[1]
            # msgid = 'MSG026'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            raise forms.ValidationError(error_msg)

            # raise forms.ValidationError(MSG026)


# Creating Model Form for updating Purchase Requisition
class UpdatePurchaseReq(forms.ModelForm):
    description = forms.CharField(
        max_length=40,
        required=True,
        label='Product Name',
        widget=forms.TextInput(attrs={'style': 'width:100%;'
                                               'height:25px;'
                                               'border-radius:2px;'})
    )

    prod_desc = forms.CharField(
        required=True,
        label='Product Description',
        widget=forms.TextInput(attrs={'style': 'width:100%;'
                                               'height:25px;'
                                               'border-radius:2px;'})
    )

    int_product_id = forms.CharField(
        required=False,
        label='Product ID',
        widget=forms.TextInput(attrs={'style': 'width:100%;'
                                               'height:25px;'
                                               'border-radius:2px;', 'min': 1})
    )

    price = forms.DecimalField(widget=forms.NumberInput(attrs={'style': 'width:100%;'
                                                                        'height:25px;'
                                                                        'border-radius:2px;', 'min': 1,
                                                               'type': 'number'}),
                               max_value=9999999999.99,
                               max_digits=9999999999,
                               decimal_places=2,
                               required=True)

    currency = forms.ModelChoiceField(
        queryset=Currency.objects.order_by('currency_id').values_list('currency_id', flat=True).distinct(),
        empty_label="Please select...", widget=forms.Select(attrs={'style': 'width:102%;'
                                                                            'height:31px;'
                                                                            'border-radius:2px;'}))

    lead_time = forms.CharField(
        required=True,
        max_length=3,
        label='Lead Time',
        widget=forms.NumberInput(attrs={'style': 'width:100%;'
                                                 'height:25px;'
                                                 'border-radius:2px;', 'type': 'number', 'min': 1,
                                        'class': 'check_number'})
    )

    quantity = forms.CharField(
        required=True,
        label='Quantity',
        widget=forms.NumberInput(attrs={'style': 'width:100%;'
                                                 'height:25px;'
                                                 'border-radius:2px;',
                                        'type': 'number',
                                        'min': 1, 'class': 'check_number'})
    )

    class Meta:
        model = CartItemDetails
        fields = ['description', 'prod_cat_desc', 'int_product_id', 'price', 'currency', 'lead_time', 'quantity']
        labels = {
            "description": "Product Name",
            "prod_cat_desc": "Product Description",
            "int_product_id": "Product Id",
            "price": "Price",
            "currency": "Currency",
            "item_del_date": "Item Delivery Date"
        }

        widgets = {
            'prod_cat': forms.HiddenInput(),
            'unit': forms.HiddenInput()
        }
