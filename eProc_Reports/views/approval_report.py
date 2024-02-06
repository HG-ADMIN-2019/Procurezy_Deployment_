"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    approval_report.py
Usage: Reads the workflow approver details according to the company code
        and account assignment category

Author:
    Varsha
"""

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render

from eProc_Configuration.models import WorkflowSchema, ApproverLimit, ApproverLimitValue, WorkflowACC
from eProc_Reports.Utilities.reports_generic import *



