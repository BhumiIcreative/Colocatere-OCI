# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class AccountFullReconcile(models.Model):
    _inherit = "account.full.reconcile"

    latest_reconciliation_date = fields.Date(
        string=_("Latest Reconciliation Date"), compute="_compute_date", store=True
    )

    @api.depends("reconciled_line_ids", "reconciled_line_ids.date")
    def _compute_date(self):
        for record in self:
            # Compute the max date efficiently
            latest_date = max(
                (line.date for line in record.reconciled_line_ids if line.date),
                default=False,
            )
            record.latest_reconciliation_date = latest_date
            # Update reconciliation_date for the related move lines
            if latest_date:
                record.reconciled_line_ids.filtered(
                    lambda l: l.reconciliation_date != latest_date
                ).write({"reconciliation_date": latest_date})
