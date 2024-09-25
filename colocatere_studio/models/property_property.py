# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, _


class PropertyProperty(models.Model):
    _inherit = 'property.property'

    partner_address_id = fields.Many2one('res.partner', string=_('Addresse du partenaire'))
    marque_finvest_immo = fields.Boolean(string=_("Marque FINVEST IMMO"))
    nom_colocation = fields.Char(string=_("Nom Colocation"))
