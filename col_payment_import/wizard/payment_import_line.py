# coding: utf-8


from odoo import fields, models, _
from odoo.exceptions import UserError
import datetime


class PaymentImportLine(models.TransientModel):
    _name = "payment.import.line"
    _description = "Payment Import line"

    def _get_default_currency(self):
        # get default currency as EUR
        res = self.env["res.currency"].search(
            [
                ("name", "=", "EUR"),
            ]
        )
        return res and res[0] or False

    def _get_partner_id(self, code, company):
        """
        Search for partner which could have  Account code  same as code in any of the accounting entries field
        and company_id similar to the company
        """
        account_code = code
        partner_id = False
        if account_code != "41110000":
            partner_ids = self.env["res.partner"].search(
                [
                    "&",
                    "|",
                    "|",
                    ("property_account_receivable_id.company_id", "=", company.id),
                    ("property_account_payable_id.company_id", "=", company.id),
                    ("property_account_employee_id.company_id", "=", company.id),
                    "|",
                    "|",
                    ("property_account_receivable_id.code", "=", account_code),
                    ("property_account_payable_id.code", "=", account_code),
                    ("property_account_employee_id.code", "=", account_code),
                ]
            )
            if len(partner_ids) > 1:
                raise UserError(
                    _("Have multiple partner with account %s") % (account_code)
                )
            partner_id = partner_ids and partner_ids.id or False
        return partner_id

    account_code = fields.Char(string="Account code")
    credit = fields.Monetary(
        string="Credit",
    )
    date = fields.Date("Date")
    debit = fields.Monetary(string="Debit")
    group = fields.Char("Group")
    libelle = fields.Char(string="Libelle")

    currency_id = fields.Many2one(
        "res.currency", string="Currency", default=_get_default_currency
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=False)
    payment_import_id = fields.Many2one(
        "payment.import",
        string="Payment entry",
        index=True,
        required=True,
        auto_join=True,
        ondelete="cascade",
    )

    def create_line(self, group, values, company):
        try:
            date = datetime.datetime.strptime(values[3], "%d/%m/%Y")
        except Exception as e:
            raise UserError(_("Invalid Data :  %s" % e))
        vals = {
            "date": fields.Date.to_string(date),
            "account_code": values[4],
            "partner_id": self._get_partner_id(values[4], company),
            "libelle": values[5],
            "debit": float(values[7].replace(",", ".")),
            "credit": float(values[9].replace(",", ".")),
            "group": group,
        }
        return vals
