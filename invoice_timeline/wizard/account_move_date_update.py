# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import models


class AccountMoveReversal(models.TransientModel):
    _inherit = "account.move.reversal"

    def reverse_moves(self, is_modify=False):
        """
        Override: Reverse moves and update timeline sequence
        Returns: dict
        """
        action = super().reverse_moves()
        original_move_ids = (
            self.env["account.move"].browse(self.env.context["active_ids"])
            if self.env.context.get("active_model") == "account.move"
            else self.move_id
        )
        if len(original_move_ids) > 1:
            original_move_ids = original_move_ids[0]
        account_move_ids = action.get("res_id", action.get("domain", [(0, 0, [])]))
        if type(account_move_ids) is not list:
            account_move_ids = [account_move_ids]
        account_move_ids = self.env["account.move"].browse(account_move_ids)
        for account_move_id in account_move_ids:
            account_move_id.timeline_sequence = original_move_ids.timeline_sequence
        return action
