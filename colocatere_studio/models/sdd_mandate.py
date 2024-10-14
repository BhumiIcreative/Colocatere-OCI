# -*- coding: utf-8 -*-
from odoo import fields, models


class SDDMandate(models.Model):
    _inherit = 'sdd.mandate'

    bic_1 = fields.Char(string="BIC", readonly=True, related='partner_bank_id.bank_bic', store=False)
    marque_finvest_immo = fields.Boolean("Marque FINVEST IMMO")
