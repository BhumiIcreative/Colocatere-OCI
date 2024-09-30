# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, _


class AccountTimelineTemplate(models.Model):
    _inherit = "account.timeline.template"

    use_on_purchase = fields.Boolean("Use on purchase")

    def _get_usage_values(self):
        """
        Override to include 'Purchase' in usage values if the template is
        used for purchase orders.
        """
        usage = super()._get_usage_values()
        if self.use_on_purchase:
            usage.append(_("Purchase"))
        return usage
