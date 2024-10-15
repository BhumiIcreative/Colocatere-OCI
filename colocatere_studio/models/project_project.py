# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Project(models.Model):
    _inherit = 'project.project'

    gestion_particuliere = fields.Boolean('Gestion particulière', copy=False)
    gestion_particuliere_description = fields.Text("Description", copy=False)
    marque_finvest_immo = fields.Boolean("Marque FINVEST IMMO", copy=False)
    property_id = fields.Many2one('property.property', string='Property', compute='_compute_property',
                                  ondelete='set null', readonly=True, copy=False)
    partner_id = fields.Many2one('res.partner', string='Customer')

    @api.depends('property_ids')
    def _compute_property(self):
        for record in self:
            record['property_id'] = record.property_ids[0] if record.property_ids else False
