# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, _, fields


class CommissionLine(models.Model):
    _name = "property.commission_line"
    _inherit = "akawam.connector"
    _description = "this is the commission line model for purchase contract"

    @api.model
    def _get_default_currency(self):
        """Return the default currency for account moves"""
        journal = self.env["account.move"]._search_default_journal()
        return journal.currency_id or journal.company_id.currency_id

    price = fields.Monetary(string=_("Price"))
    currency_id = fields.Many2one(
        "res.currency",
        string=_("Currency"),
        readonly=True,
        required=True,
        default=_get_default_currency,
    )
    partner_id = fields.Many2one("res.partner", string=_("Partner"))
    purchase_contract_id = fields.Many2one(
        "property.purchase_contract", string=_("Purchase contract")
    )
