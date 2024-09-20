# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import models, _, fields
from odoo.exceptions import UserError


class AccountMoveDateUpdate(models.TransientModel):
    _name = 'account.move.date.update'
    _inherit = 'script.wizard'
    _description = _('Account move date update wizard')

    account_timeline_template_id = fields.Many2one('account.timeline.template', string=_('Timeline'), readonly=True)

    line_ids = fields.One2many('account.move.date.update.line', 'wizard_id', string=_('Lines'))

    def confirm(self):
        """
        Update invoice dates based on the
        new due dates from writable lines.
        """
        for line_id in self.line_ids.filtered(lambda l: l.writable):
            line_id.invoice_id.write({
                'invoice_date_due': line_id.new_invoice_date_due,
                'date': line_id.new_invoice_date_due,
                'invoice_date': line_id.new_invoice_date_due,
            })
            for invoice_line_id in line_id.invoice_id.line_ids.filtered(lambda x: x.date_maturity):
                invoice_line_id.write({'date_maturity': line_id.new_invoice_date_due})
        return True

    def _compute_date(self, base_line_id):
        """
        Compute and update new invoice due dates based
        on the base line date and timeline template.
        """
        Script = self.env['script.tools']
        invoice_count = len(self.line_ids)
        lines_per_date = Script.groupby(self.account_timeline_template_id.line_ids, 'sequence')
        expected_invoice_count = len(lines_per_date.keys())
        if invoice_count != expected_invoice_count:
            raise UserError(_("I should have %s invoices but I have %s, so I can't compute next date by myself.") % (
            expected_invoice_count, invoice_count))
        i = 0
        for line_id in self.line_ids:
            if line_id == base_line_id:
                break
            i += 1
        dates = self.account_timeline_template_id.line_ids[i]._get_date(base_line_id.new_invoice_date_due)
        line_ids = self.line_ids.filtered(lambda l: l.invoice_date_due >= base_line_id.invoice_date_due)
        for line_id, new_date in zip(line_ids, dates):
            if line_id.writable:
                line_id.new_invoice_date_due = new_date
