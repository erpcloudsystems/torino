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

import frappe

@frappe.whitelist()
def validate(doc, method=None):
    for row in doc.operations:
        if row.workstation:
            time_to_fill = frappe.get_value("Item Die Table",
                                             {"parent": doc.production_item, "line_no": row.workstation},
                                             "time_to_fill_10kg_min")
            if time_to_fill is not None:
                time_in_mins = int(time_to_fill) / 10
                row.time_in_mins = time_in_mins
            else:
                for i in doc.operations:
                    fixed_time = frappe.db.get_value("BOM Operation",
                                                     {"parent": doc.bom_no, "Operation": i.operation},
                                                     "fixed_time")

                    if frappe.db.get_value("BOM Operation",
                                           {"parent": doc.bom_no, "operation": i.operation},
                                           "time_in_mins"):
                        time=frappe.db.get_value("BOM Operation",
                                                        {"parent": doc.bom_no, "operation": i.operation},
                                                        ["time_in_mins"])
                        qty=frappe.db.get_value("BOM",{"name": doc.bom_no},
                                                        ["quantity"])
                        if fixed_time:
                            i.time_in_mins = time
                        else:
                            i.time_in_mins = time * qty
                    

                    
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
def get_time(production_item):
    time_in_mins = (frappe.get_value("Work Order Operation",{"parent":production_item}),["time_to_fill_10kg_min"])/10
    # # frappe.msgprint(str(production_qty_kghour))
    # row.custom_time_to_finish_per_line=production_qty_kghour
    return time_in_mins