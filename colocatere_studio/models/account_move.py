# -*- coding: utf-8 -*-
from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    agence_id = fields.Many2one('res.partner', string="Agence", copy=False)
    anomaly_description = fields.Char("Anomaly Description", copy=False)
    cgp_id = fields.Many2one("res.partner", string='CGP', ondelete='set null', related='project_id.cgp_id',
                             store=True, copy=False)
    debut_de_bail_le = fields.Date("Debut de bail le", readonly=True, related='lease_id.start_date', copy=False)
    etiquette_ids = fields.Many2many('res.partner.category', 'account_move_res_partner_category_rel', 'account_move_id',
                                     'res_partner_category_id', string='Etiquette', copy=False,
                                     related='partner_id.category_id')
    etiquettes_ids = fields.Many2many('res.partner.category', 'account_move_res_partner_category_rel_2',
                                      'account_move_id',
                                      'res_partner_category_id', string='Etiquettes', readonly=True,
                                      related='partner_id.category_id', copy=False)
    fin_de_bail_le = fields.Date(string='Fin de bail le', readonly=True, related='lease_id.end_date', copy=False)
    gestion_particuliere = fields.Boolean('Gestion Particulière', related='project_id.gestion_particuliere', copy=False)
    in_deficit = fields.Boolean("In deficit", related='project_id.in_deficit', copy=False)
    marque_finvest_immo = fields.Boolean("Marque FINVEST IMMO", copy=False)
    project_active = fields.Boolean("Is project active", related='project_id.active', readonly=True, copy=False)
    project_id_akawam_id = fields.Integer("Projet - Akawam ID", readonly=True, related='project_id.akawam_id',
                                          copy=False)
    is_recompute_from_product = fields.Boolean("Recompute From Product", copy=False)
    sourceur_id = fields.Many2one('res.partner', string="Sourceur", ondelete='set null',
                                  related='project_id.sourcer_id', store=True, copy=False)
    type_akawam = fields.Char(string="Type Akawam", copy=False)
    vendeur_id = fields.Many2one("res.partner", string="Vendeur", related='project_id.seller_id',
                                 ondelete='set null', store=True, copy=False)
    origine_externe = fields.Char("Origine Externe", copy=False)
    is_balance_invoice = fields.Boolean("Facture de solde", copy=False)
