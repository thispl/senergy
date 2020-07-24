// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors and contributors
// For license information, please see license.txt

frappe.query_reports["Stock Balance Senergy"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": "80",
			"reqd": 1,
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": "80",
			"reqd": 1,
			"default": frappe.datetime.get_today()
		},
		{
			"fieldname": "item_group",
			"label": __("Item Group"),
			"fieldtype": "Link",
			"width": "80",
			"options": "Item Group"
		},
		,
		{
			"fieldname":"inventory_type",
			"label": __("Inventory Type"),
			"fieldtype": "Select",
			"options": "Direct Sales\nService\nConsumables",
		},
		{
			"fieldname":"brand",
			"label": __("Brand"),
			"fieldtype": "Link",
			"options": "Brand"
		},
		{
			"fieldname": "item_code",
			"label": __("Item"),
			"fieldtype": "Link",
			"width": "80",
			"options": "Item",
			"get_query": function() {
				return {
					query: "erpnext.controllers.queries.item_query",
				};
			}
		},
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"width": "80",
			"options": "Company",
		},
		{
			"fieldname": "country",
			"label": __("Country"),
			"fieldtype": "Select",
			"width": "80",
			"options": " \nKuwait\nPakistan\nIraq\nSudan",
		},
		{
			"fieldname": "warehouse",
			"label": __("Warehouse"),
			"fieldtype": "Link",
			"width": "80",
			"options": "Warehouse",
			get_query: () => {
				var warehouse_type = frappe.query_report.get_filter_value('warehouse_type');
				var company = frappe.query_report.get_filter_value('company');
				if(warehouse_type){
					return {
						filters: {
							'warehouse_type': warehouse_type
						}
					};
				}
				if(company){
					return {
						filters: {
							'company': company
						}
					};
				}
				if(warehouse_type && company){
					return {
						filters: {
							'company': company,
							'warehouse_type': warehouse_type
						}
					};
				}
			}
		},
		{
			"fieldname": "warehouse_type",
			"label": __("Warehouse Type"),
			"fieldtype": "Link",
			"width": "80",
			"options": "Warehouse Type"
		},
		{
			"fieldname": "currency",
			"label": __("Currency"),
			"fieldtype": "Link",
			"width": "80",
			"options": "Currency"
		},
		{
			"fieldname":"include_uom",
			"label": __("Include UOM"),
			"fieldtype": "Link",
			"options": "UOM"
		},
		{
			"fieldname": "show_variant_attributes",
			"label": __("Show Variant Attributes"),
			"fieldtype": "Check"
		},
		{
			"fieldname": 'show_stock_ageing_data',
			"label": __('Show Stock Ageing Data'),
			"fieldtype": 'Check'
		},
	],
	onload:function(frm){
		
		frappe.breadcrumbs.add('Senergy');
	}
	// "onload": function() {
	// 	return  frappe.call({
	// 		method: "senergy.senergy.report.stock_balance_senergy.stock_balance_senergy.get_sle_countries",
	// 		callback: function(r) {
	// 			var country_filter = frappe.query_report.get_filter('country');
	// 			country_filter.df.options = r.message;
	// 			country_filter.df.default = r.message.split("\n")[0];
	// 			country_filter.refresh();
	// 			// country_filter.set_input(country_filter.df.default);
	// 		}
	// 	});
	// }
};
