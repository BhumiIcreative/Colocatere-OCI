# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    agence_id = fields.Many2one('res.partner', string="Agence")
    anomaly_description = fields.Char("Anomaly Description")
    cgp_id = fields.Many2one("res.partner", string='CGP', ondelete='set null', related='project_id.cgp_id',
                             store=True)
    debut_de_bail_le = fields.Date("Debut de bail le", readonly=True, related='lease_id.start_date')
    etiquette_ids = fields.Many2many('res.partner.category', 'account_move_res_partner_category_rel', 'account_move_id',
                                     'res_partner_category_id', string='Etiquette', related='partner_id.category_id')
    etiquettes_ids = fields.Many2many('res.partner.category', 'account_move_res_partner_category_rel_2',
                                      'account_move_id',
                                      'res_partner_category_id', string='Etiquettes', readonly=True,
                                      related='partner_id.category_id')
    fin_de_bail_le = fields.Date(string='Fin de bail le', readonly=True, related='lease_id.end_date')
    gestion_particuliere = fields.Boolean('Gestion Particulière', related='project_id.gestion_particuliere')
    in_deficit = fields.Boolean("In deficit", related='project_id.in_deficit')
    marque_finvest_immo = fields.Boolean("Marque FINVEST IMMO")
    project_active = fields.Boolean("Is project active", related='project_id.active', readonly=True)
    project_id_akawam_id = fields.Integer("Projet - Akawam ID", readonly=True, related='project_id.akawam_id')
    is_recompute_from_product = fields.Boolean("Recompute From Product")
    sourceur_id = fields.Many2one('res.partner', string="Sourceur", ondelete='set null',
                                  related='project_id.sourcer_id', store=True)
    type_akawam = fields.Char(string="Type Akawam")
    vendeur_id = fields.Many2one("res.partner", string="Vendeur", related='project_id.seller_id',
                                 ondelete='set null', store=True)
    origine_externe = fields.Char("Origine Externe")
    is_balance_invoice = fields.Boolean("Facture de solde",copy=False)
