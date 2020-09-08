frappe.pages['asset-dashboard'].on_page_load = function (wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Asset Dashboard',
		single_column: false
	});
	console.log(page);
	$(frappe.render_template('asset_dashboard')).appendTo(page.body);
	$(frappe.render_template('asset_dashboard_sidebar')).appendTo(page.sidebar);
}