# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, _, fields


class PropertyPricing(models.Model):
    _name = "property.pricing"
    _inherit = "akawam.connector"
    _rec_name = "amount"
    _description = "Property Pricing"

    amount = fields.Integer(_("Amount"))
    interval = fields.Integer(_("Interval"))
    interval_type = fields.Selection(
        [
            ("day", _("Day")),
            ("month", _("Month")),
            ("trimester", _("Trimester")),
            ("semester", _("Semester")),
            ("year", _("Year")),
        ],
        string=_("Interval type"),
        required=True,
        default="day",
    )
