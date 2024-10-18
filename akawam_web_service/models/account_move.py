# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, models
from odoo.fields import Date

# Import constants from another module
from .variable_en_dur_degueulasse import COMPANY, JOURNAUX, PAYMENT_TYPE

import json
import logging

# Log information to help with debugging
log = logging.getLogger().info


class AccountMove(models.Model):
    _inherit = "account.move"

    def get_akawam_lines(self):
        """Function to get Akawam-specific line items for invoices"""
        lines = []
        for line_id in self.invoice_line_ids:
            lines.append(
                {
                    "text": line_id.name,
                    "price": line_id.price_subtotal,
                }
            )
        return lines

    def _timeline_sync_to_akawam(self):
        """Sync function for invoice data related to a timeline (specific to certain contracts)"""
        log("---------- _timeline_sync_to_akawam invoice")
        # Pour les entrée journal achat/vente de travaux lié à un contrat d'achat dans la SAS
        # run if """ is_standard_invoice and self.purchase_contract_id and self.company_id.id == COMPANY.get('SAS_GROUPE_COLOCATERE') """
        route = "/api/v1/model/fund-call"
        lines = self.get_akawam_lines()
        # Determine the state based on the current invoice state
        state = {
            "draft": 1,
            "to_post": 1,
            "posted": 2,
        }.get(self.state, -1)
        # If part of the invoice has been paid, update state
        if self.amount_total - self.amount_residual:
            state = 4
        # Determine invoice type (0 for sales, 1 for purchases)
        type = 0 if self.move_type == "out_invoice" else 1
        # Prepare data to be sent to Akawam
        datas = {
            "date": Date.to_string(self.date),
            "odoo_id": self.id,
            "odoo_invoice": self.name,
            "status": state,
            "price": self.amount_total,
            "lines": lines,
            "type": type,
            "dues_remaining": self.amount_residual,
            "purchase_contract_id": self.purchase_contract_id.akawam_id,
            "sequence": self.timeline_sequence,
        }
        # If there is no amount remaining, the invoice is fully paid
        if not self.amount_residual:
            datas["status"] = 3
            payment_info = json.loads(self.invoice_payments_widget)
            if payment_info:
                payments = payment_info.get("content", [])
                if payments:
                    # Add payment date if available
                    datas["payment_date"] = payments[-1].get("date", False)
        # Call Akawam web service to sync data
        self.env["akawam.ws.call"].call(route, self, datas)

        return True

    def _invoice_sync_to_akawam(self):
        """Sync function for standard invoices to Akawam"""
        log("---------- _invoice_sync_to_akawam invoice")
        route = "/api/v1/model/invoice"
        # Determine invoice state based on its status
        state = {
            "draft": 0,
            "to_post": 1,
            "posted": 2,
        }.get(self.state, -1)
        if not self.amount_residual:
            state = 3  # Mark as fully paid if no residual amount
        # Prepare data to be sent to Akawam
        datas = {
            "odoo_id": self.id,
            "reference": self.name,
            "description": self.name,
            "date": Date.to_string(self.date),
            "taxes_amount": self.amount_tax,
            "price": self.amount_untaxed,
            "price_with_taxes": self.amount_total,
            "status": state,
        }
        # Call Akawam web service to sync the invoice
        self.env["akawam.ws.call"].call(route, self, datas)

        return True

    def _location_sync_to_akawam(self):
        """Sync function for invoices related to property locations (specific journals and company)"""
        log("---------- _location_sync_to_akawam invoice")
        # si facture de quittance et reversement
        # run if """ if is_location_journal and self.company_id.id == COMPANY.get('SARL_COLOCATERE'): """
        route = "/api/v1/model/period"
        states = {
            "draft": 0,
            "to_post": 0,
            "posted": 1,
            "paid": 3,
            "in_payment": 4,
            "cancel": -1,
        }
        datas = {
            "status": states[self.state],
        }
        # Handle payment statuses differently
        if self.payment_state in ("in_payment", "paid"):
            datas = {
                "status": states[self.payment_state],
            }
        # If the invoice is a rental payment, change the API route and sync status
        if (
            self.lease_id
            and self.move_type in ("out_invoice", "out_refund")
            and self.journal_id.id == JOURNAUX.get("QUITTANCE")
        ):
            route = "/api/v1/model/financial-report"
            states = {
                "draft": 0,
                "to_post": 0,
                "posted": 1,
                "cancel": 1,
            }
            datas = {
                "status": states[self.state],
            }
        # Call Akawam web service to sync
        self.env["akawam.ws.call"].call(route, self, datas)
        return True

    def _maintenance_sync_to_akawam(self):
        """Sync function for maintenance-related invoices (special handling for SARL)"""
        log("---------- _maintenance_sync_to_akawam invoice")
        route = "/api/v1/model/invoicemaintenance"
        states = {
            "draft": 0,
            "to_post": 0,
            "posted": 1,
            "paid": 3,
            "in_payment": 4,
            "cancel": -1,
        }
        # Prepare data for syncing
        datas = {
            "status": states[self.state],
        }
        # Handle payment statuses differently
        if self.payment_state in ("in_payment", "paid"):
            datas = {
                "status": states[self.payment_state],
            }
        # Call Akawam web service to sync maintenance invoices
        self.env["akawam.ws.call"].call(route, self, datas)
        return True

    def sync_reversed_entry_to_akawam(self):
        """Sync function for reversed invoices"""
        log("---------- _location_sync_to_akawam invoice")
        # run if "extourne/avoir de facture déjà synchro" pour envoyé comme s'il s'agissait d'un paiement de la facture
        # if is_standard_invoice and self.purchase_contract_id and self.company_id.id == COMPANY.get('SAS_GROUPE_COLOCATERE'):
        # elif is_location_journal and self.company_id.id == COMPANY.get('SARL_COLOCATERE'):
        # else ...
        # Return early if no reversed entry exists
        if not self.reversed_entry_id:
            return True
        # Find the original invoice (if there are multiple reversals)
        reversed_entry_id = self.reversed_entry_id
        while reversed_entry_id.reversed_entry_id:
            reversed_entry_id = reversed_entry_id.reversed_entry_id
        # Search for the initial payment linked to the reversed invoice
        initial_payment_id = self.env["account.payment"]
        for move_line_id in reversed_entry_id.line_ids:
            initial_payment_id = initial_payment_id.search(
                [
                    ("move_line_ids", "in", move_line_id.ids),
                ]
            )
            if initial_payment_id:
                break
        # Return if no linked payment or Akawam route found
        if not initial_payment_id or not initial_payment_id.akawam_route:
            return True
        # Use the initial Akawam route for the sync
        route = initial_payment_id.akawam_route
        invoice_ids = initial_payment_id.history_invoice_ids
        invoice_ids.filtered(lambda x: x.akawam_id)
        if not invoice_ids:
            return True
        # Prepare data for the sync based on the original payment details
        invoice_id = invoice_ids[0]
        datas = {
            "odoo_id": self.id,
            "odoo_model": self._name,
            "payment": self.amount_total,
            "type": PAYMENT_TYPE[initial_payment_id.payment_method_id.code],
            "date": Date.to_string(self.date),
            "comment": "",
        }
        # Handle tenant or owner payments differently
        if route == "/api/v1/model/tenant-payment":
            datas["debit"] = (
                1 if not initial_payment_id.payment_type == "outbound" else 0
            )
            datas["origin"] = ""
            datas["rental_id"] = invoice_id.lease_id.akawam_id
        elif route == "/api/v1/model/owner-payment":
            datas["category"] = 0
            datas["owner_id"] = invoice_id.partner_id.akawam_id
            datas["period_id"] = invoice_id.akawam_id
        # Call Akawam web service to sync the reversed entry
        self.env["akawam.ws.call"].call(route, self, datas)
        return True

    def sync_to_akawam(self):
        # Main sync function for different types of invoices
        log("---------- sync_to_akawam invoice")
        # Determine the type of journal (location, standard, or maintenance)
        is_location_journal = self.journal_id.id in (
            JOURNAUX.get("REVERSEMENT"),
            JOURNAUX.get("QUITTANCE"),
        )
        is_standard_invoice = self.journal_id.id in (
            JOURNAUX.get("FACTURES_CLIENTS"),
            JOURNAUX.get("FACTURES_FOURNISSEURS"),
        )
        is_maintenance_invoice = self.journal_id.id in (
            JOURNAUX.get("FACTURES_CLIENTS_SARL"),
        ) and self.company_id.id == COMPANY.get("SARL_COLOCATERE")
        # Sync based on the type of invoice and company
        if (
            is_standard_invoice
            and self.purchase_contract_id
            and self.company_id.id == COMPANY.get("SAS_GROUPE_COLOCATERE")
        ):
            self._timeline_sync_to_akawam()
        elif is_location_journal and self.company_id.id == COMPANY.get(
            "SARL_COLOCATERE"
        ):
            self._location_sync_to_akawam()
        elif is_maintenance_invoice:
            self._maintenance_sync_to_akawam()
        else:
            self.sync_reversed_entry_to_akawam()
        return True

    def write(self, vals):
        """Override the write function to trigger sync upon updates"""
        log("---------- write invoice")
        res = super().write(vals)
        # Sync to Akawam if the project is linked to Akawam
        for move_id in self:
            if move_id.project_id.akawam_id:
                move_id.sync_to_akawam()
        return res

    @api.model_create_multi
    def create(self, vals_list):
        """Override the create function to trigger sync upon creation"""
        move_ids = super().create(vals_list)
        # Sync to Akawam if the project is linked to Akawam
        for move_id in move_ids:
            if move_id.project_id.akawam_id:
                move_id.sync_to_akawam()
        return move_ids
