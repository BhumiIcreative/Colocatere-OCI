# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models


class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"

    is_group_by_project = fields.Boolean()

    def _get_line_batch_key(self, line):
        move = line.move_id
        partner_bank_account = self.env["res.partner.bank"]
        if move.is_invoice(include_receipts=True):
            partner_bank_account = move.partner_bank_id._origin
            if self.is_group_by_project:
                return {
                    "partner_id": line.partner_id.id,
                    "project_id": move.project_id.id,
                    "account_id": line.account_id.id,
                    "currency_id": line.currency_id.id,
                    "partner_bank_id": partner_bank_account.id,
                    "partner_type": "customer"
                    if line.account_type == "asset_receivable"
                    else "supplier",
                }
            return super(AccountPaymentRegister, self)._get_line_batch_key(
                line)
