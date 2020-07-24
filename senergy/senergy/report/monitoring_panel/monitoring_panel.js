// Copyright (c) 2016, TeamPRO and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Monitoring Panel"] = {
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
			"fieldtype": "Link",
			"width": "80",
			"options":"Country",
			"get_query": () => {
				return {
					filters: {
						'reqd': '1'
					}
				};
			}
		},
		{
			"fieldname":"inventory_type",
			"label": __("Inventory Type"),
			"fieldtype": "Link",
			"options": "Inventory Type",
		},
		{
			"fieldname": "warehouse",
			"label": __("Warehouse"),
			"fieldtype": "MultiSelectList",
			"width": "80",
			get_data: function(txt) {
				company = frappe.query_report.get_filter_value('company');
				if(company){
					return frappe.db.get_link_options('Warehouse', txt,{'company' : company })
				}
				return frappe.db.get_link_options('Warehouse', txt)
			},
		},
		// {
		// 	"fieldname": "warehouse_type",
		// 	"label": __("Warehouse Type"),
		// 	"fieldtype": "Link",
		// 	"width": "80",
		// 	"options": "Warehouse Type"
		// },
		{
			"fieldname": "currency",
			"label": __("Currency"),
			"fieldtype": "Link",
			"width": "80",
			"options": "Currency"
		},
		// {
		// 	"fieldname":"include_uom",
		// 	"label": __("Include UOM"),
		// 	"fieldtype": "Link",
		// 	"options": "UOM"
		// },
		// {
		// 	"fieldname": "show_variant_attributes",
		// 	"label": __("Show Variant Attributes"),
		// 	"fieldtype": "Check"
		// },
		{
			"fieldname": 'show_stock_ageing_data',
			"label": __('Show Stock Ageing Data'),
			"fieldtype": 'Check'
		},
	],
	onload:function(frm){
		
		frappe.breadcrumbs.add('Senergy');
	}
};
