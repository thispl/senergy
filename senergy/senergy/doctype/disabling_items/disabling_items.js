frappe.ui.form.on('Disabling Items', {
	refresh(frm) {
		// your code here
	},
	onload(frm){
	    frm.set_query("serial_number", function() {
        return {
            "filters": {
                "item_code": frm.doc.item_code,
                "disabled":0,
                "disposed":0
            }
        };
    });
     frm.set_query("item_code", function() {
        return {
            "filters": {
                "company": frm.doc.company
            }
        };
	});
	cur_frm.set_query("item_code", function() {
		return erpnext.queries.item({"is_stock_item": 1, "has_serial_no": 1,"company":frm.doc.company})
	});
    },
    after_save(frm) {
		frappe.call({
            method:"senergy.senergy.doctype.disabling_items.disabling_items.update_wfs",
            args:{
                "name":frm.doc.name
            },
            callback(r){
                if(r){
                    frm.reload_doc();
                }
            }
        })
    },
})