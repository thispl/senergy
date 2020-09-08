# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import cstr, today, flt, add_years, formatdate, getdate
from erpnext.accounts.report.financial_statements import get_period_list, get_fiscal_year_data, validate_fiscal_year

def execute(filters=None):
    filters = frappe._dict(filters or {})
    columns = get_columns(filters)
    data = get_data(filters)
    # chart = prepare_chart_data(data, filters) if filters.get("group_by") not in ("Asset Category", "Location") else {}

    return columns, data, None

def get_conditions(filters):
    conditions = { 'docstatus': 1 }
    status = filters.status
    date_field = frappe.scrub(filters.date_based_on or "Purchase Date")

    if filters.get('company'):
        filters.company = frappe.parse_json(filters.get('company'))	
        conditions['company'] = ('in', filters.company)
    
    # if filters.get('location'):
    #     if not filters.get('location') == '--Select a Location--':
    #         conditions["location"] = filters.location

    if filters.get('location'):
        filters.location = frappe.parse_json(filters.get('location'))	
        conditions['location'] = ('in', filters.location)

    if filters.get('asset_category'):
        filters.asset_category = frappe.parse_json(filters.get('asset_category'))	
        conditions['asset_category'] = ('in', filters.asset_category)

    if filters.get('physical_status'):
        if not filters.get('physical_status') == '--Select a Physical Status--':
            conditions["physical_status"] = filters.physical_status	
            
    if filters.filter_based_on == "Date Range":
        conditions[date_field] = ["between", [filters.from_date, filters.to_date]]
    if filters.filter_based_on == "Fiscal Year":
        fiscal_year = get_fiscal_year_data(filters.from_fiscal_year, filters.to_fiscal_year)
        validate_fiscal_year(fiscal_year, filters.from_fiscal_year, filters.to_fiscal_year)
        filters.year_start_date = getdate(fiscal_year.year_start_date)
        filters.year_end_date = getdate(fiscal_year.year_end_date)

        conditions[date_field] = ["between", [filters.year_start_date, filters.year_end_date]]
    if filters.get('is_existing_asset'):
        conditions["is_existing_asset"] = filters.get('is_existing_asset')
    # if filters.get('asset_category'):
        # conditions["asset_category"] = filters.get('asset_category')
    if filters.get('cost_center'):
        conditions["cost_center"] = filters.get('cost_center')

    # In Store assets are those that are not sold or scrapped
    operand = 'not in'
    if status not in 'In Location':
        operand = 'in'

    conditions['status'] = (operand, ['Sold', 'Scrapped'])

    return conditions

def get_data(filters):

    data = []
    row = []

    conditions = get_conditions(filters)
    condition = ''
    addnl_condition = ''
    depreciation_amount_map = get_finance_book_value_map(filters)
    pr_supplier_map = get_purchase_receipt_supplier_map()
    pi_supplier_map = get_purchase_invoice_supplier_map()
    group_by = frappe.scrub(filters.get("group_by"))

    if not filters.get("group_by") == "--Select a group--":
        condition = " and asset.status not in ('Sold','Scrapped')"
        if filters.status == 'Disposed':
            condition = " and asset.status in ('Sold','Scrapped')"

        # if filters.get('company'):
        #     company = filters.get("company")
        #     condition += " and asset.company = '%s'" % company

        if filters.get('company'):
            company = frappe.parse_json(filters.get('company'))	
            company_list = ', '.join('"{0}"'.format(c) for c in company)
            condition += " and asset.company in (" + company_list + ")"
        # if not filters.get("location") == "--Select a Location--":
        #     location = filters.get("location")
        #     condition += " and asset.location = '%s'" % location

        if filters.get('location'):
            location = frappe.parse_json(filters.get('location'))
            location_list = ', '.join('"{0}"'.format(l) for l in location)	
            condition += " and asset.location in (" + location_list + ")"

        if group_by == "asset_category":
            fields=["asset_category",  "sum(gross_purchase_amount) as gross_purchase_amount", "sum(opening_accumulated_depreciation) as opening_accumulated_depreciation"]
            date = filters.to_date if filters.filter_based_on == "Date Range" else filters.year_end_date
            assets_records = frappe.get_all("Asset", filters= conditions, fields=fields, group_by=group_by)
            for asset in assets_records:
                ds = frappe.db.sql(query = '''Select
                        SUM(ds.depreciation_amount) as depreciation_amount
                        FROM 
                        `tabDepreciation Schedule` ds
                        join `tabAsset` as asset on asset.name = ds.parent 
                        WHERE
                            ds.parentfield='schedules'
                            AND ds.schedule_date<= '{0}'
                            AND ds.journal_entry IS NOT NULL
                            AND asset.docstatus = 1
                            AND asset.asset_category = '{1}'
                            {2}
                            '''.format(date,asset.asset_category,condition),as_dict=True)[0]

                ava = frappe.db.sql('''Select
                        SUM(ava.fixed_asset_addition) as asset_addition
                        FROM 
                        `tabAsset Value Adjustment` ava
                        join `tabAsset` as asset on asset.name = ava.asset
                        WHERE 
                        ava.docstatus = 1
                        AND asset.docstatus = 1
                        AND asset.asset_category = '{0}'
                        {1}
                        '''.format(asset.asset_category,condition),as_dict=True)[0]
                            
                gross_asset_value = asset.gross_purchase_amount - asset.opening_accumulated_depreciation
                net_asset_value = gross_asset_value - flt(ds.depreciation_amount) or 0.0 

                if ava:
                    net_asset_value = (gross_asset_value - flt(ds.depreciation_amount) or 0.0) + flt(ava.asset_addition)

                row = [asset.asset_category, asset.gross_purchase_amount, asset.opening_accumulated_depreciation, gross_asset_value, ds.depreciation_amount or 0.0, net_asset_value]
                data.append(row)

        elif group_by == "location":
            fields=["location", "sum(gross_purchase_amount) as gross_purchase_amount", "sum(opening_accumulated_depreciation) as opening_accumulated_depreciation"]
            date = filters.to_date if filters.filter_based_on == "Date Range" else filters.year_end_date
            assets_records = frappe.get_all("Asset", filters= conditions, fields=fields, group_by=group_by)

            for asset in assets_records:
                ds = frappe.db.sql('''Select
                        SUM(ds.depreciation_amount) as depreciation_amount
                        FROM 
                        `tabDepreciation Schedule` ds
                        join `tabAsset` as asset on asset.name = ds.parent 
                        WHERE
                            ds.parentfield='schedules'
                            AND ds.schedule_date<= '{0}'
                            AND ds.journal_entry IS NOT NULL
                            AND asset.docstatus = 1
                            AND asset.location = '{1}'
                            {2}
                            '''.format(date,asset.location,condition),as_dict=True)[0]

                ava = frappe.db.sql('''Select
                        SUM(ava.fixed_asset_addition) as asset_addition
                        FROM 
                        `tabAsset Value Adjustment` ava
                        join `tabAsset` as asset on asset.name = ava.asset
                        WHERE 
                        ava.docstatus = 1
                        AND asset.docstatus = 1
                        AND asset.location = '{0}'
                        {1}
                        '''.format(asset.location,condition),as_dict=True)[0]

                gross_asset_value = asset.gross_purchase_amount - asset.opening_accumulated_depreciation
                net_asset_value = gross_asset_value - flt(ds.depreciation_amount) or 0.0

                if ava:
                    net_asset_value = (gross_asset_value - flt(ds.depreciation_amount) or 0.0) + flt(ava.asset_addition)

                row = [asset.location, asset.gross_purchase_amount, asset.opening_accumulated_depreciation, gross_asset_value, ds.depreciation_amount or 0.0, net_asset_value]
                data.append(row)

        
        # asset_value = group.gross_purchase_amount - flt(group.opening_accumulated_depreciation)
        # net_asset_value =  (asset_value - flt(group.depreciation_amount)) + flt(group.asset_addition)

        # if asset_addition:
        # 	net_asset_value = (asset_value - flt(depreciation_amount_map.get(asset.asset_id))) + flt(asset_addition[0].addition)
        # else:
        # 	net_asset_value = asset_value - flt(depreciation_amount_map.get(asset.asset_id))
        # row = {
        # 	    "asset_category": group.asset_category,
        # 		"location": group.location,
        # 		"gross_purchase_amount": group.gross_purchase_amount,
        # 		"opening_accumulated_depreciation": group.opening_accumulated_depreciation,
        # 		"asset_value": asset_value,
        # 		"depreciated_amount": group.depreciation_amount,
        # 		"net_asset_value": net_asset_value,
        # 	}
            
    else:
        fields = ["name as asset_id", "asset_name", "status", "department", "cost_center", "purchase_receipt",
            "asset_category", "purchase_date", "gross_purchase_amount", "location",
            "available_for_use_date", "purchase_invoice", "opening_accumulated_depreciation","physical_status","item_code","tools_condition","asset_group","asset_sub_group","qty"]
        assets_record = frappe.db.get_all("Asset", filters=conditions, fields=fields)
        for asset in assets_record:
            asset_value = asset.gross_purchase_amount - flt(asset.opening_accumulated_depreciation) \
                - flt(depreciation_amount_map.get(asset.name))
            asset_addition = frappe.db.sql("""select sum(fixed_asset_addition) as addition from `tabAsset Value Adjustment` where asset = %s """,asset.asset_id,as_dict=1)
            if asset_addition:
                net_asset_value = (asset_value - flt(depreciation_amount_map.get(asset.asset_id))) + flt(asset_addition[0].addition)
            else:
                net_asset_value = asset_value - flt(depreciation_amount_map.get(asset.asset_id))
            if asset_value:
                row = {
                    "asset_id": asset.asset_id,
                    "asset_name": asset.asset_name,
                    "status": asset.status,
                    "department": asset.department,
                    "cost_center": asset.cost_center,
                    "asset_group": asset.asset_group,
                    "asset_sub_group": asset.asset_sub_group,
                    "asset_addition":asset_addition[0].addition,
                    "vendor_name": pr_supplier_map.get(asset.purchase_receipt) or pi_supplier_map.get(asset.purchase_invoice),
                    "part_number":frappe.get_value('Item',asset.item_code,"part_number"),
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
                    "tools_condition" : asset.tools_condition,
                    "description" : frappe.get_value('Item',asset.item_code,"description"),
                    "qty" : asset.qty
                }
                data.append(row)

    return data

def prepare_chart_data(data, filters):
    labels_values_map = {}
    date_field = frappe.scrub(filters.date_based_on)

    period_list = get_period_list(filters.from_fiscal_year, filters.to_fiscal_year, 
        filters.from_date, filters.to_date, filters.filter_based_on, "Monthly", company=filters.company)

    for d in period_list:
        labels_values_map.setdefault(d.get('label'), frappe._dict({'asset_value': 0, 'depreciated_amount': 0}))

    for d in data:
        date = d.get(date_field)
        belongs_to_month = formatdate(date, "MMM YYYY")

        labels_values_map[belongs_to_month].asset_value += d.get("asset_value")
        labels_values_map[belongs_to_month].depreciated_amount += d.get("depreciated_amount")

    return {
        "data" : {
            "labels": labels_values_map.keys(),
            "datasets": [
                { 'name': _('Asset Value'), 'values': [d.get("asset_value") for d in labels_values_map.values()] },
                { 'name': _('Depreciatied Amount'), 'values': [d.get("depreciated_amount") for d in labels_values_map.values()] }
            ]
        },
        "type": "bar",
        "barOptions": {
            "stacked": 1
        },
    }

def get_finance_book_value_map(filters):
    date = filters.to_date if filters.filter_based_on == "Date Range" else filters.year_end_date
    return frappe._dict(frappe.db.sql(''' Select
        parent, SUM(depreciation_amount)
        FROM `tabDepreciation Schedule`
        WHERE
            parentfield='schedules'
            AND schedule_date<=%s
            AND journal_entry IS NOT NULL
            AND ifnull(finance_book, '')=%s
        GROUP BY parent''', (date, cstr(filters.finance_book or ''))))


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

def get_columns(filters):
    if filters.get("group_by") in ["Asset Category", "Location"]:
        return [
            {
                "label": _("{}").format(filters.get("group_by")),
                "fieldtype": "Link",
                "fieldname": frappe.scrub(filters.get("group_by")),
                "options": filters.get("group_by"),
                "width": 120
            },
            {
                "label": _("Gross Purchase Amount"),
                "fieldname": "gross_purchase_amount",
                "fieldtype": "Currency",
                "options": "company:currency",
                "width": 180
            },
            {
                "label": _("Opening Accumulated Depreciation"),
                "fieldname": "opening_accumulated_depreciation",
                "fieldtype": "Currency",
                "options": "company:currency",
                "width": 180
            },
            {
                "label": _("Gross Asset Value"),
                "fieldname": "asset_value",
                "fieldtype": "Currency",
                "options": "company:currency",
                "width": 180
            },
            {
                "label": _("Depreciated Amount"),
                "fieldname": "depreciated_amount",
                "fieldtype": "Currency",
                "options": "company:currency",
                "width": 180
            },
            
            {
                "label": _("Net Asset Value"),
                "fieldname": "net_asset_value",
                "fieldtype": "Currency",
                "options": "company:currency",
                "width": 180
            }
        ]

    return [
        {
            "label": _("Asset Id"),
            "fieldtype": "Link",
            "fieldname": "asset_id",
            "options": "Asset",
            "width": 80
        },
        {
            "label": _("Description"),
            "fieldtype": "Data",
            "fieldname": "description",
            "width": 140
        },
        {
            "label": _("Asset Name"),
            "fieldtype": "Data",
            "fieldname": "asset_name",
            "width": 140
        },
        {
            "label": _("Asset Group"),
            "fieldtype": "Link",
            "fieldname": "asset_group",
            "options": "Asset Group",
            "width": 100
        },
        {
            "label": _("Asset Sub Group"),
            "fieldtype": "Link",
            "fieldname": "asset_sub_group",
            "options": "Asset Sub Group",
            "width": 100
        },
        {
            "label": _("Asset Category"),
            "fieldtype": "Link",
            "fieldname": "asset_category",
            "options": "Asset Category",
            "width": 100
        },
        {
            "label": _("Physical Location"),
            "fieldtype": "Link",
            "fieldname": "location",
            "options": "Location",
            "width": 100
        },
        {
            "label": _("Part Number"),
            "fieldtype": "Data",
            "fieldname": "part_number",
            "width": 100
        },
        {
            "label": _("Status"),
            "fieldtype": "Data",
            "fieldname": "status",
            "width": 80
        },
        {
            "label": _("Qty"),
            "fieldtype": "Int",
            "fieldname": "qty",
            "width": 60
        },
        {
            "label": _("Purchase Date"),
            "fieldtype": "Date",
            "fieldname": "purchase_date",
            "width": 90
        },
        {
            "label": _("Available For Use Date"),
            "fieldtype": "Date",
            "fieldname": "available_for_use_date",
            "width": 90
        },
        # {
        # 	"label": _("Gross Purchase Amount"),
        # 	"fieldname": "gross_purchase_amount",
        # 	"fieldtype": "Currency",
        # 	"options": "company:currency",
        # 	"width": 100
        # },
        {
            "label": _("Gross Asset Value"),
            "fieldname": "asset_value",
            "fieldtype": "Currency",
            "options": "company:currency",
            "width": 100
        },
        {
            "label": _("Opening Accumulated Depreciation"),
            "fieldname": "opening_accumulated_depreciation",
            "fieldtype": "Currency",
            "options": "company:currency",
            "width": 90
        },
        {
            "label": _("Depreciated Amount"),
            "fieldname": "depreciated_amount",
            "fieldtype": "Currency",
            "options": "company:currency",
            "width": 100
        },
        {
            "label": _("Asset Addition"),
            "fieldtype": "Currency",
            "fieldname": "asset_addition",
            "options": "company:currency",
            "width": 100
        },
        {
            "label": _("Net Asset Value"),
            "fieldname": "net_asset_value",
            "fieldtype": "Currency",
            "options": "company:currency",
            "width": 100
        },
        {
            "label": _("Cost Center"),
            "fieldtype": "Link",
            "fieldname": "cost_center",
            "options": "Cost Center",
            "width": 100
        },
        {
            "label": _("Department"),
            "fieldtype": "Link",
            "fieldname": "department",
            "options": "Department",
            "width": 100
        },
        {
            "label": _("Vendor Name"),
            "fieldtype": "Data",
            "fieldname": "vendor_name",
            "width": 100
        },
        {
            "label": _("Physical Status"),
            "fieldtype": "Data",
            "fieldname": "physical_status",
            "width": 100
        },
        {
            "label": _("Tools Condition"),
            "fieldtype": "Data",
            "fieldname": "tools_condition",
            "width": 100
        },
    ]