# -*- coding: utf-8 -*-
from odoo import models, fields


class Users(models.Model):
    _inherit = "res.users"

    is_delegation_cgp = fields.Boolean(string="Délégation CGP ?",copy=False)
    adresse_de_bien_ids = fields.One2many('property.property', 'property_id', string='Adresse de bien',copy=False)
