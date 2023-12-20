from django import forms
import django
from eProc_Basic.Utilities.constants.constants import CONST_IC, CONST_IO
from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Basic.Utilities.messages.messages import *
from eProc_Configuration.models import Currency
from eProc_Shopping_Cart.models import *
import datetime

regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')


class CreateLimitOrderForm(forms.Form):
    item_name = forms.CharField(max_length=40,
                                required=True,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))

    currency = forms.ModelChoiceField(
        queryset=Currency.objects.order_by('currency_id').values_list('currency_id', flat=True).distinct(),
        empty_label="Select", widget=forms.Select(attrs={'class': 'form-control'}))

    overall_limit = forms.DecimalField \
        (widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'type': 'number'}),
         max_value=9999999999.99,
         max_digits=9999999999,
         decimal_places=2,
         required=True

         )

    expected_value = forms.DecimalField \
        (widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'type': 'number'}),
         max_value=9999999999.99,
         max_digits=9999999999,
         decimal_places=2,
         required=True
         )

    Date = (
        ('', 'Select'),
        ('Between', 'Between'),
        ('On', 'On'),
        ('From', 'From')
    )

    required = forms.CharField(widget=forms.Select(choices=Date, attrs={"onchange": 'Hide(this.value)',
                                                                        'class': 'form-control'}))

    from_date = forms.DateField(
        widget=forms.DateInput
        (attrs={'type': 'date', 'class': 'form-control', 'style': 'display:none', 'min': datetime.date.today(),
                'max': '9999-12-12'}),
        required=False,
    )

    to_date = forms.DateField(
        widget=forms.DateInput
        (attrs={'type': 'date', 'class': 'form-control', 'style': 'display:none', 'min': datetime.date.today(),
                'max': '9999-12-12'}),
        label='To Date',
        required=False
    )

    on_date = forms.DateField(
        widget=forms.DateInput
        (attrs={'type': 'date', 'class': 'form-control', 'style': 'display:none', 'min': datetime.date.today(),
                'max': '9999-12-12'}),
        label='To Date',
        required=False,
    )

    followup_action = (
        ('', 'Select'),
        (CONST_IC, CONST_IC),
        (CONST_IO, CONST_IO)
    )

    follow_up_action = forms.CharField(widget=forms.Select(choices=followup_action, attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        item_name = cleaned_data.get('item_name')
        currency = cleaned_data.get('currency')
        overall_limit = cleaned_data.get('overall_limit')
        expected_value = cleaned_data.get('expected_value')
        frm_date = cleaned_data.get('from_date')
        to_date = cleaned_data.get('to_date')
        on_date = cleaned_data.get('on_date')
        required = cleaned_data.get('required')
        follow_up_actions = cleaned_data.get('follow_up_action')

        if len(item_name) < 3 or len(item_name) == 0:
            error_msg = get_message_desc(MSG020)[1]
            # msgid = 'MSG020'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            raise forms.ValidationError(error_msg)
            # raise forms.ValidationError(MSG020)

        if regex.search(item_name):
            error_msg = get_message_desc(MSG026)[1]
            # msgid = 'MSG026'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            raise forms.ValidationError(error_msg)
            # raise forms.ValidationError(MSG026)

        if currency is None:
            error_msg = get_message_desc(MSG030)[1]
            # msgid = 'MSG030'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg

            raise forms.ValidationError(error_msg)
            # raise forms.ValidationError(MSG030)

        if expected_value > overall_limit:
            error_msg = get_message_desc(MSG038)[1]
            # msgid = 'MSG038'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            raise forms.ValidationError(error_msg)
            # raise forms.ValidationError(MSG038)

        if required == 'From':
            if frm_date is not None:
                if frm_date < django.utils.timezone.now().date():
                    error_msg = get_message_desc(MSG031)[1]
                    # msgid = 'MSG031'
                    # error_msg = get_msg_desc(msgid)
                    # msg = error_msg['message_desc'][0]
                    # error_msg = msg
                    raise forms.ValidationError(error_msg)
                    # raise forms.ValidationError(MSG031)

            if frm_date is None:
                error_msg = get_message_desc(MSG039)[1]
                # msgid = 'MSG039'
                # error_msg = get_msg_desc(msgid)
                # msg = error_msg['message_desc'][0]
                # error_msg = msg
                raise forms.ValidationError(error_msg)
                # raise forms.ValidationError(MSG039)

        if required == 'Between':
            if frm_date is not None and to_date is not None:
                if to_date < frm_date < datetime.date.today():
                    error_msg = get_message_desc(MSG015)[1]
                    # msgid = 'MSG015'
                    # error_msg = get_msg_desc(msgid)
                    # msg = error_msg['message_desc'][0]
                    # error_msg = msg
                    raise forms.ValidationError(error_msg)
                    # raise forms.ValidationError(MSG015)

            if frm_date is not None and to_date is not None:
                if frm_date < datetime.date.today() or to_date < datetime.date.today():
                    error_msg = get_message_desc(MSG033)[1]
                    # msgid = 'MSG033'
                    # error_msg = get_msg_desc(msgid)
                    # msg = error_msg['message_desc'][0]
                    # error_msg = msg
                    raise forms.ValidationError(error_msg)
                    # raise forms.ValidationError(MSG033)

            if frm_date is None or to_date is None:
                error_msg = get_message_desc(MSG040)[1]
                # msgid = 'MSG040'
                # error_msg = get_msg_desc(msgid)
                # msg = error_msg['message_desc'][0]
                # error_msg = msg
                raise forms.ValidationError(error_msg)
                # raise forms.ValidationError(MSG040)

        if required == 'On':
            if on_date is None:
                error_msg = get_message_desc(MSG039)[1]
                # msgid = 'MSG039'
                # error_msg = get_msg_desc(msgid)
                # msg = error_msg['message_desc'][0]
                # error_msg = msg
                raise forms.ValidationError(error_msg)
                # raise forms.ValidationError(MSG039)

            if on_date is not None:
                if on_date < datetime.date.today():
                    error_msg = get_message_desc(MSG039)[1]
                    # msgid = 'MSG039'
                    # error_msg = get_msg_desc(msgid)
                    # msg = error_msg['message_desc'][0]
                    # error_msg = msg
                    raise forms.ValidationError(error_msg)
                    # raise forms.ValidationError(MSG039)

        if required == 'None':
            error_msg = get_message_desc(MSG039)[1]
            # msgid = 'MSG039'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            raise forms.ValidationError(error_msg)
            # raise forms.ValidationError(MSG039)

        if follow_up_actions == 'None':
            error_msg = get_message_desc(MSG041)[1]
            # msgid = 'MSG041'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            raise forms.ValidationError(error_msg)
            # raise forms.ValidationError(MSG041)


# Creating Model Form for updating Limit Item
class UpdateLimitItem(forms.ModelForm):
    description = forms.CharField(max_length=40,
                                  required=False,
                                  widget=forms.TextInput(attrs={'class': 'hg_updateInputField'}),
                                  label='Item Name'
                                  )

    overall_limit = forms.DecimalField \
        (widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'min': 1, 'type': 'number'}),
         max_value=9999999999.99,
         max_digits=9999999999,
         decimal_places=2,
         required=True)

    expected_value = forms.DecimalField \
        (widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'min': 1, 'type': 'number'}),
         max_value=9999999999.99,
         max_digits=9999999999,
         decimal_places=2,
         required=True)

    def clean(self):
        cleaned_data = super().clean()
        item_name = cleaned_data.get('description')
        overall_limit = cleaned_data.get('overall_limit')
        expected_value = cleaned_data.get('expected_value')
        follow_up_actions = cleaned_data.get('follow_up_action')

        if len(item_name) < 3 or len(item_name) == 0:
            error_msg = get_message_desc(MSG005)[1]
            # msgid = 'MSG020'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            raise forms.ValidationError(error_msg)
            # raise forms.ValidationError(MSG020)

        if regex.search(item_name):
            error_msg = get_message_desc(MSG026)[1]
            # msgid = 'MSG026'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            raise forms.ValidationError(error_msg)
            # raise forms.ValidationError(MSG026)

        if follow_up_actions == 'None':
            error_msg = get_message_desc(MSG041)[1]
            # msgid = 'MSG041'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            raise forms.ValidationError(error_msg)
            # raise forms.ValidationError(MSG041)

        if expected_value > overall_limit:
            error_msg = get_message_desc(MSG038)[1]
            # msgid = 'MSG038'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            raise forms.ValidationError(error_msg)
            # raise forms.ValidationError(MSG038)

    class Meta:
        model = CartItemDetails
        fields = ['description', 'overall_limit', 'expected_value']
        labels = {
            'overall_limit': 'Overall Limit',
            'expected_value': 'Expected Value',
        }

        widgets = {
            'ir_gr_ind': forms.CharField(widget=forms.HiddenInput(), required=False),
            'gr_flag': forms.CharField(widget=forms.HiddenInput(), required=False),
            'start_date': forms.CharField(widget=forms.HiddenInput(), required=False),
            'end_date': forms.CharField(widget=forms.HiddenInput(), required=False),
            'item_del_date': forms.CharField(widget=forms.HiddenInput(), required=False),
            'supp_id': forms.HiddenInput(),
            'prod_cat': forms.HiddenInput(),
            'currency': forms.HiddenInput
        }
