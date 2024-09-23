# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, _


class PartnerCategory(models.Model):
    _inherit = 'res.partner.category'

    is_used_by_akawam = fields.Boolean(string=_("Used by AKAWAM"))
