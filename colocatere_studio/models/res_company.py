# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    marque_finvest_immo = fields.Binary("Marque FINVEST IMMO")
    seal = fields.Binary("Cachet de la société")



