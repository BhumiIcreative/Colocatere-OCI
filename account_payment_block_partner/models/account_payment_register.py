# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, _


class AccountPaymenRegister(models.TransientModel):
    _inherit = "account.payment.register"

    display_error = fields.Boolean(
        string=_("Have to display error message"), default=False
    )
    error_message = fields.Char(string=_("Information message"))
    is_lock_payment = fields.Boolean(string=_("For hide validation button"))
