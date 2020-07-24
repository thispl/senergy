// frappe.query_reports["Physical Count Reconciliation Report"] = {
//     "filters": [
// 		{
// 			"fieldname":"company",
// 			"label": __("Company"),
//             "fieldtype": "Link",
//             "options": "Company",
// 			"width": "80",
//         },
//         {
// 			"fieldname":"country",
// 			"label": __("Country"),
// 			"fieldtype": "Link",
//             "width": "80",
//             "options": "Country",
//             "default":"Kuwait"
//         },
//         {
// 			"fieldname":"warehouse",
// 			"label": __("Warehouse"),
// 			"fieldtype": "Link",
//             "width": "80",
//             "options": "Warehouse",
//             get_query: () => {
// 				var company = frappe.query_report.get_filter_value('company');
// 				if(company){
// 					return {
// 						filters: {
// 							'company': company
// 						}
// 					};
//                 }
//             }
//         }
//     ],
//     onload:function(frm){
// 		frappe.breadcrumbs.add('Senergy');
// 	}
// };