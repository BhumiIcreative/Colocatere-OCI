# -*- coding: utf-8 -*-
from odoo import models, fields


class HrEmployeePrivate(models.Model):
    _inherit = "hr.employee"

    partenaire_id = fields.Many2one('res.partner', "Partenaire", copy=False)
