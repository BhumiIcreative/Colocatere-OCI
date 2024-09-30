# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# -*- coding: utf-8 -*-

from . import models


def post_init_hook(env):
    """
    Compute all account.full.reconcile latest date
    """
    afr = env["account.full.reconcile"].search([])
    for line in afr:
        line._compute_date()
