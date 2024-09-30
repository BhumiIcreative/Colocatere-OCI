# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class AccountPayment(models.Model):
    _inherit = "account.payment"

    display_error = fields.Boolean(
        string=_("Have to display error message"), default=False
    )
    error_message = fields.Char(string=_("Information message"))
    is_lock_payment = fields.Boolean(
        string=_("For hide validation button"), default=False
    )

    @staticmethod
    def partner_have_payment_access(partner_id):
        """Check the payment access status for a partner"""
        # No message
        if partner_id.parent_id and partner_id.payment_warn == "no-message":
            partner_id = partner_id.parent_id
        error_message, is_lock = False, False
        # Block
        if partner_id.payment_warn == "block":
            error_message = (
                _(
                    "La création/mise à jour du paiement est bloquée pour le partenaire %s"
                )
                % partner_id.name
            )
            is_lock = True
        # Warning
        if partner_id.payment_warn == "warning":
            error_message = partner_id.payment_warn_msg
        return {"error_message": error_message, "is_lock": is_lock}

    @api.onchange("partner_id")
    def _onchange_partner_id_warning(self):
        """Display message on change of partner"""
        if (
            not self.partner_id
            or self.env
            and self.env.context
            and "default_error_message" in self.env.context
        ):
            return
        self.display_error, self.error_message = False, ""
        partner = self.partner_id
        get_error = self.partner_have_payment_access(partner)
        error_msg = get_error.get("error_message")
        if error_msg:
            self.update({"display_error": True, "error_message": error_msg})
        if get_error.get("is_lock"):
            self.partner_id = ""
