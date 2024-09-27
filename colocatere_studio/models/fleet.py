# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api


class FleetVehicleLogContract(models.Model):
    _inherit = 'fleet.vehicle.log.contract'

    fleet_contrats_assurance = fields.Float("Assurance")
    fleet_contrats_avantnat = fields.Float("Avantage en nature")
    fleet_contrats_loyerfraisttc = fields.Float("Loyer + frais mensuel TTC")
    fleet_contrats_loyerht = fields.Float("Loyer Mensuel HT")
    fleet_contrats_loyerttc = fields.Float("Loyer TTC")
    fleet_contrats_moiscontr = fields.Float("New Décimal")
    fleet_contrats_serviceht = fields.Float("Service HT")
    fleet_contrats_tva = fields.Float("TVA")