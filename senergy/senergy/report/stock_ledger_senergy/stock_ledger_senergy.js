// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.query_reports["Stock Ledger Senergy"] = {
	"filters": [
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
			"reqd": 1
		},
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			"reqd": 1
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1
		},
		{
			"fieldname":"warehouse",
			"label": __("Warehouse"),
			"fieldtype": "Link",
			"options": "Warehouse",
			get_query: () => {
				var company = frappe.query_report.get_filter_value('company');
				if(company){
					return {
						filters: {
							'company': company
						}
					};
				}
			}
		},
		{
			"fieldname":"item_code",
			"label": __("Item"),
			"fieldtype": "Link",
			"options": "Item",
			"get_query": function() {
				return {
					query: "erpnext.controllers.queries.item_query"
				}
			}
		},
		{
			"fieldname":"item_group",
			"label": __("Item Group"),
			"fieldtype": "Link",
			"options": "Item Group"
		},
		{
			"fieldname":"batch_no",
			"label": __("Batch No"),
			"fieldtype": "Link",
			"options": "Batch"
		},
		{
			"fieldname":"brand",
			"label": __("Brand"),
			"fieldtype": "Link",
			"options": "Brand"
		},
		{
			"fieldname":"voucher_no",
			"label": __("Voucher #"),
			"fieldtype": "Data"
		},
		{
			"fieldname":"project",
			"label": __("Project"),
			"fieldtype": "Link",
			"options": "Project"
		},
		{
			"fieldname":"include_uom",
			"label": __("Include UOM"),
			"fieldtype": "Link",
			"options": "UOM"
		},
		{
			"fieldname":"currency",
			"label": __("Currency"),
			"fieldtype": "Link",
			"options": "Currency",
			"default":'KWD'
		}
	],
	onload:function(frm){
		
		frappe.breadcrumbs.add('Senergy');
	}

	// "onload": function() {
	// 	return  frappe.call({
	// 		method: "senergy.report.stock_balance_senergy.stock_balance_senergy.get_sle_countries",
	// 		callback: function(r) {
	// 			var country_filter = frappe.query_report.get_filter('country');
	// 			country_filter.df.options = r.message;
	// 			country_filter.df.default = r.message.split("\n")[0];
	// 			country_filter.refresh();
	// 			country_filter.set_input(year_filter.df.default);
	// 		}
	// 	});
	// }

}

// $(function() {
// 	$(wrapper).bind("show", function() {
// 		frappe.query_report.load();
// 	});
// });