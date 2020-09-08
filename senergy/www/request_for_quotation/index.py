import frappe

no_cache = 1


def get_context(context):
    context.no_cache = 1
    context.user = frappe.session.user
    context.rfq_list = get_rfq_list()


def get_rfq_list():
    rfq_list = []
    supplier = frappe.get_value(
        'User', {'email': 'supplier@senergy.com'}, ['supplier'])
    rfqs_list = frappe.get_all('Request for Quotation Supplier', filters={
                               'supplier': supplier}, fields=['parent'])
    for rfqs in rfqs_list:
        submitted = False
        po_released = False
        rfq = frappe.get_value('Request for Quotation', {
                               'name': rfqs.parent, 'docstatus': 1})
        if rfq:
            sqtn = frappe.db.exists('Supplier Quotation', {
                                    'rfq': rfq, 'supplier': supplier})
            if sqtn:
                submitted = True
            po = frappe.db.exists('Purchase Order', {'sqtn': sqtn, 'docstatus': 1})
            if po:
                po_released = True
            rfq_list.append(frappe._dict({
                'rfq': rfq,
                'submitted': submitted,
                'sqtn':sqtn,
                'po_released': po_released
            }))
    return rfq_list
