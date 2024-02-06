# # The purpose of a form is to give users a chance to enter data and submit it to a server.
# # Form for Account Reports
#
# # Importing the Django standard libraries
# from django import forms
#
#
# class AccountReportForm(forms.Form):
#     comp_list = (
#         ('1000', '1000'),
#         ('2000', '2000')
#     )
#
#     comp_code_app = forms.ChoiceField(label='Company Code', required= False, choices=comp_list,
#                                   widget=forms.Select(attrs={'class' :'choiceField'}))
#
#     acc_list = (
#         ('CC', 'CC'),
#         ('AS', 'AS'))
#
#     acc_assgn_cat = forms.ChoiceField(label='Account Assignment Category', required= False, choices=acc_list,
#                                   widget=forms.Select (attrs={'class' :'choiceField'}))
#
#     lang_list = (('EN','EN'), ('NL', 'NL'),('DE','DE'))
#
#     language = forms.ChoiceField(label='Language', required= False, choices=lang_list,
#                                   widget=forms.Select(attrs={'class' :'choiceField'}))
#
#     def clean(self):
#         cleaned_data = super(AccountReportForm, self).clean()
