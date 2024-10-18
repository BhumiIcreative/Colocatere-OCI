# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _
from odoo.fields import Date

from .variable_en_dur_degueulasse import COMPANY, JOURNAUX, PAYMENT_TYPE


class AccountPayment(models.Model):
    _name = "account.payment"
    _inherit = ["account.payment", "akawam.connector"]

    akawam_route = fields.Char("Akawam route")
    history_invoice_count = fields.Integer(
        string=_("History invoice count"),
        compute="_cpt_history_invoice_ids",
        store=True,
    )

    history_invoice_ids = fields.Many2many(
        "account.move",
        relation="rel_payment_invoice_history",
        compute="_cpt_history_invoice_ids",
        store=True,
        string=_("Invoice history"),
        help="Store every related invoice, even no longer reconcilied.",
    )

    @api.depends("reconciled_invoice_ids")
    def _cpt_history_invoice_ids(self):
        """Compute function to update history_invoice_ids and count, based on reconciled invoices"""
        for payment_id in self:
            # Get the current reconciled invoices
            current_invoice_ids = payment_id.reconciled_invoice_ids
            # Update the history with the current invoices
            payment_id.history_invoice_ids = [
                (4, invoice_id.id) for invoice_id in current_invoice_ids
            ]
            # Update the count of the history invoices
            payment_id.history_invoice_count = len(
                payment_id.history_invoice_ids
            )

    # Action to open the history of invoices
    def action_open_history_invoice_ids(self):
        return self.env["script.tools"].open_records(self.history_invoice_ids)

    def _tenant_sync_to_akawam(self):
        """Function to sync tenant payments to the Akawam system"""
        route = "/api/v1/model/tenant-payment"
        # Prepare the data to send to the Akawam system
        datas = {
            "odoo_id": self.id,
            "odoo_model": self._name,
            "payment": self.amount,
            "debit": 1 if self.payment_type == "outbound" else 0,
            "type": PAYMENT_TYPE[self.payment_method_id.code],
            "origin": "",
            "date": Date.to_string(self.date),
            "comment": "",
        }
        # Check if there are any reconciled invoices to sync rental ID
        invoice_ids = self.reconciled_invoice_ids
        if invoice_ids:
            # Add rental ID from the first reconciled invoice
            datas["rental_id"] = invoice_ids[0].lease_id.akawam_id
        # Call the Akawam web service
        self.env["akawam.ws.call"].call(route, self, datas)
        # Update the Akawam route field
        self.akawam_route = route
        return True

    def sync_to_akawam(self):
        """Main function to sync payments to Akawam based on the type of payment"""
        # Don't sync if payment is still in draft state
        if self.state == "draft":
            return False
        payment_type = False
        is_sarl = self.company_id.id == COMPANY.get("SARL_COLOCATERE")
        # Determine payment type based on related invoices
        for invoice_id in self.reconciled_invoice_ids:
            if (
                invoice_id.move_type
                in (
                    "out_invoice",
                    "out_refund",
                )
                and invoice_id.journal_id.id == JOURNAUX.get("QUITTANCE")
            ):
                payment_type = "tenant"
                break
            if (
                invoice_id.move_type
                in (
                    "in_invoice",
                    "in_refund",
                )
                and invoice_id.journal_id.id == JOURNAUX.get("REVERSEMENT")
            ):
                payment_type = "owner"
        # Sync tenant payments to Akawam if conditions are met
        if self.akawam_route == "/api/v1/model/tenant-payment" or (
            is_sarl and payment_type == "tenant"
        ):
            self._tenant_sync_to_akawam()
        # Sync each related invoice to Akawam
        for invoice_id in self.reconciled_invoice_ids:
            invoice_id.sync_to_akawam()
        return True

    def write(self, vals):
        """Override write to ensure Akawam sync after modifications"""
        res = super().write(vals)
        # If the Akawam route is not manually modified, trigger the sync
        if "akawam_route" not in vals:
            for payment_id in self:
                payment_id.sync_to_akawam()
        return res

    @api.model
    def create(self, vals):
        """Override create to sync newly created payments to Akawam"""
        payment_id = super().create(vals)
        payment_id.sync_to_akawam()
        return payment_id

    def action_post(self):
        """Override action_post to sync payments and their reconciled invoices to Akawam when posted"""
        res = super().action_post()
        for payment_id in self:
            payment_id.sync_to_akawam()
            # Sync each reconciled invoice to Akawam
            for invoice_id in payment_id.reconciled_invoice_ids:
                invoice_id.sync_to_akawam()
        return res
