import re
from django import forms
from eProc_Basic.Utilities.functions.mathematical_symbols import validationMathSymbols
from eProc_Basic.Utilities.functions.messages_config import get_msg_desc, get_message_desc
from eProc_Basic.Utilities.messages.messages import MSG019, MSG036, MSG042


class FreeTextFormConf(forms.Form):
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Supplier Description')
    supp_art_no = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Supplier Article No')
    lead_time = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'min': 1}),
                                max_length=3, label='Lead Time')
    cat_id = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Catalog Id')
    form_field1 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:70%'}),
                                  label='Form Field 1', required=False)
    form_field2 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:70%'}),
                                  label='Form Field 2', required=False)
    form_field3 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:70%'}),
                                  label='Form Field 3', required=False)
    form_field4 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:70%'}),
                                  label='Form Field 4', required=False)
    form_field5 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:70%'}),
                                  label='Form Field 5', required=False)
    form_field6 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:70%'}),
                                  label='Form Field 6', required=False)
    form_field7 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:70%'}),
                                  label='Form Field 7', required=False)
    form_field8 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:70%'}),
                                  label='Form Field 8', required=False)
    form_field9 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:70%'}),
                                  label='Form Field 9', required=False)
    form_field10 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:70%'}),
                                   label='Form Field 10', required=False)
    check_box1 = forms.BooleanField(label='Required', required=False,
                                    widget=forms.CheckboxInput(attrs={'class': 'hg_check_box_inp'}))
    check_box2 = forms.BooleanField(label='Required', required=False,
                                    widget=forms.CheckboxInput(attrs={'class': 'hg_check_box_inp'}))
    check_box3 = forms.BooleanField(label='Required', required=False,
                                    widget=forms.CheckboxInput(attrs={'class': 'hg_check_box_inp'}))
    check_box4 = forms.BooleanField(label='Required', required=False,
                                    widget=forms.CheckboxInput(attrs={'class': 'hg_check_box_inp'}))
    check_box5 = forms.BooleanField(label='Required', required=False,
                                    widget=forms.CheckboxInput(attrs={'class': 'hg_check_box_inp'}))
    check_box6 = forms.BooleanField(label='Required', required=False,
                                    widget=forms.CheckboxInput(attrs={'class': 'hg_check_box_inp'}))
    check_box7 = forms.BooleanField(label='Required', required=False,
                                    widget=forms.CheckboxInput(attrs={'class': 'hg_check_box_inp'}))
    check_box8 = forms.BooleanField(label='Required', required=False,
                                    widget=forms.CheckboxInput(attrs={'class': 'hg_check_box_inp'}))
    check_box9 = forms.BooleanField(label='Required', required=False,
                                    widget=forms.CheckboxInput(attrs={'class': 'hg_check_box_inp'}))
    check_box10 = forms.BooleanField(label='Required', required=False,
                                     widget=forms.CheckboxInput(attrs={'class': 'hg_check_box_inp'}))

    def clean(self):
        cleaned_data = super().clean()
        description = cleaned_data.get('description')
        supp_art_no = cleaned_data.get('supp_art_no')
        lead_time = cleaned_data.get('lead_time')
        cat_id = cleaned_data.get('cat_id')
        form_field1 = cleaned_data.get('form_field1')
        form_field2 = cleaned_data.get('form_field2')
        form_field3 = cleaned_data.get('form_field3')
        form_field4 = cleaned_data.get('form_field4')
        form_field5 = cleaned_data.get('form_field5')
        form_field6 = cleaned_data.get('form_field7')
        form_field7 = cleaned_data.get('form_field7')
        form_field8 = cleaned_data.get('form_field8')
        form_field9 = cleaned_data.get('form_field9')
        form_field10 = cleaned_data.get('form_field10')

        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')

        check_mathematical_symbols = validationMathSymbols(description)
        if check_mathematical_symbols:
            error_msg = get_message_desc(MSG036)[1]
            # msgid = 'MSG036'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            raise forms.ValidationError(error_msg)
            # raise forms.ValidationError(MSG036)

        if regex.search(cat_id):
            error_msg = get_message_desc(MSG019)[1]
            # msgid = 'MSG019'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            raise forms.ValidationError(error_msg)
            # raise forms.ValidationError(MSG019)

        if len(lead_time) > 3:
            error_msg = get_message_desc(MSG042)[1]
            # msgid = 'MSG042'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            raise forms.ValidationError(error_msg)
            # raise forms.ValidationError(MSG042)

        if regex.search(form_field1):
            error_msg = get_message_desc(MSG019)[1]
            # msgid = 'MSG019'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            raise forms.ValidationError(error_msg)
            # raise forms.ValidationError(MSG019)

        if regex.search(form_field2):
            error_msg = get_message_desc(MSG019)[1]
            # msgid = 'MSG019'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            raise forms.ValidationError(error_msg)
            # raise forms.ValidationError(MSG019)

        if regex.search(form_field3):
            error_msg = get_message_desc(MSG019)[1]
            # msgid = 'MSG019'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            raise forms.ValidationError(error_msg)
            # raise forms.ValidationError(MSG019)

        if regex.search(form_field4):
            error_msg = get_message_desc(MSG019)[1]
            # msgid = 'MSG019'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            raise forms.ValidationError(error_msg)
            # raise forms.ValidationError(MSG019)

        if regex.search(form_field5):
            error_msg = get_message_desc(MSG019)[1]
            # msgid = 'MSG019'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            raise forms.ValidationError(error_msg)
            # raise forms.ValidationError(MSG019)

        if regex.search(form_field6):
            error_msg = get_message_desc(MSG019)[1]
            # msgid = 'MSG019'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            raise forms.ValidationError(error_msg)
            # raise forms.ValidationError(MSG019)

        if regex.search(form_field7):
            error_msg = get_message_desc(MSG019)[1]
            # msgid = 'MSG019'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            raise forms.ValidationError(error_msg)
            # raise forms.ValidationError(MSG019)

        if regex.search(form_field8):
            error_msg = get_message_desc(MSG019)[1]
            # msgid = 'MSG019'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            raise forms.ValidationError(error_msg)
            # raise forms.ValidationError(MSG019)

        if regex.search(form_field9):
            error_msg = get_message_desc(MSG019)[1]
            # msgid = 'MSG019'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            raise forms.ValidationError(error_msg)
            # raise forms.ValidationError(MSG019)

        if regex.search(form_field10):
            error_msg = get_message_desc(MSG019)[1]
            # msgid = 'MSG019'
            # error_msg = get_msg_desc(msgid)
            # msg = error_msg['message_desc'][0]
            # error_msg = msg
            raise forms.ValidationError(error_msg)
            # raise forms.ValidationError(MSG019)
