# coding: utf-8

from odoo import models, _, fields


class AccountTimelineTemplate(models.Model):
    _inherit = "account.timeline.template"

    room_min = fields.Integer(
        string="Room minimum",
        help=_("Minimum room for this template (negative for no minimum limit)"),
        default=-1,
    )
    room_max = fields.Integer(
        string="Room maximum",
        help=_("Maximum room for this template (negative for no maximum limit)"),
        default=-1,
    )
