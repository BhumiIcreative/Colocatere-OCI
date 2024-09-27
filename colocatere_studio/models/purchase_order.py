# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    marque_finvest_immo = fields.Boolean("Marque FINVEST IMMO")
    is_projet_active = fields.Boolean("Is Projet active", readonly=True, related='project_id.active')
    tag_ids = fields.Many2many("res.partner.category", "purchase_order_res_partner_category_rel", "purchase_order_id",
                               "res_partner_category_id", string='Étiquette', ondelete='cascade', readonly=True,
                               related='partner_id.category_id')
