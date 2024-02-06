"""Copyright (c) 2020 Hiranya Garbha, Inc.
Name:
    Doc_Report.py
Usage:
    SC and PO document search form.
     m_docsearch_meth - This function is used to get header details of shopping cart and purchase order.
Author:
    Varsha
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from eProc_Basic.Utilities.functions.encryption_util import encrypt
from eProc_Basic.Utilities.functions.get_db_query import getClients
from eProc_Doc_Search_and_Display.Utilities.search_display_generic import get_hdr_data
from eProc_Doc_Search_and_Display.Utilities.search_display_specific import get_sc_header_app
from eProc_Reports.Report_Forms.SearchDoc_forms import *
from eProc_Reports.Utilities.reports_generic import get_companylist

