# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def link_to_account_move_line(self, move_line_values):
        """Add sale order line ID to the provided move line values.
        :rtype: dict
        """
        self.ensure_one()
        move_line_values["sale_line_ids"] = [(4, self.id)]
        return move_line_values

    def _get_data_line_invoice_timeline(self):
        """Prepare data from the purchase order line to be used in invoice timeline.
        :rtype: dict
        """
        self.ensure_one()
        return {
            "line_id": self,
            "product_id": self.product_id,
            "tax_ids": self.tax_id,
            "price_unit": self.price_unit,
            "quantity": self.product_uom_qty,
            "name": self.name,
            "account_analytic_id": self.order_id.analytic_account_id,
        }
