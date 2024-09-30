# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models


class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"

    def _compute_communication(self):
        """Override to compute the communication string
        with additional references.
        """
        communication = super()._compute_communication()
        additionnal = (
            self.env["account.move"]
            .browse(self._context.get("active_id"))
            .mapped("additional_invoice_payment_ref")
        )
        for wizard in self:
            if wizard.can_edit_wizard:
                batches = wizard._get_batches()
                wizard.communication = wizard._get_batch_communication(batches[0])
                for record in additionnal:
                    if record:
                        wizard.communication += " " + record
            else:
                wizard.communication = False
        return communication
