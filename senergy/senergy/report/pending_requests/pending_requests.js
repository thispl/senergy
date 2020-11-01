// Copyright (c) 2016, TeamPRO and contributors
// For license information, please see license.txt
/* eslint-disable */
	frappe.query_reports["Pending Requests"] = {
		"formatter": function (value, row, column, data, default_formatter) {
            value = default_formatter(value, row, column, data);
			if (data["Approval Status"] === 'Approved') {
				if (column['fieldname'] == 'Approval Status') {
					value = "<span style='color:green!important;font-weight:bold'>" + value + "</span>";
				}

            }
            if (data["Approval Status"] === 'Rejected') {
				if (column['fieldname'] == 'Approval Status') {
					value = "<span style='color:red!important;font-weight:bold'>" + value + "</span>";
				}

            }
            if (data["Approval Status"] === 'Review Pending' || data["Approval Status"] === 'Approval Pending') {
				if (column['fieldname'] == 'Approval Status') {
					value = "<span style='color:yellow!important;font-weight:bold'>" + value + "</span>";
				}

			}
			
			return value;
		},
		onload: function (frm) {
			frappe.breadcrumbs.add('Senergy');
		}
	}

