# # The purpose of a form is to give users a chance to enter data and submit it to a server.
# # Form for Approval Reports
#
# # Importing the Django standard libraries
# from django import forms
#
# from eProc_Basic.models import AccountAssignmentCategory
#
#
# class ApprovalReportForm(forms.Form):
#
#     comp_list = (
#         ('5000', '5000'),
#         ('3000', '3000')
#     )
#
#     comp_code_app = forms.ChoiceField(label='Company Code', required=False, choices=comp_list,
#                                       widget=forms.Select(attrs={'class':'choiceField'}))
#
#     acc_list = (('zz', 'zz'), ('yy', 'yy'))
#
#     acc_assgn_cat = forms.ChoiceField(label='Account Assignment Category', required=False, choices=acc_list,
#                                       widget=forms.Select(attrs={'class': 'choiceField'}))
#
#     #acc_assgn_cat = forms.ModelChoiceField(
#     #    queryset=AccountAssignmentCategory.objects.order_by('account_assign_cat').values_list('account_assign_cat', flat=True).distinct(),
#     #    empty_label="None", widget=forms.Select(attrs={'style': 'width:476px; height:31px; border-radius:2px;'}))
#
#
#     def clean(self):
#         cleaned_data = super(ApprovalReportForm, self).clean()
#
