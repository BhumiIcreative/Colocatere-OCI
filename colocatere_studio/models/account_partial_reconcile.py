# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, _


class AccountPartialReconcile(models.Model):
    _inherit = "account.partial.reconcile"

    debit_move_id = fields.Many2one('account.move.line', string=_('Debit Move'))
