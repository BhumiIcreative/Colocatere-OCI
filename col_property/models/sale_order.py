# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import api, models, _, fields

log = logging.getLogger(__name__).info


class SaleOrder(models.Model):
    _name = "sale.order"
    _inherit = ["sale.order", "akawam.connector"]

    project_id = fields.Many2one("project.project", string=_("Project"))
    purchase_contract_id = fields.Many2one(
        "property.purchase_contract", string=_("Purchase contract")
    )
    analytic_account_id = fields.Many2one(
        "account.analytic.account",
        compute="_cpt_analytic_account_id",
        store=True,
        readonly=False,
    )

    @api.depends("project_id", "project_id.analytic_account_id")
    def _cpt_analytic_account_id(self):
        """set the analytic account from the project's analytic account."""
        for sale_id in self:
            sale_id.analytic_account_id = sale_id.project_id.analytic_account_id

    def _create_invoices(self, **kwargs):
        """Override create invoices to set project and purchase
        contract on created invoices."""
        move_ids = super()._create_invoices(**kwargs)
        for move_id in move_ids:
            move_id.project_id = self.project_id
            move_id.purchase_contract_id = self.purchase_contract_id
        return move_ids
