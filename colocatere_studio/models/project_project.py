# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, _, api


class Project(models.Model):
    _inherit = 'project.project'

    gestion_particuliere = fields.Boolean('Gestion particulière')
    gestion_particuliere_description = fields.Text("Description")
    marque_finvest_immo = fields.Boolean("Marque FINVEST IMMO")
    property_id = fields.Many2one('property.property', string=_('Property'), compute='_compute_property',
                                  ondelete='set null',readonly=True)
    partner_id = fields.Many2one('res.partner', string=_('Customer'))

    @api.depends('property_ids')
    def _compute_property(self):
        for record in self:
            record['property_id'] = record.property_ids[0] if record.property_ids else False
