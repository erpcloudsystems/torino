// frappe.ui.form.on('Production Plan','custom_wip_warehouse',function(frm){
//     console.log("kkkk")
//     frappe.call({
//         method:"torino.doctype_triggers.manufacturing.production_plan.production_plan.get_production_line",
//         args:{
//             item_code:frm.docitem_code,
//             planned_qty:frm.doc.pending_qty,
//             custom_wip_warehouse:frm.doc.custom_wip_warehouse
//         },
//         callback:function(r){
//             console.log(r.message)
//             frappe.set_value('custom_time_to_finish_per_line',r.message)
//         }
        
//     });
//     frm.refresh_field("custom_time_to_finish_per_line")
// })


frappe.ui.form.on('Production Plan Item', {
    custom_wip_warehouse: function(frm, cdt, cdn) {
        let child = locals[cdt][cdn];
        console.log("kkkk");
        if (child.custom_wip_warehouse){
        frappe.call({
            method: "torino.doctype_triggers.manufacturing.production_plan.production_plan.get_production_line",
            args: {
                item_code: child.item_code,
                planned_qty: child.pending_qty,
                custom_wip_warehouse: child.custom_wip_warehouse
            },
            callback: function(r) {
                if (r.message) {
                    console.log(r.message);
                    frappe.model.set_value(cdt, cdn, 'custom_time_to_finish_per_line', r.message);
                } else {
                    frappe.msgprint("No data received from the server.");
                }
            },
            error: function(err) {
                frappe.msgprint("Error: " + err.responseText);
            }
        });
    }else{
        frappe.model.set_value(cdt, cdn, 'custom_time_to_finish_per_line', 0);
    }}
});

