import frappe
from erpnext.manufacturing.doctype.work_order.work_order import WorkOrder
from frappe.utils import (
	cint,
	date_diff,
	flt,
	get_datetime,
	get_link_to_form,
	getdate,
	now,
	nowdate,
	time_diff_in_hours,
)

class CustomWorkOrder(WorkOrder):
    
    # def set_work_order_operations(self):
    #     """Fetch operations from BOM and set in 'Work Order'"""

    #     def _get_operations(bom_no, qty=1):
    #         data = frappe.get_all(
    #             "BOM Operation",
    #             filters={"parent": bom_no},
    #             fields=[
    #                 "operation",
    #                 "description",
    #                 "workstation",
    #                 "idx",
    #                 "workstation_type",
    #                 "base_hour_rate as hour_rate",
    #                 "time_in_mins",
    #                 "parent as bom",
    #                 "batch_size",
    #                 "sequence_id",
    #                 "fixed_time",
    #             ],
    #             order_by="idx",
    #         )

    #         for d in data:
    #             time_to_fill_10kg_min = frappe.get_value("Work Order Operation",{"parent":self.production_item}),["time_to_fill_10kg_min"]
    #             if time_to_fill_10kg_min:
    #                 d.time_in_mins =(time_to_fill_10kg_min)/10
    #             elif not d.fixed_time:
    #                 d.time_in_mins = flt(d.time_in_mins) * flt(qty)
    #             d.status = "Pending"

    #         return data

    #     self.set("operations", [])
    #     if not self.bom_no or not frappe.get_cached_value("BOM", self.bom_no, "with_operations"):
    #         return

    #     operations = []

    #     if self.use_multi_level_bom:
    #         bom_tree = frappe.get_doc("BOM", self.bom_no).get_tree_representation()
    #         bom_traversal = reversed(bom_tree.level_order_traversal())

    #         for node in bom_traversal:
    #             if node.is_bom:
    #                 operations.extend(_get_operations(node.name, qty=node.exploded_qty / node.bom_qty))

    #     bom_qty = frappe.get_cached_value("BOM", self.bom_no, "quantity")
    #     operations.extend(_get_operations(self.bom_no, qty=1.0 / bom_qty))

    #     for correct_index, operation in enumerate(operations, start=1):
    #         operation.idx = correct_index

    #     self.set("operations", operations)
    #     self.calculate_time()
        
    def calculate_time(self):
            for d in self.get("operations"):
                time_to_fill_10kg_min = frappe.get_value("Work Order Operation",{"parent":self.production_item}),["time_to_fill_10kg_min"]
                if time_to_fill_10kg_min:
                    d.time_in_mins =flt((time_to_fill_10kg_min))/10
                    
                elif not d.fixed_time:
                    d.time_in_mins = flt(d.time_in_mins) * (flt(self.qty) / flt(d.batch_size))

            self.calculate_operating_cost()