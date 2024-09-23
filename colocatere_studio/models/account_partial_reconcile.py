# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, Command


class AccountPartialReconcile(models.Model):
    _inherit = "account.partial.reconcile"

    debit_move_id = fields.Many2one('account.move.line',string=_('Debit Move'))
