# -*- coding: utf-8 -*-

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    agence_id = fields.Many2one(string="Agence")
    cgp_id = fields.Many2one("res.partner", string='CGP', related='project_id.cgp_id', ondelete="set null",
                             store=True, copy=False)
    marque_finvest_immo = fields.Boolean("Marque FINVEST IMMO", copy=False)
    is_projet_active = fields.Boolean("Is Projet active", readonly=True, related='project_id.active', copy=False)
    signature_date = fields.Date("Signature Date", related='purchase_contract_id.signature_date', copy=False)
    sourceur_id = fields.Many2one('res.partner', string="Sourceur", readonly=True, ondelete="set null",
                                  related='project_id.sourcer_id', store=True, copy=False)
    vendeur_id = fields.Many2one("res.partner", string="Vendeur", readonly=True, ondelete="set null",
                                 related='project_id.seller_id', store=True, copy=False)
    is_signature_relle = fields.Boolean(string="Signature Réelle", readonly=True, copy=False,
                                        related='purchase_contract_id.is_real_signature')
