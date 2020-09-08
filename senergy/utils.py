from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import cstr, today, flt, add_years, formatdate, getdate
from erpnext.accounts.report.financial_statements import get_period_list, get_fiscal_year_data, validate_fiscal_year

def create_asset_log():
    fields = ["company","name as asset_id", "asset_name", "status", "department", "cost_center", "purchase_receipt",
            "asset_category", "purchase_date", "gross_purchase_amount", "location",
            "available_for_use_date", "purchase_invoice", "opening_accumulated_depreciation","physical_status","tools_condition","asset_group","asset_sub_group"]

    assets_record = frappe.db.get_all("Asset", filters={'docstatus':('!=','2')},fields=fields)

    depreciation_amount_map = get_finance_book_value_map()
    pr_supplier_map = get_purchase_receipt_supplier_map()
    pi_supplier_map = get_purchase_invoice_supplier_map()

    for asset in assets_record:
        asset_value = asset.gross_purchase_amount - flt(asset.opening_accumulated_depreciation) \
            - flt(depreciation_amount_map.get(asset.name))
        net_asset_value = asset_value - flt(depreciation_amount_map.get(asset.asset_id))
        asset_addition = frappe.db.sql("""select sum(fixed_asset_addition) as addition from `tabAsset Value Adjustment` where asset = %s """,asset.asset_id,as_dict=1)
        if asset_value:
            asset_log = frappe.db.exists('Asset Log',asset.asset_id)
            if asset_log:
                asset_log_id = frappe.get_doc('Asset Log',asset.asset_id)
            else:
                asset_log_id = frappe.new_doc('Asset Log')
            asset_log_id.update({
                "asset_id": asset.asset_id,
                "company": asset.company,
                "asset_name": asset.asset_name,
                "status": asset.status,
                "department": asset.department,
                "cost_center": asset.cost_center,
                "asset_group": asset.asset_group,
                "asset_sub_group": asset.asset_sub_group,
                "asset_addition":asset_addition[0].addition,
                "vendor_name": pr_supplier_map.get(asset.purchase_receipt) or pi_supplier_map.get(asset.purchase_invoice),
                "gross_purchase_amount": asset.gross_purchase_amount,
                "opening_accumulated_depreciation": asset.opening_accumulated_depreciation,
                "depreciated_amount": depreciation_amount_map.get(asset.asset_id) or 0.0,
                "available_for_use_date": asset.available_for_use_date,
                "location": asset.location,
                "asset_category": asset.asset_category,
                "purchase_date": asset.purchase_date,
                "asset_value": asset_value,
                "net_asset_value": net_asset_value,
                "physical_status" :asset.physical_status,
                "tools_condition" : asset.tools_condition
            })   
            asset_log_id.save(ignore_permissions=True)
            frappe.db.commit() 
        


def get_finance_book_value_map():
    return frappe._dict(frappe.db.sql(''' Select
        parent, SUM(depreciation_amount)
        FROM `tabDepreciation Schedule`
        WHERE
            parentfield='schedules'
            AND journal_entry IS NOT NULL
        GROUP BY parent'''))

def get_purchase_receipt_supplier_map():
    return frappe._dict(frappe.db.sql(''' Select
        pr.name, pr.supplier
        FROM `tabPurchase Receipt` pr, `tabPurchase Receipt Item` pri
        WHERE
            pri.parent = pr.name
            AND pri.is_fixed_asset=1
            AND pr.docstatus=1
            AND pr.is_return=0'''))

def get_purchase_invoice_supplier_map():
    return frappe._dict(frappe.db.sql(''' Select
        pi.name, pi.supplier
        FROM `tabPurchase Invoice` pi, `tabPurchase Invoice Item` pii
        WHERE
            pii.parent = pi.name
            AND pii.is_fixed_asset=1
            AND pi.docstatus=1
            AND pi.is_return=0'''))

def cancel_all_assets():
    import json
    from frappe.desk.form.linked_with import get_submitted_linked_docs, cancel_all_linked_docs

    assets_list = frappe.get_all('Asset',{'company':'Eastern National Oilfield Services','new_asset':1},['name'])
    for assets in assets_list:
        asset = frappe.get_doc('Asset',assets.name)
        docs = get_submitted_linked_docs('Asset',asset.name)
        dump_docs = json.dumps(docs.get('docs'))
        cancel_all_linked_docs(dump_docs)
        asset.cancel()
        return

def cancel_gl():
    assets_list = frappe.get_all('Asset',{'company':'Eastern National Oilfield Services','new_asset':0},['name'])
    for assets in assets_list:
        # asset = frappe.get_doc('Asset',assets.name)
        gls = frappe.get_all('GL Entry',{'against_voucher':"ACC-ASS-2020-00257"})
        for gl in gls:
            if gl.name != "ACC-GLE-2020-05481":
                gl = frappe.get_doc("GL Entry",gl.name)
                # frappe.errprint(gl.name)
                gl.cancel()

@frappe.whitelist(allow_guest=True)
def get_rfq_items(rfq):
    return frappe.get_all('Request for Quotation Item',{'parent':rfq},['item_code','item_name','qty','warehouse','uom'])

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