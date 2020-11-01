frappe.ui.form.on('Disposing Items', {
    refresh(frm){
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
    item_code(frm){
        if(frm.doc.item_code){
            frappe.call({
                method : "frappe.client.get_list",
                args:{
                    "doctype" : "Serial No",
                    filters:{
                        "item_code" : frm.doc.item_code
                    },
                    fields:['name','warehouse','purchase_date','purchase_rate']
                },
                callback(r){
                    $.each(r.message,function(i,d){
                        var row = frappe.model.add_child(frm.doc,"Disposing Item Table","items")
                        row.serial_number = d.name
                        row.warehouse = d.warehouse
                        row.received_date = d.purchase_date
                        row.item_value = d.purchase_rate
                    })
                    refresh_field("items")
                }
            })
        }
    }
})