# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import api, models, fields

log = logging.getLogger(__name__).info


class PurchaseOrderLine(models.Model):
    _name = "purchase.order.line"
    _inherit = ["purchase.order.line", "akawam.connector"]

    account_analytic_id = fields.Many2one(
        "account.analytic.account",
        compute="_cpt_account_analytic_id",
        store=True,
        readonly=False,
    )

    @api.depends(
        "order_id", "order_id.project_id", "order_id.project_id.analytic_account_id"
    )
    def _cpt_account_analytic_id(self):
        """Compute and set the analytic account based on the project's analytic account."""
        for line_id in self:
            line_id.account_analytic_id = (
                line_id.order_id.project_id.analytic_account_id
            )
