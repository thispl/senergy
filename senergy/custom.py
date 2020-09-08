import frappe
from frappe.utils.csvutils import read_csv_content
from frappe.utils import cint
from frappe.utils.data import today

@frappe.whitelist()
def quality_inspection(name):
    stock = frappe.get_doc("Stock Entry",name)
    for i in stock.items:
        doc = frappe.new_doc("Quality Inspection")
        doc.inspection_type = "Incoming"
        doc.reference_type = "Stock Entry"
        doc.reference_name = stock.name
        doc.status = "Pending"
        doc.item_code = i.item_code
        doc.sample_size = i.qty
        doc.quality_inspection_template = "Material Quality Inspection"
        doc.inspected_by = stock.inspected_by
        doc.inspection_department = stock.inspected_department
        doc.verification_department = stock.department
        for d in stock.inspection_points:
            doc.append("readings",{
                "specification" : d.point,
                "inspection_status":d.yes_no
            })
        doc.verified_by = stock.employee

        doc.save(ignore_permissions=True)
    frappe.db.set_value("Stock Entry",stock.name,"assigned",1)


@frappe.whitelist()
def get_asset_addition(asset):
    if frappe.db.exists("Asset Value Adjustment",{"asset":asset}):
        asset = frappe.get_all("Asset Value Adjustment",{"asset":asset})
        doc = frappe.get_doc("Asset Value Adjustment",asset[0])
        return doc.new_asset_value

@frappe.whitelist()
def movement_approved_by(name,user):
    emp = frappe.get_doc("Employee",{"user_id":user},["employee_name","designation","department"])
    frappe.db.set_value("Asset Movement",name,"approved_by",emp.employee_name)
    frappe.db.set_value("Asset Movement",name,"a_designation",emp.designation)
    frappe.db.set_value("Asset Movement",name,"a_department",emp.department)
    return emp

# @frappe.whitelist()
# def physical_count(company):
#     sle = frappe.db.sql("""select name,company,country,item_code,warehouse from `tabStock Ledger Entry` where company = %s and posting_date = (SELECT MAX(posting_date) FROM `tabStock Ledger Entry` WHERE item_code = name) """,company)
#     return sle

def asset_update():
    assets = frappe.get_all("Asset",{'company':'Eastern Testing Services'})
    frappe.errprint(len(assets))
    for asset in assets:
        doc = frappe.get_doc("Asset",asset.name)
        doc.location = 'Pakistan'
        doc.save(ignore_permissions=True)
        frappe.db.commit()


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
def update_asset():
    assets = frappe.get_all("Asset",{"company":"Eastern National Oilfield Services"})
    frappe.errprint(len(assets))
    for asset in assets:
        doc = frappe.get_doc("Asset",asset.name)
        if not doc.physical_status:
            doc.physical_status = "Operating"
            # doc.tools_condition = "Ready for Operation"
            doc.save(ignore_permissions=True)
            frappe.db.commit()

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
    # for pp in pps:
        # assets = frappe.get_doc("Asset",{'name':pp[0]})
        # for asset in assets:
        # i = frappe.get_doc('Asset',pp[0])
        # frappe.errprint(i.location)
        # if i.qty == 0:
        #     i.qty = pp[1]
        #     # frappe.errprint(pp[1])
        #     i.save(ignore_permissions=True)
        #     frappe.db.commit()
                
                
                
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

def update_item_location():
    sles = frappe.get_all("Stock Ledger Entry",['item_code','name','voucher_no'])
    for sle in sles:
        item_location = frappe.get_value("Stock Entry",sle.voucher_no,"item_location")
        if item_location:
            sleid = frappe.get_doc('Stock Ledger Entry',sle.name)
            sleid.item_location = item_location
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

def push_to_bg():
    from frappe import enqueue
    job = enqueue('erpnext.assets.doctype.asset.depreciation.post_depreciation_entries')

# @frappe.whitelist()
# def physical_count(company,country=None,warehouse=None):
#     filters = ""
#     if country:
#         filters += "and `tabStock Ledger Entry`.country = '%s'" % country
#     if warehouse:
#         filters += "and `tabStock Ledger Entry`.warehouse = '%s'" % warehouse
#     # query = """select name,company,country,item_code,warehouse,qty_after_transaction from `tabStock Ledger Entry` where company = '%s' %s 
#     # and posting_date = (SELECT MAX(posting_date) FROM `tabStock Ledger Entry` WHERE  ) """ % (company,filters)
#     query = """select `tabItem`.name,`tabItem`.item_name,`tabItem`.description,`tabStock Ledger Entry`.company,`tabStock Ledger Entry`.country, `tabStock Ledger Entry`.warehouse,`tabStock Ledger Entry`.posting_date,`tabStock Ledger Entry`.qty_after_transaction from `tabItem`
#     LEFT JOIN `tabStock Ledger Entry` on `tabItem`.name = `tabStock Ledger Entry`.`item_code`
#     WHERE `tabStock Ledger Entry`.company = '%s' %s and `tabStock Ledger Entry`.posting_date = (SELECT MAX(`tabStock Ledger Entry`.posting_date) FROM `tabStock Ledger Entry` 
#     WHERE `tabItem`.name = `tabStock Ledger Entry`.item_code)
#     """ % (company,warehouse)
#     sle = frappe.db.sql(query,as_dict=1)
#     return sle

@frappe.whitelist()
def physical_count(company,country=None,warehouse=None):
    if country:
        country = "and `tabStock Ledger Entry`.country = '%s'" % country
    if warehouse:
        warehouse = "and `tabStock Ledger Entry`.warehouse = '%s'" % warehouse
    # query = """select name,company,country,item_code,warehouse,qty_after_transaction from `tabStock Ledger Entry` where company = '%s' %s 
    # and posting_date = (SELECT MAX(posting_date) FROM `tabStock Ledger Entry` WHERE  ) """ % (company,filters)
    query = """select `tabItem`.name as item,`tabItem`.item_name,`tabItem`.description,`tabStock Ledger Entry`.company,`tabStock Ledger Entry`.country, 
    `tabStock Ledger Entry`.warehouse,`tabStock Ledger Entry`.posting_date,`tabStock Ledger Entry`.qty_after_transaction,
    `tabStock Entry`.name, `tabStock Entry`.item_location
    from `tabItem`
    LEFT JOIN `tabStock Ledger Entry` ON `tabItem`.name = `tabStock Ledger Entry`.`item_code`
    LEFT JOIN `tabStock Entry` ON `tabStock Ledger Entry`.voucher_no = `tabStock Entry`.name
    WHERE `tabStock Ledger Entry`.company = '%s' %s %s and `tabStock Ledger Entry`.posting_time = (SELECT MAX(`tabStock Ledger Entry`.posting_time) FROM `tabStock Ledger Entry` 
    WHERE `tabItem`.name = `tabStock Ledger Entry`.item_code and
    `tabStock Ledger Entry`.posting_date = (SELECT MAX(`tabStock Ledger Entry`.posting_date) FROM `tabStock Ledger Entry` 
    WHERE `tabItem`.name = `tabStock Ledger Entry`.item_code))""" % (company,country,warehouse)
    sle = frappe.db.sql(query,as_dict=1)
    return sle


@frappe.whitelist()
def asset_movement(asset):
    a_mov = frappe.db.sql("""select `tabAsset Movement`.name,`tabAsset Movement`.purpose,`tabAsset Movement`.transaction_date, `tabAsset Movement Item`.asset,`tabAsset Movement Item`.target_location,`tabAsset Movement Item`.source_location FROM `tabAsset Movement`
    LEFT JOIN `tabAsset Movement Item` ON `tabAsset Movement`.name = `tabAsset Movement Item`.parent
    WHERE `tabAsset Movement Item`.asset = '%s' and `tabAsset Movement`.purpose = "Transfer"
    """%(asset),as_dict=True)
    return a_mov

@frappe.whitelist()
def asset_maintenance(asset):
    a_main = frappe.db.sql("""select `tabAsset Maintenance`.name, `tabAsset Maintenance Log`.task_name,
    `tabAsset Maintenance Log`.maintenance_status,`tabAsset Maintenance Log`.asset_maintenance,
    `tabAsset Maintenance Log`.periodicity,`tabAsset Maintenance Log`.assign_to_name,`tabAsset Maintenance Log`.due_date,
    `tabAsset Maintenance Log`.completion_date 
    FROM `tabAsset Maintenance`
    LEFT JOIN `tabAsset Maintenance Log` ON `tabAsset Maintenance`.name = `tabAsset Maintenance Log`.asset_maintenance
    WHERE `tabAsset Maintenance`.name = '%s'
    """ %(asset),as_dict=True)
    return a_main

@frappe.whitelist()
def asset_addition(asset):
    a_add = frappe.db.sql("""select `tabAsset Value Adjustment`.name,`tabAsset Value Adjustment`.date,`tabAsset Value Adjustment`.current_asset_value,
    `tabAsset Value Adjustment`.fixed_asset_addition,`tabAsset Value Adjustment`.new_asset_value,`tabAsset Value Adjustment`.difference
    FROM `tabAsset Value Adjustment`
    WHERE `tabAsset Value Adjustment`.asset = '%s'
    """%(asset),as_dict=True)
    return a_add

@frappe.whitelist()
def asset_repair(asset):
    a_rep = frappe.db.sql("""select `tabAsset Repair`.name,`tabAsset Repair`.failure_date,`tabAsset Repair`.assign_to_name,
    `tabAsset Repair`.completion_date,`tabAsset Repair`.repair_status,`tabAsset Repair`.description,`tabAsset Repair`.actions_performed
    FROM `tabAsset Repair`
    WHERE `tabAsset Repair`.asset_name = '%s'
    """%(asset),as_dict=True)
    return a_rep

@frappe.whitelist()
def asset_disposal(asset):
    a_dis = frappe.db.sql("""select `tabAsset Disposal`.date,`tabAsset Disposal`.method_of_disposal,`tabAsset Disposal`.used_by_name,`tabAsset Disposal`.reason_for_disposal,`tabDisposal Assets`.asset,
    `tabDisposal Assets`.gbv,`tabDisposal Assets`.depreciation_value,`tabDisposal Assets`.nbv
    FROM `tabAsset Disposal`
    LEFT JOIN `tabDisposal Assets` ON `tabAsset Disposal`.name = `tabDisposal Assets`.parent
    WHERE `tabDisposal Assets`.asset = '%s' and `tabAsset Disposal`.workflow_state = "Approved"
    """%(asset),as_dict=True)
    return a_dis

# @frappe.whitelist()
# def get_po_number(name):
#     po = frappe.db.sql("""select `tabPurchase Receipt`.name, `Purchase Receipt Item`.purchase_order,`tabPurchase Order`.name
#     FROM `tabPurchase Receipt`
#     LEFT JOIN `tabPurchase Receipt Item` ON `tabPurchase Receipt.name = `tabPurchase Receipt`.parent
#     LEFT JOIN `tabPurchase Order` ON `tabPurchase Order`.name = `tabPurchase Receipt Item`.purchase_order""")