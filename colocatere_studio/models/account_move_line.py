# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    catgorie_darticle_id = fields.Many2one('product.category', string='Catégorie d article')
    statement_line_id = fields.Many2one('account.bank.statement.line',
                                        string='Bank statement line reconciled with this entry')
    etiquettes_ids = fields.Many2many('res.partner.category', 'account_move_line_res_partner_category_rel',
                                      'account_move_line_id',
                                      'res_partner_category_id', string='Etiquettes', ondelete='cascade', readonly=True,
                                      related='partner_id.category_id')
    external_reconcile = fields.Char("external_reconcile")
    field_9zob8_ids = fields.One2many('account.partial.reconcile', 'debit_move_id', string='New One2many')
    field_idF59_id = fields.Many2one('res.partner', string='New Champ lié')
    in_deficit = fields.Boolean(string="in deficit", related='move_id.in_deficit', readonly=True, store=True)
    marque_finvest_immo = fields.Boolean(string="Marque FINVEST IMMO", related='move_id.marque_finvest_immo',
                                         readonly=True)
    projet_id = fields.Many2one("project.project", string='Projet', ondelete='set null', readonly=True,
                                related='move_id.project_id', store=True)
    qualit_partenaire_ids = fields.Many2many('res.partner.category', 'account_move_line_res_partner_category_rel_1',
                                             'account_move_line_id',
                                             'res_partner_category_id', string='Qualité Partenaire', ondelete='cascade',
                                             readonly=True, related='partner_id.category_id')
    is_recompute_from_product = fields.Boolean("X Studio Recompute From Product")
    external_identifier = fields.Char("external_identifier")
