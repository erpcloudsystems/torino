import frappe
from erpnext.manufacturing.doctype.production_plan.production_plan import  ProductionPlan ,get_bin_details
from erpnext.manufacturing.doctype.bom.bom import get_children as get_bom_children
class CustomProductionPlan(ProductionPlan):
    def make_work_order_for_subassembly_items(self, wo_list, subcontracted_po, default_warehouses):
        for row in self.sub_assembly_items:
            if row.type_of_manufacturing == "Subcontract":
                subcontracted_po.setdefault(row.supplier, []).append(row)
                continue

            if row.type_of_manufacturing == "Material Request":
                continue

            work_order_data = {
                "wip_warehouse": default_warehouses.get("wip_warehouse"),
                "fg_warehouse": default_warehouses.get("fg_warehouse"),
                "company": self.get("company"),

            }

            self.prepare_data_for_sub_assembly_items(row, work_order_data)
            work_order = self.create_work_order(work_order_data)
            if work_order:
                wo_list.append(work_order)
    def prepare_data_for_sub_assembly_items(self, row, wo_data):
        for field in [
            "production_item",
            "item_name",
            "qty",
            "fg_warehouse",
            "description",
            "bom_no",
            "stock_uom",
            "bom_level",
            "schedule_date",
            "custom_work_order_date"
        ]:
            if row.get(field):
                wo_data[field] = row.get(field)

        wo_data.update(
            {
                "use_multi_level_bom": 0,
                "production_plan": self.name,
                "production_plan_sub_assembly_item": row.name,
                "custom_date":row.custom_work_order_date

            }
        )
        
# def get_sub_assembly_items(bom_no, bom_data, to_produce_qty, company, warehouse=None, indent=0):
# 	data = get_bom_children(parent=bom_no)
# 	for d in data:
# 		if d.expandable:
# 			parent_item_code = frappe.get_cached_value("BOM", bom_no, "item")
# 			stock_qty = (d.stock_qty / d.parent_bom_qty) * flt(to_produce_qty)

# 			if warehouse:
# 				bin_dict = get_bin_details(d, company, for_warehouse=warehouse)

# 				if bin_dict and bin_dict[0].projected_qty > 0:
# 					if bin_dict[0].projected_qty > stock_qty:
# 						continue
# 					else:
# 						stock_qty = stock_qty - bin_dict[0].projected_qty

# 			bom_data.append(
# 				frappe._dict(
# 					{
# 						"parent_item_code": parent_item_code,
# 						"description": d.description,
# 						"production_item": d.item_code,
# 						"item_name": d.item_name,
# 						"stock_uom": d.stock_uom,
# 						"uom": d.stock_uom,
# 						"bom_no": d.value,
# 						"is_sub_contracted_item": d.is_sub_contracted_item,
# 						"bom_level": indent,
# 						"indent": indent,
# 						"stock_qty": stock_qty,
#                         "custom_date": d.custom_work_order_date
# 					}
# 				)
# 			)

# 			if d.value:
# 				get_sub_assembly_items(d.value, bom_data, stock_qty, company, warehouse, indent=indent + 1)