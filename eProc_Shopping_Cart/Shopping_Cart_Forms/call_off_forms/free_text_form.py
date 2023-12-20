import datetime
import django
from django import forms

from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Basic.Utilities.messages.messages import *
from eProc_Form_Builder.models.form_builder import EformFieldData
from eProc_Shopping_Cart.models import *


class CreateFreeText(forms.Form):
    product_name = forms.CharField(max_length=40, min_length=3,
                                   required=True,
                                   widget=forms.TextInput(attrs={'class': 'form-control check_product_name'}))

    description = forms.CharField(max_length=255, widget=forms.Textarea(attrs={'class': 'form-control ',
                                                                               'style': 'height:40px'}))

    price_unit = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control check_number', 'min': 1, 'type': 'number'}),
        max_value=9999999.99,
        max_digits=9999999.99,
        decimal_places=2,
        required=True)
    price = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control check_price', 'min': 1, 'type': 'number'}),
        max_value=9999999.99,
        max_digits=9999999.99,
        decimal_places=2,
        required=True)

    delivery_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'min': datetime.date.today(),
                                      'max': '9999-12-12'}),
        required=True,
    )

    quantity = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control check_number', 'min': 1, 'type': 'number'}))

    def clean(self):
        cleaned_data = super().clean()
        product_name = cleaned_data.get('product_name')
        description = cleaned_data.get('description')
        delivery_date = cleaned_data.get('delivery_date')
        quantity = cleaned_data.get('quantity')

        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        if len(product_name) < 3:
            error_msg = get_message_desc(MSG020)[1]
            # msgid = 'MSG020'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            raise forms.ValidationError(error_msg)
            # raise forms.ValidationError(MSG020)


        if regex.search(product_name):
            error_msg = get_message_desc(MSG026)[1]
            # msgid = 'MSG026'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            raise forms.ValidationError(error_msg)
            # raise forms.ValidationError(MSG026)

        if len(description) > 250:
            error_msg = get_message_desc(MSG024)[1]
            # msgid = 'MSG024'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            raise forms.ValidationError(error_msg)
            # raise forms.ValidationError(MSG024)

        # Date range validation
        if delivery_date is None:
            raise forms.ValidationError(' Please enter delivery date')

        if delivery_date < django.utils.timezone.now().date():
            error_msg = get_message_desc(MSG024)[1]
            # msgid = 'MSG024'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            raise forms.ValidationError(error_msg)
            # raise forms.ValidationError(MSG024)

        if len(quantity) > 7:
            error_msg = get_message_desc(MSG025)[1]
            # msgid = 'MSG025'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            raise forms.ValidationError(error_msg)
            # raise forms.ValidationError(MSG025)


# Creating Model Form for updating Freetext Item
class UpdateFreeText(forms.ModelForm):
    description = forms.CharField(max_length=40, label='Product Name', widget=forms.TextInput(
        attrs={'style': 'width:100%;'
                        'height:25px;'
                        'border-radius:2px;', 'class': 'check_product_name'}))

    prod_desc = forms.CharField(label='Product Description', max_length=250,
                                widget=forms.Textarea(attrs={'style': 'width:100%;'
                                                                      'height:25px;'
                                                                      'border-radius:2px;'}))

    price = forms.DecimalField(widget=forms.NumberInput(attrs={'style': 'width:100%;'
                                                                        'height:25px;'
                                                                        'border-radius:2px;', 'min': 1,
                                                               'type': 'number',
                                                               'class': 'check_price'}),
                               max_value=9999999999.99,
                               max_digits=9999999999,
                               decimal_places=2,
                               required=True)

    item_del_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'style': 'width:100%;'
                                                               'height:25px;'
                                                               'border-radius:2px;', 'min': datetime.date.today()}),
        required=True,
    )
    quantity = forms.CharField(label='Quantity', widget=forms.TextInput(
        attrs={'style': 'width:100%;'
                        'height:25px;'
                        'border-radius:2px;', 'min': 1, 'type': 'number', 'class': 'check_number'}))

    def clean(self):
        cleaned_data = super().clean()
        description = cleaned_data.get('description')
        prod_desc = cleaned_data.get('prod_cat_desc')
        price = cleaned_data.get('price')
        item_del_date = cleaned_data.get('item_del_date')
        quantity = cleaned_data.get('quantity')

        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        # To restrict the wildcard search to 3 characters and form fields validations
        if len(description) < 3:
            error_msg = get_message_desc(MSG020)[1]
            # msgid = 'MSG020'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            raise forms.ValidationError(error_msg)
            # raise forms.ValidationError(MSG020)

        if regex.search(description):
            error_msg = get_message_desc(MSG026)[1]
            # msgid = 'MSG026'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            raise forms.ValidationError(error_msg)
            # raise forms.ValidationError(MSG026)

        if len(prod_desc) > 250:
            error_msg = get_message_desc(MSG021)[1]
            # msgid = 'MSG021'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            raise forms.ValidationError(error_msg)
            # raise forms.ValidationError(MSG021)

        # Date range validation
        if item_del_date is None:
            error_msg = get_message_desc(MSG024)[1]
            # msgid = 'MSG024'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            raise forms.ValidationError(error_msg)
            # raise forms.ValidationError(MSG024)

        if len(quantity) > 14:
            error_msg = get_message_desc(MSG025)[1]
            # msgid = 'MSG025'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            raise forms.ValidationError(error_msg)
            # raise forms.ValidationError(MSG025)

    class Meta:
        model = CartItemDetails
        fields = ['description', 'prod_cat_desc', 'price', 'item_del_date', 'quantity']
        widgets = {
            'unit': forms.HiddenInput()
        }


# Creating Model Form for updating Eform Data
class UpdateEform(forms.ModelForm):
    form_field1 = forms.CharField(widget=forms.TextInput(
        attrs={'style': 'width:100%;'
                        'height:25px;'
                        'border-radius:2px;'}))
    form_field2 = forms.CharField(widget=forms.TextInput(
        attrs={'style': 'width:100%;'
                        'height:25px;'
                        'border-radius:2px;'}))
    form_field3 = forms.CharField(widget=forms.TextInput(
        attrs={'style': 'width:100%;'
                        'height:25px;'
                        'border-radius:2px;'}))
    form_field4 = forms.CharField(widget=forms.TextInput(
        attrs={'style': 'width:100%;'
                        'height:25px;'
                        'border-radius:2px;'}))
    form_field5 = forms.CharField(widget=forms.TextInput(
        attrs={'style': 'width:100%;'
                        'height:25px;'
                        'border-radius:2px;'}))
    form_field6 = forms.CharField(widget=forms.TextInput(
        attrs={'style': 'width:100%;'
                        'height:25px;'
                        'border-radius:2px;'}))
    form_field7 = forms.CharField(widget=forms.TextInput(
        attrs={'style': 'width:100%;'
                        'height:25px;'
                        'border-radius:2px;'}))
    form_field8 = forms.CharField(widget=forms.TextInput(
        attrs={'style': 'width:100%;'
                        'height:25px;'
                        'border-radius:2px;'}))
    form_field9 = forms.CharField(widget=forms.TextInput(
        attrs={'style': 'width:100%;'
                        'height:25px;'
                        'border-radius:2px;'}))
    form_field10 = forms.CharField(widget=forms.TextInput(
        attrs={'style': 'width:100%;'
                        'height:25px;'
                        'border-radius:2px;'}))

    class Meta:
        model = EformFieldData
        fields = ['form_field1', 'form_field2', 'form_field3', 'form_field4', 'form_field5', 'form_field6',
                  'form_field7', 'form_field8', 'form_field9', 'form_field10']

    def __init__(self, *args, **kwargs):
        super(UpdateEform, self).__init__(*args, **kwargs)
        self.fields['form_field1'].required = False
        self.fields['form_field2'].required = False
        self.fields['form_field3'].required = False
        self.fields['form_field4'].required = False
        self.fields['form_field5'].required = False
        self.fields['form_field6'].required = False
        self.fields['form_field7'].required = False
        self.fields['form_field8'].required = False
        self.fields['form_field9'].required = False
        self.fields['form_field10'].required = False
