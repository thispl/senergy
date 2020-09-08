frappe.listview_settings['Fixed Asset Request'] = {
    onload: () => {
        frappe.breadcrumbs.add({
            type: 'Custom',
            module: __('Assets'),
            label: __('Assets'),
            route: '#workspace/Assets'
        });
    }
}