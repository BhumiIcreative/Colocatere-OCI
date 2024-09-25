# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import Command, models, fields


class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    fleet_critair = fields.Integer("Vignette Crit'Air")
