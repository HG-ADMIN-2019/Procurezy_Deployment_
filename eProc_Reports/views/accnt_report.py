"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    accnt_report.py
Usage: Read the account assignment data from the for the selected company code,
        account assignment category and language

Author:
    Varsha
"""

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

from eProc_Configuration.models import AccountingData, AccountingDataDesc
from eProc_Reports.Utilities.reports_generic import *



