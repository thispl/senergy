// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Fixed Asset Register Report"] = {
	"filters": [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "MultiSelectList",
			get_data: function (txt) {
				return frappe.db.get_link_options('Company', txt)
			}	
		},
		// {
		// 	fieldname: "location",
		// 	label: __("Location"),
		// 	fieldtype: "Select",
		// 	options: ["--Select a Location--", "Kuwait","Iraq", "Sudan","Pakistan"],
		// 	default:"--Select a Location--",
		// 	reqd: 1
		// },
		{
			fieldname: "location",
			label: __("Location"),
			fieldtype: "MultiSelectList",
			get_data: function (txt) {
				return frappe.db.get_link_options('Country', txt, {'reqd': 1} )
			},
		},
		{
			fieldname: "status",
			label: __("Status"),
			fieldtype: "Select",
			options: "In Location\nDisposed",
			default: 'In Location',
			reqd: 1
		},
		{
			"fieldname": "filter_based_on",
			"label": __("Period Based On"),
			"fieldtype": "Select",
			"options": ["Fiscal Year", "Date Range"],
			"default": ["Date Range"],
			"reqd": 1
		},
		{
			"fieldname": "from_date",
			"label": __("Start Date"),
			"fieldtype": "Date",
			"depends_on": "eval: doc.filter_based_on == 'Date Range'",
			"reqd": 1,
			"read_only": 1
		},
		{
			"fieldname": "to_date",
			"label": __("End Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.nowdate(),
			"depends_on": "eval: doc.filter_based_on == 'Date Range'",
			"reqd": 1
		},
		{
			"fieldname": "from_fiscal_year",
			"label": __("Start Year"),
			"fieldtype": "Link",
			"options": "Fiscal Year",
			// "default": frappe.defaults.get_user_default("fiscal_year"),
			"default":"2005",
			"depends_on": "eval: doc.filter_based_on == 'Fiscal Year'",
			"reqd": 1,
			"read_only": 1
			
		},
		{
			"fieldname": "to_fiscal_year",
			"label": __("End Year"),
			"fieldtype": "Link",
			"options": "Fiscal Year",
			"default": frappe.defaults.get_user_default("fiscal_year"),
			"depends_on": "eval: doc.filter_based_on == 'Fiscal Year'",
			"reqd": 1
		},
		{
			"fieldname": "date_based_on",
			"label": __("Date Based On"),
			"fieldtype": "Select",
			"options": ["Purchase Date", "Available For Use Date"],
			"default": "Purchase Date",
			"reqd": 1
		},
		// {
		// 	fieldname: "asset_category",
		// 	label: __("Asset Category"),
		// 	fieldtype: "Link",
		// 	options: "Asset Category"
		// },
		{
			fieldname: "asset_category",
			label: __("Asset Category"),
			fieldtype: "MultiSelectList",
			get_data: function (txt) {
				return frappe.db.get_link_options('Asset Category', txt)
			},
		},
		{
			fieldname: "physical_status",
			label: __("Physical Status"),
			fieldtype: "Select",
			options: ["--Select a Physical Status--", "Operating","Lost in Hole","Junked"],
			default:"--Select a Physical Status--",
			reqd:1
		},
		{
			fieldname: "group_by",
			label: __("Group By"),
			fieldtype: "Select",
			options: ["--Select a group--", "Asset Category", "Location"],
			default: "--Select a group--",
			reqd: 1
		},
		{
			fieldname: "is_existing_asset",
			label: __("Is Existing Asset"),
			fieldtype: "Check"
		},
	],
	onload: function (frm) {
		var company = frappe.defaults.get_user_default('Company')
		// var company = frappe.defaults.get_user_permissions().Company[0].doc
		// if (!company){
		// 	console.log(frappe.defaults.get_user_default('Company'))
		// }
		var company_filter = frappe.query_report.get_filter('company');
		company_filter.df.default = company;
		company_filter.refresh();
		company_filter.set_input(company_filter.df.default);

		var start_date_filter = frappe.query_report.get_filter('from_date');
		frappe.db.get_value('Company', company, ["date_of_establishment"], function (value) {
			start_date_filter.df.default = value["date_of_establishment"];
			start_date_filter.refresh();
			start_date_filter.set_input(start_date_filter.df.default);
		});
	}

};
