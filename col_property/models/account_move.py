# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from datetime import datetime, timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

log = logging.getLogger(__name__).info


class AccountMove(models.Model):
    _name = "account.move"
    _inherit = ["account.move", "akawam.connector"]

    state = fields.Selection(
        [
            ("draft", _("Draft")),
            ("to_post", _("To post")),
            ("posted", _("Posted")),
            ("cancel", _("Cancel")),
        ]
    )
    in_deficit = fields.Boolean(
        string=_("Is in deficit"), related="project_id.in_deficit", store=True
    )
    additional_invoice_payment_ref = fields.Char(
        string=_("Additional invoice payment ref")
    )
    purchase_contract_id = fields.Many2one(
        "property.purchase_contract", string=_("Purchase contract")
    )
    lease_id = fields.Many2one("property.lease", string=_("Lease"))
    lease_partner_ids = fields.Many2many(
        "res.partner",
        string=_("Lessors"),
        compute="_cpt_lease_partner_ids",
        store=True,
        readonly=True,
    )

    @api.depends("lease_id", "lease_id.lessor_partner_ids")
    def _cpt_lease_partner_ids(self):
        """Compute and set lease partner IDs based on the associated lease."""
        for move_id in self:
            move_id.lease_partner_ids = [(5)]
            lease_id = move_id.lease_id
            if lease_id:
                partner_ids = lease_id.lessor_partner_ids
                if partner_ids:
                    move_id.lease_partner_ids = [(6, 0, partner_ids.ids)]

    def action_to_post(self):
        """Change the invoice state to 'to_post' if it's in draft state."""
        for move_id in self:
            if move_id.state != "draft":
                raise UserError(
                    _(
                        "You can't mark an invoice as to post if it's not in draft state."
                    )
                )
            move_id.state = "to_post"

    def get_last_day_of_next_month(self):
        script = self.env["script.tools"]
        next_month = datetime.now().replace(day=1) + timedelta(days=32)
        next_stop = script.get_nex_month_stop(next_month)["stop"]
        return next_stop

    def action_switch_invoice_into_refund_credit_note(self):
        if any(move.type not in ("in_invoice", "out_invoice") for move in self):
            raise ValidationError(_("This action isn't available for this document."))

    def cron_auto_invoice_repayment(self, date=""):
        """
        Automatically process and post invoices based
        on due dates within the current month.
        """
        script = self.env["script.tools"]
        date = date or fields.Date.today()
        month_range = script.get_date_month_start_stop(date)

        move_ids = self.search(
            [
                ("state", "not in", ["posted", "cancel"]),
                ("journal_id.name", "=", "Reversement"),
                ("invoice_date_due", ">=", month_range["start"]),
                ("invoice_date_due", "<=", month_range["stop"]),
                ("line_ids", "!=", False),
            ]
        )

        try:
            negative_move_ids = move_ids.filtered(
                lambda x: x.amount_total < 0 and "refund" not in x.type
            )
            if negative_move_ids:
                negative_move_ids.action_switch_invoice_into_refund_credit_note()

            for move_id in move_ids:
                if move_id.state == "draft":
                    move_id.action_to_post()
                elif move_id.state == "to_post":
                    move_id.action_post()

        except Exception as e:
            log("cron_auto_invoice_repayment failed: %s", repr(e))
            mail_template_id = self.env.ref("col_property.mail_template_exception")
            mail_template_id.send_mail(self.env.user.id)

        return True

    # defined in module account_auto_match_journal_invoice_voucher (remain to migrate)
    # def _can_be_auto_matched_with(self, move_line_id):
    #     res = super()._can_be_auto_matched_with(move_line_id)
    #     res = res and self.project_id == move_line_id.move_id.project_id
    #     res = res and self.project_id
    #     return res
