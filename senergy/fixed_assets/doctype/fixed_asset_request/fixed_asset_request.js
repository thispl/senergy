// Copyright (c) 2020, TeamPRO and contributors
// For license information, please see license.txt

{% include 'erpnext/public/js/controllers/buying.js' %};

frappe.ui.form.on('Fixed Asset Request', {
	onload(frm){
		frappe.breadcrumbs.add("Assets", "Fixed Asset Request");
	},
	onload_post_render:function(frm) {
		if(frm.doc.__islocal){
			frm.set_value('req_by',frappe.session.user);
		}
	    
		// your code here
		frm.trigger("set_filter")
	},
	refresh: function(frm) {
		frm.trigger("set_filter");
		if(frm.doc.docstatus == 1){
			frm.events.make_custom_buttons(frm);
		}
		
	},
	schedule_date:function(frm){
		frm.trigger("set_schedule_date")
	},
	validate(frm){
		frm.trigger("set_schedule_date")
	},
	set_schedule_date(frm) {
		if(frm.doc.schedule_date){
			erpnext.utils.copy_value_in_all_rows(frm.doc, frm.doc.doctype, frm.doc.name, "items", "schedule_date");
		}
	},
	set_filter:function(frm){
	    frm.set_query('item_code', 'items', () => {
			return {
				filters: {
					company: frm.doc.company,
					is_fixed_asset: 1
				}
			}
		})
	},
	make_custom_buttons(frm){
			frm.add_custom_button(__('Purchase Order'),
				() => frm.events.make_purchase_order(frm), __('Create'));

			frm.add_custom_button(__("Request for Quotation"),
				() => frm.events.make_request_for_quotation(frm), __('Create'));

			frm.add_custom_button(__("Supplier Quotation"),
				() => frm.events.make_supplier_quotation(frm), __('Create'));
	},
	make_request_for_quotation: function(frm) {
		frappe.model.open_mapped_doc({
			method: "senergy.fixed_assets.doctype.fixed_asset_request.fixed_asset_request.make_request_for_quotation",
			frm: frm,
			run_link_triggers: true
		});
	},
	make_supplier_quotation: function(frm) {
		frappe.model.open_mapped_doc({
			method: "senergy.fixed_assets.doctype.fixed_asset_request.fixed_asset_request.make_supplier_quotation",
			frm: frm
		});
	},
	make_purchase_order: function(frm) {
		frappe.prompt(
			{
				label: __('For Default Supplier (Optional)'),
				fieldname:'default_supplier',
				fieldtype: 'Link',
				options: 'Supplier',
				description: __('Select a Supplier from the Default Supplier List of the items below.'),
				get_query: () => {
					return{
						query: "senergy.fixed_assets.doctype.fixed_asset_request.fixed_asset_request.get_default_supplier_query",
						filters: {'doc': frm.doc.name}
					}
				}
			},
			(values) => {
				frappe.model.open_mapped_doc({
					method: "senergy.fixed_assets.doctype.fixed_asset_request.fixed_asset_request.make_purchase_order",
					frm: frm,
					args: { default_supplier: values.default_supplier },
					run_link_triggers: true
				});
			},
			__('Enter Supplier'),
			__('Create')
		)
	},
});




