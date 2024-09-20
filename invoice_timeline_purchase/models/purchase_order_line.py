# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, _
from odoo.fields import *


class PurchaseOrderLine(models.Model):
    """
    Inherited: Purchase Order Line
    """
    _inherit = 'purchase.order.line'

    def link_to_account_move_line(self, move_line_values):
        """
        Add purchase order line ID to the provided move line values.
        :rtype: dict
        """
        self.ensure_one()
        move_line_values['purchase_line_id'] = self.id
        return move_line_values

    def _get_data_line_invoice_timeline(self):
        """
        Prepare data from the purchase order line to be used in invoice timeline.
        :rtype: dict
        """
        self.ensure_one()
        return {
            'line_id': self,
            'product_id': self.product_id,
            'tax_ids': self.taxes_id,
            'price_unit': self.price_unit,
            'quantity': self.product_qty,
            'name': self.name,
        }

