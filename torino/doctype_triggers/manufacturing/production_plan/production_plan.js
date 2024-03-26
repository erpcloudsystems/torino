frappe.ui.form.on('Production Plan', {
    custom_wip_warehouse: function(frm) {
        if (frm.doc.custom_wip_warehouse) {
            frappe.call({
                method: "torino.doctype_triggers.manufacturing.production_plan.production_plan.get_production_line",
                args: {
                    item_code: frm.doc.item_code,
                    planned_qty: frm.doc.pending_qty,
                    custom_wip_warehouse: frm.doc.custom_wip_warehouse
                },
                callback: function(r) {
                    if (r.message) {
                        frappe.model.set_value(frm.doctype, frm.docname, 'custom_time_to_finish_per_line', r.message);
                    } else {
                        frappe.msgprint("No data received from the server.");
                    }
                },
                error: function(err) {
                    frappe.msgprint("Error: " + err.responseText);
                }
            });
        } else {
            frappe.model.set_value(frm.doctype, frm.docname, 'custom_time_to_finish_per_line', 0);
        }
    }
});

frappe.ui.form.on('Production Plan Item', {
    custom_wip_warehouse: function(frm, cdt, cdn) {
        let child = locals[cdt][cdn];
        if (child.custom_wip_warehouse) {
            frappe.call({
                method: "torino.doctype_triggers.manufacturing.production_plan.production_plan.get_production_line",
                args: {
                    item_code: child.item_code,
                    planned_qty: child.pending_qty,
                    custom_wip_warehouse: child.custom_wip_warehouse
                },
                callback: function(r) {
                    if (r.message) {
                        frappe.model.set_value(cdt, cdn, 'custom_time_to_finish_per_line', r.message);
                    } else {
                        frappe.msgprint("No data received from the server.");
                    }
                },
                error: function(err) {
                    frappe.msgprint("Error: " + err.responseText);
                }
            });
        } else {
            frappe.model.set_value(cdt, cdn, 'custom_time_to_finish_per_line', 0);
        }
    }
});

frappe.ui.form.on('Production Plan', {
    get_sub_assembly_items: async function(frm, cdt, cdn) {
        let child = locals[cdt][cdn];
        let qty = 0.0;

        if (frm.doc.sub_assembly_items) {
            for (let row of frm.doc.sub_assembly_items) {
                try {
                    let itemGroup = await frappe.db.get_value("Item", { name: row.production_item }, "item_group");
                    console.log("Item Group:", itemGroup);
                    if (itemGroup && itemGroup.message.item_group === "نصف مصنع") {
                        console.log("Quantity Before Addition:", qty);
                        qty += row.qty;
                        console.log("Quantity After Addition:", qty);
                    }
                } catch (error) {
                    console.error("Error getting item group:", error);
                }
            }

            console.log("Final Quantity:", qty);
            frm.set_value('custom_qty_to_mix', qty);
            let remaining = 750 - qty;
            frm.set_value('custom_qty_remaining', remaining);
            frm.refresh_field('custom_qty_to_mix');
            frm.refresh_field('custom_qty_remaining');
        }
    }
});






frappe.ui.form.on('Mixing Remaining', {
    create_work_order: function(frm, cdt, cdn) {
        let child = locals[cdt][cdn];
        let document = frm.doc;
        let row_index = child.idx;
        
        for (let row of document.custom_mixing_remaining) {
            if (parseInt(row_index) === parseInt(row.idx)) {
                if (!row.work_order1) {
                    let wo1 = frappe.model.get_new_doc("Work Order");
                    wo1.production_item = row.item1;
                    wo1.qty = row.qty1;
                    wo1.bom_no = row.bom1;
                    wo1.fg_warehouse = "Mixing - T";
                    frappe.db.insert(wo1);
                    frappe.after_ajax(() => {
                        if (wo1.name) {
                            frappe.msgprint(`Work Order Created ${wo1.name}`);
                            row.work_order1 = wo1.name;
                            frm.refresh();
                        }
                    });
                }

                if (!row.work_order2) {
                    let wo2 = frappe.model.get_new_doc("Work Order");
                    wo2.production_item = row.item2;
                    wo2.qty = row.qty2;
                    wo2.bom_no = row.bom2;
                    wo2.fg_warehouse = "Mixing - T";
                    frappe.db.insert(wo2);
                    frappe.after_ajax(() => {
                        if (wo2.name) {
                            frappe.msgprint(`Work Order Created ${wo2.name}`);
                            row.work_order2 = wo2.name;
                            frm.refresh();
                        }
                    });
                }
            }
        }
    }
});





