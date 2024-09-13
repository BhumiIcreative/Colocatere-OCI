# coding: utf-8
from odoo import fields, models, _


class ExpenseReportImportLine(models.TransientModel):
    _name = "expense_report_import_line"
    _description = "Import expense report line"

    def _get_default_currency(self):
        res = self.env["res.currency"].search(
            [
                ("name", "=", "EUR"),
            ]
        )
        return res and res[0] or False

    date = fields.Date(_("Date"))
    account_code = fields.Char(_("Account"), size=64)
    move_ref = fields.Char(_("Reference"))
    label = fields.Char(_("Label"))
    debit = fields.Monetary(_("Debit"))
    credit = fields.Monetary(_("Credit"))
    analytic_account_id = fields.Integer(_("Analytic account"))

    currency_id = fields.Many2one(
        "res.currency", string=_("Currency"), default=_get_default_currency
    )
    partner_id = fields.Many2one("res.partner", string=_("Partner"))
    expense_report_import_id = fields.Many2one(
        "expense_report_import",
        string=_("Export report import"),
        index=True,
        required=True,
        auto_join=True,
        ondelete="cascade",
    )
