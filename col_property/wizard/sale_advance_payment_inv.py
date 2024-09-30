# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models


class SaleAdvancePaymentInv(models.TransientModel):
    """
    Inherit sale Advance Payment Inv
    """

    _inherit = "sale.advance.payment.inv"

    def _prepare_invoice_values(self, order, so_lines):
        """Prepare invoice values including project
        and purchase contract information.
        """
        invoice_vals = super()._prepare_invoice_values(order, so_lines)
        invoice_vals.update(
            {
                "project_id": order.project_id.id,
                "purchase_contract_id": order.purchase_contract_id.id,
            }
        )
        return invoice_vals
