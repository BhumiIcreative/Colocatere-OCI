# -*- coding: utf-8 -*-
from odoo import fields, models


class PropertyProperty(models.Model):
    _inherit = 'property.property'

    partner_address_id = fields.Many2one('res.partner', string='Addresse du partenaire')
    marque_finvest_immo = fields.Boolean(string="Marque FINVEST IMMO")
    nom_colocation = fields.Char(string="Nom Colocation")
