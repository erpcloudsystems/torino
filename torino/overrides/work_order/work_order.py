import frappe
from erpnext.manufacturing.doctype.work_order.work_order import( WorkOrder,get_item_details,add_variant_item)
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
    def onload(self):
        frappe.msgprint("kkkkkkkk")

    def set_work_order_operations3(self):
        """Fetch operations from BOM and set in 'Work Order'"""

        def _get_operations(bom_no, qty=1):
            data = frappe.get_all(
                "BOM Operation",
                filters={"parent": bom_no},
                fields=[
                    "operation",
                    "description",
                    "workstation",
                    "idx",
                    "workstation_type",
                    "base_hour_rate as hour_rate",
                    "time_in_mins",
                    "parent as bom",
                    "batch_size",
                    "sequence_id",
                    "fixed_time",
                ],
                order_by="idx",
            )

            for d in data:
                for row in self.operations:
                    if row.workstation:
                        time=(frappe.db.get_value("Item Die Table",{'parent':self.production_item},"time_to_fill_10kg_min"))/10
                        d.time_in_mins=time
                        frappe.msgprint("str(time)")
                    # elif not d.fixed_time:
                    #     d.time_in_mins = flt(d.time_in_mins) * flt(qty)
                d.status = "Pending"

            return data

        self.set("operations", [])
        if not self.bom_no or not frappe.get_cached_value("BOM", self.bom_no, "with_operations"):
            return

        operations = []

        if self.use_multi_level_bom:
            bom_tree = frappe.get_doc("BOM", self.bom_no).get_tree_representation()
            bom_traversal = reversed(bom_tree.level_order_traversal())

            for node in bom_traversal:
                if node.is_bom:
                    operations.extend(_get_operations(node.name, qty=node.exploded_qty / node.bom_qty))

        bom_qty = frappe.get_cached_value("BOM", self.bom_no, "quantity")
        operations.extend(_get_operations(self.bom_no, qty=1.0 / bom_qty))

        for correct_index, operation in enumerate(operations, start=1):
            operation.idx = correct_index

        self.set("operations", operations)
        self.calculate_time()

    def calculate_time(self):
        for d in self.get("operations"):
            if not d.fixed_time:
                d.time_in_mins = flt(d.time_in_mins) * (flt(self.qty) / flt(d.batch_size))
@frappe.whitelist()
def set_work_order_ops(name):
    po = frappe.get_doc("Work Order", name)
    frappe.msgprint("helllo")
    po.set_work_order_operations3()
    po.save()
@frappe.whitelist()
def make_work_order(bom_no, item, qty=0, project=None, variant_items=None):
	if not frappe.has_permission("Work Order", "write"):
		frappe.throw(_("Not permitted"), frappe.PermissionError)

	item_details = get_item_details(item, project)

	wo_doc = frappe.new_doc("Work Order")
	wo_doc.production_item = item
	wo_doc.update(item_details)
	wo_doc.bom_no = bom_no

	if flt(qty) > 0:
		wo_doc.qty = flt(qty)
		wo_doc.get_items_and_operations_from_bom()

	if variant_items:
		add_variant_item(variant_items, wo_doc, bom_no, "required_items")

	return wo_doc

@frappe.whitelist()
def get_item_details(item, project=None, skip_bom_info=False, throw=True):
	res = frappe.db.sql(
		"""
		select stock_uom, description, item_name, allow_alternative_item,
			include_item_in_manufacturing
		from `tabItem`
		where disabled=0
			and (end_of_life is null or end_of_life='0000-00-00' or end_of_life > %s)
			and name=%s
	""",
		(nowdate(), item),
		as_dict=1,
	)

	if not res:
		return {}

	res = res[0]
	if skip_bom_info:
		return res

	filters = {"item": item, "is_default": 1, "docstatus": 1}

	if project:
		filters = {"item": item, "project": project}

	res["bom_no"] = frappe.db.get_value("BOM", filters=filters)

	if not res["bom_no"]:
		variant_of = frappe.db.get_value("Item", item, "variant_of")

		if variant_of:
			res["bom_no"] = frappe.db.get_value("BOM", filters={"item": variant_of, "is_default": 1})

	if not res["bom_no"]:
		if project:
			res = get_item_details(item, throw=throw)
			frappe.msgprint(
				_("Default BOM not found for Item {0} and Project {1}").format(item, project), alert=1
			)
		else:
			msg = _("Default BOM for {0} not found").format(item)
			frappe.msgprint(msg, raise_exception=throw, indicator="yellow", alert=(not throw))

			return res

	bom_data = frappe.db.get_value(
		"BOM",
		res["bom_no"],
		["project", "allow_alternative_item", "transfer_material_against", "item_name"],
		as_dict=1,
	)

	res["project"] = project or bom_data.pop("project")
	res.update(bom_data)
	res.update(check_if_scrap_warehouse_mandatory(res["bom_no"]))

	return res

@frappe.whitelist()
def check_if_scrap_warehouse_mandatory(bom_no):
	res = {"set_scrap_wh_mandatory": False}
	if bom_no:
		bom = frappe.get_doc("BOM", bom_no)

		if len(bom.scrap_items) > 0:
			res["set_scrap_wh_mandatory"] = True

	return res