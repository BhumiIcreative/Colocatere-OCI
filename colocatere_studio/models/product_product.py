from odoo import api, fields, models, _


class ProductProduct(models.Model):
    _inherit = "product.product"

    is_used_by_akawam = fields.Boolean(string=_("Used by Akawam"))
