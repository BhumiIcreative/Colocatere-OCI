# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models


class AccountTimelineTemplate(models.Model):
    _inherit = "account.timeline.template"

    oci_note_cgv = fields.Html(string="Terms of sales")
