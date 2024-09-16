# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import models, _
from odoo.fields import *


class AccountTimelineTemplate(models.Model):
    _inherit = 'account.timeline.template'

    use_on_sale = Boolean(_('Use on sale'))

    use_on_finvest = Boolean(_('Marque FINVEST IMMO'))

    def _get_usage_values(self):
        """ Override to include 'Sale' in usage values if the template is
            used for sale orders.
        """
        usage = super()._get_usage_values()
        if self.use_on_sale:
            usage.append(_('Sale'))
        return usage
