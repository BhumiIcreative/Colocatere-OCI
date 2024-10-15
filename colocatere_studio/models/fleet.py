# -*- coding: utf-8 -*-
from odoo import models, fields

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



class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    fleet_critair = fields.Integer("Vignette Crit'Air")
