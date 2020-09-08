
frappe.listview_settings['Asset Disposal'] = {
    refresh(frm) {
        if (frappe.user.has_role("Verifier")) {
            if (!frappe.route_options) {
                frappe.route_options = {
                    "workflow_state": ["=", "Review Pending"]
                };
            }
        }
        else if (frappe.user.has_role("Approver")) {
            if(!frappe.user.has_role("System Manager")){
            if (!frappe.route_options) {
                frappe.route_options = {
                    "workflow_state": ["=", "Approval Pending"]
                };
            }
        }
        }
    }
}