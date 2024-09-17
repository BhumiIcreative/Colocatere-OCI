# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    oci_cgv = fields.Html(string=_("Terms of sales"))
