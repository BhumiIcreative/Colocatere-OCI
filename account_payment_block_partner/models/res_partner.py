# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, _
from odoo.addons.base.models.res_partner import (
    WARNING_MESSAGE,
    WARNING_HELP,
)


class ResPartner(models.Model):
    _inherit = "res.partner"

    payment_warn = fields.Selection(
        WARNING_MESSAGE, string=_("Payment"), help=WARNING_HELP, default="no-message"
    )
    payment_warn_msg = fields.Text(_("Message for Invoice"))
