import frappe
from frappe.utils.csvutils import read_csv_content
from frappe.utils import cint
from frappe.utils.data import today

def get_countries(doctype, txt, searchfield, start, page_len, filters, as_dict=False):
    return (('Kuwait','Iraq','Pakistan','Sudan'))

def maintenance_due_date_alert():
    log = frappe.get_all("Asset Maintenance Log",{"due_date":today(),"maintenance_status":"Planned"},["asset_maintenance","assign_to_name"])
    for l in log:
        maintenance = frappe.get_doc("Asset Maintenance",l.asset_maintenance)
        for m in maintenance.asset_maintenance_tasks:
            if m.assign_to_name == l.assign_to_name:
                frappe.sendmail(
                    recipients= m.assign_to,
                    subject='Asset Maintenance Due Date Alert',
                    message="""
                    <h3>Asset Maintenance Due Date Alert</h3>
                    <p>Dear %s,</p>
                    <h4>Info:</h4>
                    <p>Asset <b>%s</b> Maintenance Due Date is Today<br>Regards,<br>ERP Admin"""
                    % (m.assign_to_name,maintenance.item_code)
                )

def maintenance_completion_mail(doc,method):
    maintenance = frappe.get_doc("Asset Maintenance",doc.asset_maintenance)
    team = frappe.get_doc("Asset Maintenance Team",maintenance.maintenance_team)
    frappe.sendmail(
                    recipients= team.maintenance_manager,
                    subject='Asset Maintenance Completion Mail',
                    message="""
                    <h3>Asset Maintenance Completion Mail</h3>
                    <p>Dear %s,</p>
                    <h4>Info:</h4>
                    <p>Maintenance for Asset-<b>%s</b> was completed by %s<br>Regards,<br>ERP Admin"""
                    % (team.maintenance_manager_name,doc.asset_name,doc.assign_to_name)
                )

def minimum_stock_alert(doc,method):
    slen = frappe.get_list('Stock Ledger Entry',{'voucher_no':doc.name},["*"])
    for s in slen:
        item = frappe.get_doc("Item",s.item_code)
        child = item.reorder_levels
        if s.actual_qty < 0:
            for c in child:
                if c.warehouse == s.warehouse:
                    if c.warehouse_reorder_level >= s.qty_after_transaction:
                        recipient = frappe.get_doc("Warehouse",s.warehouse)
                        recip = recipient.recipients
                        for r in recip:
                            frappe.sendmail(
                                        recipients= r.email_id,
                                        subject='Stock Minimum Quantity Alert',
                                        message="""
                                        <h3>Stock Minimum Quantity Alert</h3>
                                        <p>Dear Team,</p>
                                        <h4>Info:</h4>
                                        <p>Stock Balance for Item <b>%s</b> in Warehouse <b>%s</b> is <b>%s</b> <br> Regards <br>ERP Admin"""
                                        % (s.item_code,s.warehouse,s.qty_after_transaction)
                                    )

def bulk_update_from_csv(filename):
    #below is the method to get file from Frappe File manager
    from frappe.utils.file_manager import get_file
    #Method to fetch file using get_doc and stored as _file
    _file = frappe.get_doc("File", {"file_name": filename})
    #Path in the system
    filepath = get_file(filename)
    #CSV Content stored as pps

    pps = read_csv_content(filepath[1])
    count = 0
    for pp in pps:
        cl = frappe.db.exists("Item",{'description':pp[0]})
        if cl:
            items = frappe.get_all("Item",{'description':pp[0]})
            for item in items:
                i = frappe.get_doc('Item',item.name)
                if not i.supplier_items:
                    i.append("supplier_items",{
                        'supplier' : pp[1]
                    })
                    i.save(ignore_permissions=True)
                    frappe.db.commit()
                # for it in i.supplier_items:
                #     frappe.errprint(it.supplier_part_no)
                #     # frappe.errprint(pp[1])
                #     if not it.supplier:
                #         i
                #         it.supplier = pp[1]
                #         it.save(ignore_permissions=True)
                #         frappe.db.commit()

            # exists = frappe.db.exists('Stock Entry Detail',{'item_code':item.name})
            # if exists:
            #     ste = frappe.get_value('Stock Entry Detail',{'item_code':item.name},['parent'])
            #     print(ste)
            # # if not exists:
            # ste = frappe.new_doc('Stock Entry')
            # ste.stock_entry_type = 'Material Receipt'
            # ste.company = 'Eastern Testing Services'
            # ste.append("items", {
            #     'item_code': item.name,
            #     't_warehouse': 'Stores - ETS',
            #     'qty':cint(pp[1]),
            #     'uom' : 'Nos',
            #     'cost_center': 'Main - ETS'
            #     })
            # ste.save(ignore_permissions=True)
            # # ste.submit()
            # frappe.db.commit()    
            # count += 1

def save_sle():
    sles = frappe.get_all('Stock Ledger Entry',['name','item_code'])  
    for sle in sles:
        sleid = frappe.get_doc('Stock Ledger Entry',sle.name)
        sleid.inventory_type = frappe.get_value('Item',sleid.item_code,'inventory_type')
        sleid.db_update()
        return 
        # sleid.save(ignore_permissions=True)

def update_country():
    items = frappe.get_all("Item")
    for item in items:
        i = frappe.get_doc("Item",item.name)
        for s in i.item_defaults:
            company = frappe.get_doc("Company",i.company)
            frappe.errprint(company.country)
            if not s.country:
                s.country = company.country
                frappe.errprint(i.name)
                i.save(ignore_permissions=True)
                frappe.db.commit()

def update_part_no():
    sles = frappe.get_all("Stock Ledger Entry",['item_code','name'])
    for sle in sles:
        itemid = frappe.get_doc("Item",sle.item_code)
        supplier_info = frappe.get_value('Item Supplier',{'parent':itemid.name},['supplier','supplier_part_no'])
        if supplier_info:
            sleid = frappe.get_doc('Stock Ledger Entry',sle.name)
            # print(supplier_info[1])
            sleid.supplier = supplier_info[0]
            sleid.supplier_part_no = supplier_info[1]
            sleid.db_update()
            frappe.db.commit()
            # return

def movement_status():
    movement = frappe.get_all("Item")
    for move in movement:
        m = frappe.get_doc("Item",move.name)
        frappe.errprint(m.name)
        m.movement_status = ""
        m.save(ignore_permissions=True)
        frappe.db.commit()