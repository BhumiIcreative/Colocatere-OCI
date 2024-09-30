# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, _


class ResPartner(models.Model):
    _name = "res.partner"
    _inherit = ["res.partner", "akawam.connector"]

    purchase_contract_ids = fields.Many2many(
        "property.purchase_contract",
        "rel_purchase_owner",
        string=_("Purchase contracts"),
    )
