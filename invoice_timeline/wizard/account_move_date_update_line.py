# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, models, _, fields


class AccountMoveDateUpdateLine(models.TransientModel):
    _name = "account.move.date.update.line"
    _description = _("Account move date update wizard line")
    _order = "invoice_date_due"

    @api.depends("invoice_id", "invoice_id.state")
    def _cpt_writable(self):
        """
        Compute `writable` based on the state of the related invoice.
        """
        for line_id in self:
            line_id.writable = line_id.invoice_id.state in ("draft", "to_post")

    invoice_date_due = fields.Date(
        string="Current invoice date due",
        related="invoice_id.invoice_date_due",
        store=True,
    )
    new_invoice_date_due = fields.Date(string="New invoice date due", required=True)
    writable = fields.Boolean(string="Writable", compute="_cpt_writable")
    invoice_id = fields.Many2one(
        "account.move", string="Invoice", required=True, readonly=True
    )
    wizard_id = fields.Many2one("account.move.date.update", string="Wizard")

    def compute_date(self):
        """
        Compute the date using the wizard and open the wizard view.
        """
        self.wizard_id._compute_date(self)
        return self.wizard_id.open_wizard()
