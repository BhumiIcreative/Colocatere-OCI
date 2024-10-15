# -*- coding: utf-8 -*-
from odoo import fields, models


class PartnerCategory(models.Model):
    _inherit = 'res.partner.category'

    is_used_by_akawam = fields.Boolean(string="Used by AKAWAM",copy=False)
