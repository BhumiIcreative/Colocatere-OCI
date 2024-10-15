# -*- coding: utf-8 -*-
from odoo import models, fields


class FleetVehicleLogContract(models.Model):
    _inherit = 'fleet.vehicle.log.contract'

    oci_fleet_contrats_assurance = fields.Float("Assurance", copy=False)
    oci_fleet_contrats_avantnat = fields.Float("Avantage en nature", copy=False)
    oci_fleet_contrats_loyerfraisttc = fields.Float("Loyer + frais mensuel TTC", copy=False)
    oci_fleet_contrats_loyerht = fields.Float("Loyer Mensuel HT", copy=False)
    oci_fleet_contrats_loyerttc = fields.Float("Loyer TTC", copy=False)
    oci_fleet_contrats_moiscontr = fields.Float("New Décimal", copy=False)
    oci_fleet_contrats_serviceht = fields.Float("Service HT", copy=False)
    oci_fleet_contrats_tva = fields.Float("TVA", copy=False)


class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    oci_fleet_critair = fields.Integer("Vignette Crit'Air", copy=False)
