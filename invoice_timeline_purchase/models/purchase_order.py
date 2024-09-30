# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import models, fields


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    invoice_timeline_template_id = fields.Many2one(
        "account.timeline.template",
        string="Invoice timeline",
        ondelete="restrict",
        copy=False,
        domain=[
            ("use_on_purchase", "=", True),
        ],
    )

    def _create_invoices_from_timeline_default_value(self):
        """
        Provide default values for creating invoices from the timeline.
        """
        self.ensure_one()
        journal_id = self.env["account.journal"].search(
            [
                ("type", "=", "purchase"),
            ],
            limit=1,
        )
        return {
            "ref": self.partner_ref,
            "invoice_origin": self.name,
            "journal_id": journal_id.id,
        }

    def create_invoices_from_timeline(self):
        """Create invoices from the timeline for each purchase order"""
        for purchase_id in self:
            lines = [
                line_id._get_data_line_invoice_timeline()
                for line_id in purchase_id.order_line
            ]
            default_value = purchase_id._create_invoices_from_timeline_default_value()
            invoice_ids = purchase_id.invoice_timeline_template_id.create_invoices(
                purchase_id.partner_id,
                lines,
                invoice_type="in_invoice",
                **default_value
            )
            purchase_id.invoice_ids = [(4, invoice_id.id) for invoice_id in invoice_ids]
            purchase_id.invoice_timeline_template_id = purchase_id.invoice_ids.mapped(
                "account_timeline_template_id"
            )
