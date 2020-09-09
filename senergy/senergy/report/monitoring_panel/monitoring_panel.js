// Copyright (c) 2016, TeamPRO and contributors
// For license information, please see license.txt
/* eslint-disable */
frappe.require("assets/erpnext/js/financial_statements.js", function () {
	frappe.query_reports["Monitoring Panel"] = {
		"filters": [
			{
				"fieldname": "from_date",
				"label": __("From Date"),
				"fieldtype": "Date",
				"width": "80",
				"reqd": 1,
				"hidden": 1,
				"default": frappe.datetime.add_months(frappe.datetime.get_today(), -240),
			},
			{
				"fieldname": "to_date",
				"label": __("To Date"),
				"fieldtype": "Date",
				"width": "80",
				"reqd": 1,
				"hidden": 1,
				"default": frappe.datetime.get_today()
			},
			{
				"fieldname": "company",
				"label": __("Company"),
				"fieldtype": "Link",
				"width": "80",
				"reqd": 1,
				"options": "Company",
			},
			{
				"fieldname": "country",
				"label": __("Country"),
				"fieldtype": "Link",
				"width": "80",
				"reqd": 1,
				"options": "Country",
				"get_query": () => {
					return {
						filters: {
							'reqd': '1'
						}
					};
				}
			},
			{
				"fieldname": "item_group",
				"label": __("Category"),
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
				"get_query": function () {
					return {
						query: "erpnext.controllers.queries.item_query",
					};
				}
			},
			{
				"fieldname": "inventory_type",
				"label": __("Inventory Type"),
				"fieldtype": "Link",
				"options": "Inventory Type",
			},
			{
				"fieldname": "warehouse",
				"label": __("Warehouse"),
				"fieldtype": "MultiSelectList",
				"width": "80",
				get_data: function (txt) {
					company = frappe.query_report.get_filter_value('company');
					country = frappe.query_report.get_filter_value('country');
					if (company && country) {
						return frappe.db.get_link_options('Warehouse', txt, { 'country': country, 'company': company })
					}
					if (company) {
						return frappe.db.get_link_options('Warehouse', txt, { 'company': company })
					}
					if (country) {
						return frappe.db.get_link_options('Warehouse', txt, { 'country': country })
					}
					return frappe.db.get_link_options('Warehouse', txt)
				},
			},
			{
				"fieldname": "currency",
				"label": __("Currency"),
				"fieldtype": "Link",
				"width": "80",
				"options": "Currency"
			},
			{
				"fieldname": 'show_stock_ageing_data',
				"label": __('Show Stock Ageing Data'),
				"fieldtype": 'Check'
			},
		],
		"formatter": function (value, row, column, data, default_formatter) {
			if (column.fieldname=="item_code") {
				value = data["item_code"];

				// column.link_onclick =
				// 	"frappe.query_reports['Profitability Analysis'].open_profit_and_loss_statement(" + JSON.stringify(data) + ")";
				column.is_tree = true;
			}

			value = default_formatter(value, row, column, data);

			if (data["status"] === 'Low Quantity') {
				if (column['fieldname'] == 'status') {
					value = "<span style='color:red!important;font-weight:bold'>" + value + "</span>";
				}

			}
			if (data["status"] === 'Ideal Quantity') {
				if (column['fieldname'] == 'status') {
					value = "<span style='color:green!important;font-weight:bold'>" + value + "</span>";
				}

			}
			if (data["status"] === 'Frozen Item') {
				if (column['fieldname'] == 'status') {
					value = "<span style='color:blue!important;font-weight:bold'>" + value + "</span>";
				}
			}

			// if (!data['parent_warehouse']) {
			// 	value = $(`<span>${value}</span>`);
			// 	var $value = $(value).css("font-weight", "bold");
			// 	value = $value.wrap("<p></p>").parent().html();
			// }
			return value;
		},
		// "formatter": erpnext.financial_statements.formatter,
		"tree": true,
		"name_field": "item_code",
		// "parent_field": "parent_warehouse",
		// "initial_depth": 3,
		onload: function (frm) {
			frappe.breadcrumbs.add('Senergy');
		}
	}

});
