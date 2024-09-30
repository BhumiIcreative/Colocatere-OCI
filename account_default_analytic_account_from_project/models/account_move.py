# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _


class AccountMove(models.Model):
    _inherit = "account.move"

    analytic_account_id = fields.Many2one(
        "account.analytic.account",
        string=_("Analytic account"),
        compute="_cpt_analytic_account_id",
        store=True,
        readonly=False,
    )

    @api.depends("project_id")
    def _cpt_analytic_account_id(self):
        """Compute the analytic account based on the associated project"""
        for move_id in self:
            if move_id.project_id and move_id.project_id.analytic_account_id:
                move_id.analytic_account_id = (
                    move_id.project_id.analytic_account_id
                )
