# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, models, fields


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    invoice_timeline_template_id = fields.Many2one(
        "account.timeline.template",
        compute="_cpt_invoice_timeline_template_id",
        store=True,
    )

    @api.depends("project_id", "project_id.property_ids")
    def _cpt_invoice_timeline_template_id(self):
        """Get the model for account timeline templates"""
        AccountTimelineTemplate = self.env["account.timeline.template"]
        for purchase_id in self:
            # Ensure the field has a value or get it from the template
            purchase_id.invoice_timeline_template_id = (
                purchase_id.invoice_timeline_template_id or AccountTimelineTemplate
            )
            # Skip if there are existing invoices for the purchase order
            if purchase_id.invoice_ids:
                continue
            # Calculate total room count from linked properties in the project
            room_count = sum(
                purchase_id.project_id.mapped("property_ids").mapped("room_count")
            )
            # Search for the appropriate timeline template based on room count
            invoice_timeline_template_id = AccountTimelineTemplate.search(
                [
                    ("use_on_purchase", "=", True),
                    ("room_min", "<=", room_count),
                    "|",
                    ("room_max", ">=", room_count),
                    ("room_max", "<", 0),
                ],
                limit=1,
            )
            # Assign the template if found
            if invoice_timeline_template_id:
                purchase_id.invoice_timeline_template_id = invoice_timeline_template_id

    """Call the parent function and add extra default values for invoice creation"""

    def _create_invoices_from_timeline_default_value(self):
        default_value = super()._create_invoices_from_timeline_default_value()
        return dict(
            default_value,
            project_id=self.project_id.id,  # Add project_id from the purchase order
            purchase_contract_id=self.purchase_contract_id.id,  # Add project_id from the purchase order
        )
