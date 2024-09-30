# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models


class AccountPayment(models.Model):
    _inherit = "account.payment"

    @api.model
    def default_get(self, default_fields):
        """Override default_get to append additional invoice references to the communication field."""
        rec = super().default_get(default_fields)
        active_ids = self._context.get("active_ids") or self._context.get("active_id")
        active_model = self._context.get("active_model")

        if active_ids and active_model == "account.move":
            invoices = (
                self.env["account.move"]
                .browse(active_ids)
                .filtered(lambda move: move.is_invoice(include_receipts=True))
            )
            if invoices:
                invoice_id = invoices[0]
                if invoice_id.additional_invoice_payment_ref:
                    rec["communication"] = (
                        f"{rec.get('communication', '')} {invoice_id.additional_invoice_payment_ref}"
                    )
        return rec
