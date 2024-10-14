# -*- coding: utf-8 -*-
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    adresse_de_bien_ids = fields.One2many('property.property', 'partner_address_id', string='Adresse de bien',copy=False)
    is_delegation_cgp = fields.Boolean("Délégation CGP ?",copy=False)
    proprietaire_projet_ids = fields.One2many("project.project","partner_id",string='Proprietaire / Projet',copy=False)
