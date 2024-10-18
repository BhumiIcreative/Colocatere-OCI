# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"
    
    #Does not call from anywhere
    # def recompute_taxes(self):
    #     for line_id in self.with_context(check_move_validity=False):
    #         line_id.tax_ids = line_id._get_computed_taxes()
    #     for move_id in self.mapped('move_id'):
    #         move_id.write({
    #             'invoice_line_ids': [],
    #         })
    #     return True
