frappe.ui.form.on('Disposing Items', {
    refresh(Frm){
        if(frm.doc.__islocal){
			frm.reload_doc()
		}
    },
	after_save(frm) {
		frappe.call({
            method:"senergy.senergy.doctype.disposing_items.disposing_items.update_wfs",
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
	}
})