# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _


class AccountPayment(models.Model):
    _inherit = "account.payment"

    use_employee_account = fields.Boolean(
        string=_("Use employee account"), readonly=False, default=False
    )

    @api.depends_context("use_employee_account")  # add field on base depend
    @api.depends(
        "journal_id",
        "partner_id",
        "partner_type",
        "use_employee_account",
        "is_internal_transfer",
        "destination_journal_id",
    )
    def _compute_destination_account_id(self):
        super()._compute_destination_account_id()  # Call the parent method
        for payment_id in self:
            if payment_id.use_employee_account:
                # Check if employee account should be used so set employee account as destination
                payment_id.destination_account_id = payment_id.partner_id.with_context(
                    force_company=payment_id.company_id.id
                ).property_account_employee_id
