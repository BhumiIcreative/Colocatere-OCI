# -*- coding: utf-8 -*-
from odoo import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    marque_finvest_immo = fields.Binary("Marque FINVEST IMMO", copy=False)
    seal = fields.Binary("Cachet de la société", copy=False)
