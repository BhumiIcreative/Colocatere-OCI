# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, api


class Xname(models.Model):
    _name = 'x_name'

    x_name_f = fields.Char("Name")
    external_identifier = fields.Char(string="external_identifier", copy=True)
    date = fields.Date("date", copy=True)
    account_id = fields.Integer("account_id", copy=True)
    partner_id = fields.Integer("partner_id", copy=True)
    ref = fields.Char("ref", copy=True)
    date_maturity = fields.Date("date_maturity", copy=True)
    name = fields.Char("Name", copy=True)
    debit = fields.Float("debit", copy=True)
    credit = fields.Float("credit", copy=True)
    result = fields.Integer("result", compute="_compute_result")
    field_account_id = fields.Many2one("account.move.line", string="Écriture comptable", ondelete="set null")

    @api.depends('external_identifier', 'date', 'account_id', 'partner_id', 'ref', 'date_maturity', 'name', 'debit',
                 'credit', 'result')
    def _compute_result(self):
        for record in self:
            record.result = self.env['account.move.line'].search([
                ('external_identifier', '=', record.external_identifier),
                ('account_id', '=', record.account_id),
                ('partner_id', '=', record.partner_id),
                ('ref', '=', record.ref),
                ('date_maturity', '=', record.date_maturity),
                ('name', '=', record.name),
                ('debit', '=', record.debit),
                ('credit', '=', record.credit)])
