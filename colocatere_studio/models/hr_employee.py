# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields


class HrEmployeePrivate(models.Model):
    _inherit = "hr.employee"

    partenaire_id = fields.Many2one('res.partner', "Partenaire", ondelete="set null")
