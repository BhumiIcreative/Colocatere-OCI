# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class AccountMove(models.Model):
    _inherit = "sale.order"

    oci_cgv = fields.Html("Terms of sales")
