# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, _


class AccountMove(models.Model):
    _inherit = "account.move"

    display_error = fields.Boolean(
        string=_("Have to display error message"), default=False
    )
    error_message = fields.Char(string=_("Information message"))
    is_lock_payment = fields.Boolean(
        string=_("For hide validation button"), default=False
    )

    def action_register_payment(self):
        """It verifies the payment access for partners associated with the records and handles any errors or locks that may arise."""
        context = dict(self.env.context)
        # Ensure the context contains 'active_ids' and 'active_model'
        if not context.get("active_ids") or not context.get("active_model"):
            context.update({"active_model": "account.move", "active_ids": self.ids})

        # Validate and check for errors related to payment access
        error_messages = []
        is_lock_payment = False
        for record in self.env[context.get("active_model")].browse(
            context.get("active_ids")
        ):
            if record.partner_id:
                payment_access_error = self.payment_id.partner_have_payment_access(
                    record.partner_id
                )
                if payment_access_error.get("error_message"):
                    error_messages.append(
                        f"{record.partner_id.name}: {payment_access_error.get('error_message')}"
                    )
                if payment_access_error.get("is_lock"):
                    is_lock_payment = True

        # Update the context with error messages and lock status if any issues exist
        if error_messages:
            context.update(
                {
                    "default_error_message": "\n".join(error_messages),
                    "error_message": True,
                }
            )

        if is_lock_payment:
            context["default_is_lock_payment"] = True

        # Prepare action context for the payment registration form
        action_context = {
            "active_model": "account.move.line",
            "active_ids": self.ids,
            "default_is_lock_payment": context.get("default_is_lock_payment"),
            "default_display_error": context.get("error_message"),
            "default_error_message": context.get("default_error_message"),
        }

        # Return the action to open the payment registration form in a new window
        return {
            "name": _("Register Payment"),
            "res_model": "account.payment.register",
            "view_mode": "form",
            "views": [[False, "form"]],
            "context": action_context,
            "target": "new",
            "type": "ir.actions.act_window",
        }
