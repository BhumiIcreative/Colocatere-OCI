# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, _


class AccountBankStatementLine(models.Model):
    _inherit = 'account.bank.statement.line'

    ecritures_comptable_ids = fields.One2many("account.move.line", "statement_line_id",
                                              string=_("Ecritures comptable"))
