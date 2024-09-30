# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    "name": "Account Warn Payment",
    "summary": """
        Add a pop-up message when creating a payment if the
        partner has a warning or blockage""",
    "version": "17.0.1.0.0",
    "license": "LGPL-3",
    "author": "Aktiv software",
    "website": "https://www.aktivsoftware.com",
    "depends": ["account"],
    "data": [
        "security/account_security.xml",
        "views/res_config_settings_views.xml",
        "views/res_partner_view.xml",
        "views/account_payment_view.xml",
        "views/account_payment_register_view.xml",
    ],
}
