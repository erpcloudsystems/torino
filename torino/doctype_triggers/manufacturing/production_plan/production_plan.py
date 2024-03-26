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

@frappe.whitelist()
def get_production_line(item_code,planned_qty,custom_wip_warehouse):
    production_qty_kghour = (float(planned_qty))/(frappe.get_value("Item Die Table",{"parent":item_code,"line_no":custom_wip_warehouse},["production_qty_kghour"]))
    return production_qty_kghour
@frappe.whitelist()
def get_qty_to_mix(name):
    production_plan = frappe.get_doc("Production Plan",name)
    qty=0.0
    if production_plan.sub_assembly_items:
        for row in production_plan.sub_assembly_items:
            item_group=frappe.get_value("Item",{"name":row.production_item},"item_group")
            if item_group == "نصف مصنع":
                qty+= row.qty
    qty_to_mix=qty
    return qty_to_mix
# @frappe.whitelist()
# def make_work_order(document, row_index):
#     # frappe.msgprint(str(document))
#     # production_plan = frappe.get_doc("Production Plan", name)
 
#     for row in document.custom_mixing_remaining:
#         if int(row_index) == int(row.idx):
            
#             wo1 = frappe.new_doc("Work Order")
#             wo1.production_item = row.item1
#             wo1.qty = row.qty1
#             wo1.bom_no = row.bom1
#             wo1.fg_warehouse="Mixing - T"

#             wo2 = frappe.new_doc("Work Order")
#             wo2.production_item = row.item2
#             wo2.qty = row.qty2
#             wo2.bom_no = row.bom2
#             wo2.fg_warehouse="Mixing - T"

#             wo1.insert()
#             wo2.insert()

#             if wo1.name:
#                 frappe.msgprint(f"Work Order Created {wo1.name}")
#                 row.work_order1=wo1.name
#             if wo2.name:
#                 frappe.msgprint(f"Work Order Created {wo2.name}")
#                 row.work_order2=wo2.name
#     document.save()

    
    