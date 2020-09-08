frappe.ui.form.on('Asset Disposal', {
	refresh(frm) {
		if (!frm.doc.__islocal) {
			if (frm.doc.workflow_state == "Approved") {
				frm.add_custom_button(__("Print Receipt"), function () {
					var f_name = frm.doc.name
					var print_format = "Asset Disposal";
					window.open(frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
						+ "doctype=" + encodeURIComponent("Asset Disposal")
						+ "&name=" + encodeURIComponent(f_name)
						+ "&trigger_print=1"
						+ "&format=" + print_format
						+ "&no_letterhead=0"
					));
				})
			}
		}
	},
	after_workflow_action(frm) {
		if (in_list(["Scrapped", "Lost"], frm.doc.method_of_disposal)) {
			if (frm.doc.workflow_state == "Approved") {
				$.each(frm.doc.table_10,function(i,d){
					frappe.call({
						args: {
							"asset_name": d.asset
						},
						method: "erpnext.assets.doctype.asset.depreciation.scrap_asset",
						callback: function (r) {
							cur_frm.reload_doc();
						}
					})
				})
			}
		}
		else if (frm.doc.method_of_disposal == "Sold") {
			if (frm.doc.workflow_state == "Approved") {
				frappe.call({
					method: "senergy.fixed_assets.doctype.asset_disposal.asset_disposal.make_sales_invoice",
					args: {
						"name":frm.doc.name
					},
					callback: function (r) {
						var doclist = frappe.model.sync(r.message);
						frappe.set_route("Form", doclist[0].doctype, doclist[0].name);
					}
		
				})
			}
		}
	},
	onload(frm) {
		frm.fields_dict['table_10'].grid.get_field("asset").get_query = function (doc, cdt, cdn) {
			return {
				filters: [
					['Asset', 'company', '=', frm.doc.company]
				]
			}
		}
	},
	asset_name(frm) {
		frappe.call({
			method: "frappe.client.get",
			args: {
				"doctype": "Asset",
				'name': frm.doc.asset_name
			},
			callback(r) {
				var dep_amt = 0;
				$.each(r.message.schedules, function (i, d) {
					if (d.journal_entry) {
						dep_amt += d.depreciation_amount
					}
				})
				var gbv = r.message.gross_purchase_amount - r.message.opening_accumulated_depreciation;
				var opening_dep = r.message.opening_accumulated_depreciation;
				var nbv = gbv - dep_amt;
				frm.set_value("total_depreciation_value", dep_amt)
				frm.set_value("total_gbv", gbv)
				frm.set_value("total_nbv", nbv)
				frm.clear_table("table_10");
				var row = frappe.model.add_child(frm.doc, "Disposal Assets", "table_10");
				row.asset = frm.doc.asset_name;
				row.depreciation_value = dep_amt;
				row.purchase_date = r.message.purchase_date;
				row.gbv = gbv;
				row.nbv = nbv;
				row.location = r.message.location;
				refresh_field("table_10")
			}
		})

	},

	company(frm) {
		if (frm.doc.company == "Senergy Services Company") {
			frm.fields_dict.naming_series.df.options = 'SSC-Disposal.-';
			frm.fields_dict.naming_series.df.default = 'SSC-Disposal.-';
			refresh_field("naming_series");
		}
		if (frm.doc.company == 'Eastern National Oilfield Services') {
			frm.fields_dict.naming_series.df.options = 'ENOS-Disposal.-';
			frm.fields_dict.naming_series.df.default = 'ENOS-Disposal.-';
			refresh_field("naming_series");
		}
		if (frm.doc.company == 'Eastern International Testing Services') {
			frm.fields_dict.naming_series.df.options = 'EITS-Disposal.-';
			frm.fields_dict.naming_series.df.default = 'EITS-Disposal.-';
			refresh_field("naming_series");
		}
		if (frm.doc.company == 'Eastern Testing Services') {
			frm.fields_dict.naming_series.df.options = 'ETS-Disposal.-';
			frm.fields_dict.naming_series.df.default = 'ETS-Disposal.-';
			refresh_field("naming_series");
		}
		if (frm.doc.company == 'Gulf International General Trading') {
			frm.fields_dict.naming_series.df.options = 'GIGT-Disposal.-';
			frm.fields_dict.naming_series.df.default = 'GIT-Disposal.-';
			refresh_field("naming_series");
		}
	}
})

frappe.ui.form.on('Disposal Assets', {
	asset(frm, cdn, cdt) {
		var child = locals[cdn][cdt]
		frappe.call({
			method: "frappe.client.get",
			args: {
				"doctype": "Asset",
				'name': child.asset
			},
			callback(r) {
				var dep_amt = 0;
				$.each(r.message.schedules, function (i, d) {
					if (d.journal_entry) {
						dep_amt += d.depreciation_amount
					}
				})
				var gbv = r.message.gross_purchase_amount - r.message.opening_accumulated_depreciation;
				var opening_dep = r.message.opening_accumulated_depreciation;
				var nbv = gbv - dep_amt;
				child.depreciation_value = dep_amt;
				child.purchase_date = r.message.purchase_date;
				child.gbv = gbv;
				child.nbv = nbv;
				child.location = r.message.location;
				refresh_field("table_10")
				var total_nbv = 0
				var total_gbv = 0
				var total_dep = 0
				$.each(frm.doc.table_10, function (i, d) {
					if (d.nbv > 0) {
						total_nbv += d.nbv
					}
					if (d.gbv > 0) {
						console.log(d.gbv)
						total_gbv += d.gbv
					}
					if (d.depreciation_value > 0) {
						total_dep += d.depreciation_value
					}
				})
				// frm.set_value("disposal_value",total_nbv)
				frm.set_value("total_nbv",total_nbv)
				frm.set_value("total_gbv",total_gbv)
				frm.set_value("total_depreciation_value",total_dep)
			}
		})
	}
})