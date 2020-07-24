# -*- coding: utf-8 -*-
# Copyright (c) 2020, TeamPRO and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class FreezingRequest(Document):
	def on_submit(self):
		frappe.db.set_value("Item",self.item,"disabled",1)

