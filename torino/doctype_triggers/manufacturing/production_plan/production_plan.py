from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import now

import math

@frappe.whitelist()
def before_insert(doc, method=None):
    pass

@frappe.whitelist()
def after_insert(doc, method=None):
    pass

@frappe.whitelist()
def onload(doc, method=None):
    pass
@frappe.whitelist()
def before_validate(doc, method=None):
    pass

@frappe.whitelist()
def validate(doc, method=None):
    for row in doc.po_items:
        production_qty_kghour = (row.planned_qty)/(frappe.get_value("Item Die Table",{"parent":row.item_code,"line_no":row.custom_wip_warehouse},["production_qty_kghour"]))
        # frappe.msgprint(str(production_qty_kghour))
        row.custom_time_to_finish_per_line=production_qty_kghour

@frappe.whitelist()
def on_submit(doc, method=None):
    pass
@frappe.whitelist()
def on_cancel(doc, method=None):
    pass
@frappe.whitelist()
def on_update_after_submit(doc, method=None):
    pass
@frappe.whitelist()
def before_save(doc, method=None):
    pass
@frappe.whitelist()
def before_cancel(doc, method=None):
    pass
@frappe.whitelist()
def on_update(doc, method=None):
    pass

@frappe.whitelist()
def get_production_line(item_code,planned_qty,custom_wip_warehouse):
    production_qty_kghour = (float(planned_qty))/(frappe.get_value("Item Die Table",{"parent":item_code,"line_no":custom_wip_warehouse},["production_qty_kghour"]))
    # # frappe.msgprint(str(production_qty_kghour))
    # row.custom_time_to_finish_per_line=production_qty_kghour
    return production_qty_kghour