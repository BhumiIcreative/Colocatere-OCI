# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = "sale.order"

    invoice_timeline_template_id = fields.Many2one(
        "account.timeline.template",
        string="Invoice timeline",
        ondelete="restrict",
        readonly=True,
        copy=False,
        domain=[
            ("use_on_sale", "=", True),
        ],
    )

    def _create_invoices_from_timeline_default_value(self):
        """Provide default values for creating invoices from the timeline."""
        self.ensure_one()
        journal_id = self.env["account.journal"].search(
            [
                ("type", "=", "sale"),
            ],
            limit=1,
        )
        return {
            "ref": self.client_order_ref,
            "invoice_origin": self.name,
            "journal_id": journal_id.id,
        }

    def _create_invoices_from_timeline(self):
        """Create invoices from the timeline for each sale order"""
        for sale_id in self:
            lines = [
                line_id._get_data_line_invoice_timeline()
                for line_id in sale_id.order_line
            ]
            default_value = sale_id._create_invoices_from_timeline_default_value()
            invoice_ids = sale_id.invoice_timeline_template_id.create_invoices(
                sale_id.partner_id, lines, **default_value
            )
            sale_id.invoice_ids = [(4, invoice_id.id) for invoice_id in invoice_ids]
