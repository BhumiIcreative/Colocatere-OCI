# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import models, _, fields


class AccountTimelineTemplate(models.Model):
    _inherit = "account.timeline.template"

    use_on_sale = fields.Boolean("Use on sale")

    use_on_finvest = fields.Boolean("Marque FINVEST IMMO")

    def _get_usage_values(self):
        """Override to include 'Sale' in usage values if the template is
        used for sale orders.
        """
        usage = super()._get_usage_values()
        if self.use_on_sale:
            usage.append(_("Sale"))
        return usage
