# -*- coding: utf-8 -*-
from odoo import fields, models


class PropertyProperty(models.Model):
    _inherit = 'property.property'

    partner_address_id = fields.Many2one('res.partner', string=_('Addresse du partenaire'))
    marque_finvest_immo = fields.Boolean(string=_("Marque FINVEST IMMO"),copy=False)
    nom_colocation = fields.Char(string=_("Nom Colocation"),copy=False)
    property_id = fields.Many2one('res.users', string='Property')
