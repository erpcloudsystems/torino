frappe.ui.form.on("Payment Entry", "mode_of_payment_2", function(frm) {
    if (frm.doc.payment_type === "Internal Transfer") {
    frappe.call({
        method: "torino.doctype_triggers.accounting.payment_entry.payment_entry.get_paid_to_account",
        args: {
            account: frm.doc.mode_of_payment_2
        },
        callback: function(r) {
            if (r.message) {
                // Use the returned value
                console.log(r.message);
                frm.set_value("paid_to", r.message);
                refresh_field("paid_to");
            }
        }
    });
}
});