# Custom template tags
import os

from django import template
from eProc_Purchase_Order.models.purchase_order import PoHeader
from eProc_Shopping_Cart.models import ScHeader

register = template.Library()


# Remove underscore and redefine column name
@register.filter
def remove_underscore(data):
    return data.replace("_", " ").upper()


# Get row(r) data with value cl
@register.filter
def get_row_data(r, cl):
    dt = getattr(r, cl[0])
    if dt is None:
        return ''
    return getattr(r, cl[0])

# Overriding the models column names
@register.filter
def get_verbose(mdl, cl):
    return mdl._meta.get_field(cl).verbose_name



# Get data for link columns
@register.filter
def get_link_data(r, cl):
    if cl[1] == 1:
        return getattr(r, 'guid')
    elif cl[1] == 2:
        if cl[0] == 'sc_num':
            objid = getattr(r, 'sc_num')
            return ScHeader.get_hdr_guid_by_objid(objid)
        elif cl[0] == 'po_num':
            return PoHeader.get_hdr_guid_by_objid(getattr(r, 'po_num'))
    else:
        return getattr(r, cl[0])


# Get doc type
@register.filter
def get_doc_type(r, cl):
    if cl[1] == 1:
        if r._meta.object_name == 'ScHeader':
            return 'SC'
        elif r._meta.object_name == 'PoHeader':
            return 'PO'
        else:
            return 'error'
    elif cl[1] == 2:
        if cl[0] == 'sc_num':
            return 'SC'
        elif cl[0] == 'po_num':
            return 'PO'
    else:
        return 'error'


# Check file or directory
@register.filter
def check_is_file(file):
    if os.path.exists(file[0]):
        if os.path.isfile(file[0]):
            return True
    return False
