# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# -*- coding: utf-8 -*-

from odoo import fields, models,_


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    reconciliation_date = fields.Date(string=_("Date de Lettrage"), copy=False)
