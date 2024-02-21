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
    # sub_assembly_items = frappe.get_all("Sub Assembly Items",
    #                                     filters={"production_item": doc.production_item},
    #                                     fields=["custom_work_order_date"])

    # if sub_assembly_items:
    #     frappe.db.set_value("Work Order", doc.name, "custom_date", sub_assembly_items.custom_work_order_date)
    pass
@frappe.whitelist()
def before_validate(doc, method=None):
    pass

@frappe.whitelist()
def validate(doc, method=None):
    pass

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
