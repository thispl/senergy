frappe.ui.form.on('Physical Count Reconciliation', {
	refresh(frm) {
		if(frm.doc.__islocal){
			frm.reload_doc()
		}
		frm.set_value('date',frappe.datetime.get_today());
		frm.set_query("country", function() {
        return {
            filters: {
						'reqd': '1'
					}
        };
    });
	},
	company(frm){
		frm.set_value("warehouse","")
	},
	after_save(frm) {
		frappe.call({
            method:"senergy.senergy.doctype.physical_count_reconciliation.physical_count_reconciliation.update_wfs",
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
	set_queries(frm){
		frm.set_query("company", function() {
        return {
            "filters": {
                // "country": frm.doc.country,
            }
        };
    });
	frm.set_query("warehouse", function() {
        return {
            "filters": {
                "country": frm.doc.country,
				"company": frm.doc.company
            }
        };
    });
	frm.set_query("country", function() {
        return {
            filters: {
						'reqd': '1'
					}
        };
    });
	},
	
	company(frm){
	//  frm.trigger('get_items')
	if(frm.doc.warehouse){
		frm.set_value("warehouse","")
	}
	 frm.trigger('set_queries')
	},
	warehouse(frm){
		frm.trigger('get_items')
		frm.trigger('set_queries')
	},
	country(frm){
		// frm.trigger('get_items')
		frm.trigger('set_queries')
		frm.set_query("warehouse", function() {
        return {
            "filters": {
                "country": frm.doc.country,
				"company": frm.doc.company
            }
        };
    });
	},
	get_items(frm){
		if(frm.doc.company){
		frappe.call({
			method:"senergy.custom.physical_count",
			args:{
				"doctype":"Item",
				"company":frm.doc.company,
				"country":frm.doc.country,
				"warehouse": frm.doc.warehouse
			},
			callback(r){
			   frm.clear_table("table_6");
			   $.each(r.message,function(i,d){
				   var row = frappe.model.add_child(frm.doc, "Physical Count", "table_6");
				   row.company = d.company;
				   row.warehouse = d.warehouse;
				   row.country = d.country;
				   row.store_quantity = d.qty_after_transaction;
				   row.item = d.item;
				   row.item_name = d.item_name;
				   row.description = d.description;
				   row.item_location = d.item_location;
			   });
			   refresh_field("table_6");
			}
		})   
	}
}
})
frappe.ui.form.on('Physical Count', {
	refresh(frm) {
		// your code here
    },
    physical_quantity(frm,cdt,cdn){
        var child = locals[cdt][cdn]
        var diff_qty = (Number(child.physical_quantity) - Number(child.store_quantity))
        child.difference_quantity = diff_qty
        refresh_field("table_6")
    }
})