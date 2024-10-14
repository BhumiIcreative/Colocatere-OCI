# -*- coding: utf-8 -*-
from odoo import fields, models


class AccountBankStatementLine(models.Model):
    _inherit = 'account.bank.statement.line'

    ecritures_comptable_ids = fields.One2many("account.move.line", "statement_line_id",
                                              string="Ecritures comptable",copy=False)
