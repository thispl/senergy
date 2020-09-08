# -*- coding: utf-8 -*-
# Copyright (c) 2020, TeamPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class DisablingItems(Document):
	def validate(self):
		if self.workflow_state == "Approved":
			frappe.db.set_value("Serial No",self.serial_number,"disabled",1)

@frappe.whitelist()
def update_wfs(name):
	doc = frappe.get_doc("Disabling Items",name)
	if doc.warehouse:
		if "Main" in doc.warehouse:
			frappe.db.set_value("Disabling Items",doc.name,"workflow_state","Approval Pending")