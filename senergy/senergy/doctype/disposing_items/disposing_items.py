from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class DisposingItems(Document):
    def validate(self):
        if self.workflow_state == "Approved":
            for i in self.items:
                frappe.db.set_value("Serial No",i.serial_number,"disposed",1)
                

@frappe.whitelist()
def update_wfs(name):
    doc = frappe.get_doc("Disposing Items",name)
    if doc.warehouse:
        if "Main" in doc.warehouse:
            frappe.db.set_value("Disposing Items",doc.name,"workflow_state","Approval Pending")