"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    user_report.py
Usage:
    SC and PO document search by company code, date range created by and requester
     m_docsearch_meth - This function is used to get header details of shopping cart and purchase order.
Author:
    Varsha
"""
import re

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render
from eProc_Basic.Utilities.functions.get_db_query import display_cart_counter, getClients
from eProc_Basic.Utilities.functions.str_concatenate import concatenate_str
from eProc_Org_Model.models import OrgModel
from eProc_Registration.models import UserData
from eProc_Reports.Report_Forms.SearchDoc_forms import *
from django.utils.translation import gettext_lazy as _

# Function to show the reports main page and search different reports
from eProc_Reports.Report_Forms.user_report_form import UserReportForm
from eProc_Reports.Utilities.reports_generic import get_usrid_by_username, get_companylist

