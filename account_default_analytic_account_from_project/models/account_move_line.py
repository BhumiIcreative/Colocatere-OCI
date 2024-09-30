# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    analytic_account_id = fields.Many2one(
        "account.analytic.account",
        string=_("Analytic account"),
        index=True,
        compute="_cpt_analytic_account_id",
        store=True,
        readonly=False,
    )

    @api.depends("move_id", "move_id.analytic_account_id")
    def _cpt_analytic_account_id(self):
        """Compute the analytic account for the move line based on the related account move"""
        for line_id in self:
            line_id.analytic_account_id = line_id.move_id.analytic_account_id

    @api.onchange("product_id", "account_id")
    def _onchange_recompute_analytic(self):
        """Recompute the analytic account when the product or account changes"""
        self._cpt_analytic_account_id()
