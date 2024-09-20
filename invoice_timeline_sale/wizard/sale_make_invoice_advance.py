# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, _
from odoo.fields import *


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = 'sale.advance.payment.inv'

    @api.model
    def _default_invoice_timeline_template_id(self):
        """ Return the invoice timeline template ID of the active sale order. """
        ctx = self._context
        if ctx.get('active_model') == 'sale.order' and ctx.get('active_id', False):
            sale_id = self.env['sale.order'].browse(ctx.get('active_id'))
            return sale_id.invoice_timeline_template_id

    invoice_timeline_template_id = Many2one('account.timeline.template',
        string=_('Invoice timeline'), readonly=True, default=_default_invoice_timeline_template_id)

    def create_invoices(self):
        """  Create invoices using the timeline template and handle context actions """
        ctx = self._context
        sale_ids = self.env['sale.order'].browse(ctx.get('active_ids', []))

        if self.invoice_timeline_template_id:
            for sale_id in sale_ids:
                sale_id._create_invoices_from_timeline()
                sale_id.invoice_timeline_template_id = sale_id.invoice_ids.mapped('account_timeline_template_id')
            if ctx.get('open_invoices'):
                return sale_ids.action_view_invoice()
            return {'type': 'ir.actions.act_window_close'}
        return super().create_invoices()
