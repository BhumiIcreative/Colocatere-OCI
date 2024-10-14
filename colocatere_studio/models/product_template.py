# -*- coding: utf-8 -*-
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_used_by_akawam = fields.Boolean("Used by Akawam",copy=False)
