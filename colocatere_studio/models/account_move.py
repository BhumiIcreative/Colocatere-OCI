# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class AccountMove(models.Model):
    _inherit = "account.move"

    agence_id = fields.Many2one('res.partner', string=_("Agence"))
    anomaly_description = fields.Char("Anomaly Description")
    cgp_id = fields.Many2one("res.partner", string=_('CGP'), ondelete='set null', related='project_id.cgp_id')
    # debut_de_bail_le = fields.Date("Debut de bail le", readonly=True, related='lease_id.start_date')
    etiquette_ids = fields.Many2many('res.partner.category', 'account_move_res_partner_category_rel', 'account_move_id',
                                     'res_partner_category_id', string='Etiquette', related='partner_id.category_id')
    etiquettes_ids = fields.Many2many('res.partner.category', 'account_move_res_partner_category_rel_2',
                                      'account_move_id',
                                      'res_partner_category_id', string='Etiquettes', readonly=True,
                                      related='partner_id.category_id')
    # fin_de_bail_le = fields.date(string=_('Fin de bail le'), readonly=True, related='lease_id.end_date')
    gestion_particuliere = fields.Boolean('Gestion Particulière', related='project_id.gestion_particuliere')
    in_deficit = fields.Boolean("in deficit", related='project_id.in_deficit')
    marque_finvest_immo = fields.Boolean("Marque FINVEST IMMO")
    project_active = fields.Boolean("Is project active", related='project_id.active', readonly=True)
    project_id_akawam_id = fields.Integer("Projet - Akawam ID", readonly=True, related='project_id.akawam_id')
    is_recompute_from_product = fields.Boolean("Recompute From Product")
    sourceur_id = fields.Many2one('res.partner', string=_("Sourceur"), ondelete='set null',
                                  related='project_id.sourcer_id')
    type_akawam = fields.Char(string=_("Type Akawam"))
    vendeur_id = fields.Many2one("res.partner", string=_("Vendeur"), related='project_id.seller_id',
                                 ondelete='set null')
