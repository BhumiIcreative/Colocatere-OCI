# -*- coding: utf-8 -*-

from odoo import models, fields


class AccountMove(models.Model):
    """
     Inherited: Sale Order
    """
    _inherit = 'sale.order'

    oci_cgv = fields.Html('Terms of sales')
