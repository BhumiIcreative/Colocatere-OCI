# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, _


class Users(models.Model):
    _inherit = "res.users"

    is_delegation_cgp = fields.Boolean(string=_("Délégation CGP ?"))
