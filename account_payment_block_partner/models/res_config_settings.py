# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    group_warning_payment = fields.Boolean(
        string=_("Payment alert"),
        implied_group="account_payment_block_partner.group_warning_payment",
    )
