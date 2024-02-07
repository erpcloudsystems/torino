# Copyright (c) 2024, ECS and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class CashEntry(Document):
    pass
# Copyright (c) 2022, ERPCloud.Systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt
class CashEntry(Document):
    @frappe.whitelist()
    def validate(self):
        self.total_amount = 0
        for x in self.expense_entry_account:
            self.total_amount += x.amount

    # @frappe.whitelist()
    # def before_submit(self):
    # 	if flt(self.total_amount,2) != flt(self.total_amount,2):
    # 		frappe.throw(" Amount Must Be Equal To Total Amount Of Accounts Table ... Difference is " + str(self.total_amount - self.total_amount))

    @frappe.whitelist()
    def on_submit(self):
        if self.payment_type == "Pay":
            accounts = [
                {
                    "doctype": "Journal Entry Account",
                    "account": self.account_paid_from,
                    "credit": self.total_amount,
                    "debit": 0,
                    "credit_in_account_currency": self.total_amount
                }
            ]

            for x in self.expense_entry_account:
                accounts1 = {
                    "doctype": "Journal Entry Account",
                    "account": x.account,
                    "credit": 0,
                    "debit": x.amount,
                    "debit_in_account_currency": x.amount,
                    "party_type": x.party_type,
                    "party": x.party,
                    "cost_center": x.cost_center,
                    "user_remark": x.user_remark
                },
                accounts.extend(accounts1)

            new_doc = frappe.get_doc({
                "doctype": "Journal Entry",
                "voucher_type": "Journal Entry",
                "reference_doctype": "Cash Entry",
                "reference_link": self.name,
                "cheque_no": self.name,
                "cheque_date": self.posting_date,
                "posting_date": self.posting_date,
                "accounts": accounts,
                "payment_type": self.payment_type,
                "company": self.company,
                "user_remark": self.remarks,
                "multi_currency": self.multi_currency
            })

            new_doc.insert(ignore_permissions=True)
            new_doc.submit()

        if self.payment_type == "Receive":
            accounts = [
                {
                    "doctype": "Journal Entry Account",
                    "account": self.account_paid_to,
                    "credit": 0,
                    "debit": self.total_amount,
                    "debit_in_account_currency": self.total_amount				}
            ]

            for x in self.expense_entry_account:
                accounts1 = {
                                "doctype": "Journal Entry Account",
                                "account": x.account,
                                "credit": x.amount,
                                "debit": 0,
                                "credit_in_account_currency": x.amount,
                                "party_type": x.party_type,
                                "party": x.party,
                                "cost_center": x.cost_center,
                                "vehicle": x.vehicle,
                                "branch": x.branch,
                                "project": x.project,
                                "user_remark": x.user_remark
                            },
                accounts.extend(accounts1)

            new_doc = frappe.get_doc({
                "doctype": "Journal Entry",
                "voucher_type": "Journal Entry",
                "reference_doctype": "Cash Entry",
                "reference_link": self.name,
                "cheque_no": self.name,
                "cheque_date": self.posting_date,
                "posting_date": self.posting_date,
                "accounts": accounts,
                "payment_type": self.payment_type,
                "company": self.company,
                "user_remark": self.remarks,
                "multi_currency": self.multi_currency
            })

            frappe.msgprint(str(new_doc.accounts))
            new_doc.insert(ignore_permissions=True)
            new_doc.submit()