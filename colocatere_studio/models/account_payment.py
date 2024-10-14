# -*- coding: utf-8 -*-
from odoo import fields, models


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    marque_finvest_immo = fields.Boolean("Marque FINVEST IMMO")
