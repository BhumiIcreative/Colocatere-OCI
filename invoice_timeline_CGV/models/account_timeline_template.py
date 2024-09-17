# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, _


class AccountTimelineTemplate(models.Model):
    _inherit = "account.timeline.template"

    oci_note_cgv = fields.Html(string=_("Terms of sales"))
