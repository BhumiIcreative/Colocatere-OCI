# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, models, fields, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    invoice_timeline_template_id = fields.Many2one(
        "account.timeline.template",
        compute="_cpt_invoice_timeline_template_id",
        store=True,
    )
    x_studio_marque_finvest_immo = fields.Boolean(
        "x_studio_marque_finvest_immo"
    )
    # FIXME la fonction est également définie dans cet autre module invoice_timeline_CGV/models/sale_invoice.py
    @api.depends("project_id", "project_id.property_ids")
    def _cpt_invoice_timeline_template_id(self):
        account_timeline_obj = self.env["account.timeline.template"]
        for sale_id in self:
            # Assign the existing value of invoice_timeline_template_id or initialize it with account_timeline_obj
            sale_id.invoice_timeline_template_id = (
                sale_id.invoice_timeline_template_id or account_timeline_obj
            )
            # Skip the process if the sale order is fully invoiced
            if sale_id.invoice_status in ["invoiced"]:
                continue
            # Check if the sale order is from company with ID 1
            if sale_id.company_id.id == 1:
                # Calculate the total number of rooms from the project's property records
                room_count = sum(
                    sale_id.project_id.mapped("property_ids").mapped(
                        "room_count"
                    )
                )
                # Define the domain for searching the appropriate timeline template based on room count
                domain = [
                    ("use_on_sale", "=", True),
                    ("room_min", "<=", room_count),
                    "|",
                    ("room_max", ">=", room_count),
                    ("room_max", "<", 0),
                ]
                # If the Finvest flag is set, extend the domain to include Finvest-specific templates
                if sale_id.x_studio_marque_finvest_immo:
                    domain += [("use_on_finvest", "=", True)]
                else:
                    domain += [("use_on_finvest", "=", False)]
                # Ensure there is exactly one matching template, otherwise raise a UserError
                if len(account_timeline_obj.search(domain)) != 1:
                    raise UserError(
                        _(
                            "Aucun ou Plusieurs résultat(s) pour %s chambre(s) et Finvest = %s"
                            % (
                                room_count,
                                sale_id.x_studio_marque_finvest_immo,
                            )
                        )
                    )
                # Assign the found timeline template to the sale or
                invoice_timeline_template_id = account_timeline_obj.search(
                    domain
                )
                if invoice_timeline_template_id:
                    sale_id.invoice_timeline_template_id = (
                        invoice_timeline_template_id
                    )
                # Set the CGV note from the selected timeline template to the sale order
                sale_id.oci_cgv = (
                    sale_id.invoice_timeline_template_id.oci_note_cgv
                )

    """Override the default method to add project_id and purchase_contract_id
        to the invoice's default values"""

    def _create_invoices_from_timeline_default_value(self):
        default_value = super()._create_invoices_from_timeline_default_value()
        return dict(
            default_value,
            project_id=self.project_id.id,
            purchase_contract_id=self.purchase_contract_id.id,
        )
