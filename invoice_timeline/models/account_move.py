# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, _,fields


class AccountMove(models.Model):
    """
     Inherited: Account Move
    """
    _inherit = 'account.move'

    timeline_sequence = fields.Integer(_('Timeline sequence'), compute='_cpt_timeline_sequence', store=True)

    account_timeline_template_id = fields.Many2one('account.timeline.template', string=_('Timeline'), readonly=True, ondelete='restrict',  copy=False)

    @api.depends('invoice_date_due', 'account_timeline_template_id', 'account_timeline_template_id.invoice_ids')
    def _cpt_timeline_sequence(self):
        """
        Compute the sequence number of each invoice
        within its associated timeline template.
        """
        self.timeline_sequence = 0
        for timeline_template_id in self.mapped('account_timeline_template_id'):
            move_ids = timeline_template_id.invoice_ids
            move_ids = move_ids.sorted('invoice_date_due')
            move_count = timeline_template_id.invoice_count
            for move_id, sequence in zip(move_ids, range(move_count)):
                move_id.timeline_sequence = sequence + 1

    def action_update_invoice_date(self):
        """
        Prepare and open a wizard to update invoice due dates
        based on the current timeline template.

        Returns: action
        """
        self.ensure_one()
        lines = [(0, 0, {
            'invoice_id': invoice.id,
            'new_invoice_date_due': invoice.invoice_date_due,
        }) for invoice in self.account_timeline_template_id.invoice_ids]
        return self.env['account.move.date.update'].create_and_open({
            'account_timeline_template_id': self.account_timeline_template_id.id,
            'line_ids': lines,
        })
