# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, _


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    marque_finvest_immo = fields.Boolean("Marque FINVEST IMMO")
