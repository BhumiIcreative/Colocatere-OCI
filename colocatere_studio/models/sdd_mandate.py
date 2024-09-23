# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _


class SDDMandate(models.Model):
    _inherit = 'sdd.mandate'

    bic_1 = fields.Char(string=_("BIC"), readonly=True, related='partner_bank_id.bank_bic', store=False)
    marque_finvest_immo = fields.Boolean("Marque FINVEST IMMO")
