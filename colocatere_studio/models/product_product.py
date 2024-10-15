# -*- coding: utf-8 -*-
from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    is_used_by_akawam = fields.Boolean(string="Used by Akawam")
