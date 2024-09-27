# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    "name": "Colocatere Studio",
    "version": "1.0",
    "summary": "studio",
    "description": "studio",
    "category": "account",
    "author": "Aktiv software",
    "website": "www.aktivsoftware.com",
    "depends": [
        'fleet',
        'col_property',
        'account_anomaly',
        'base_automation',
        'hr',
    ],
    "data": [
        'security/ir.model.access.csv',
        'data/base_automation.xml',
        'data/ir_actions_server.xml',
        'views/x_name_views.xml',
        # 'data/mail_template.xml',
        'security/colocatere_security.xml',
        'views/sale_order_views.xml',
        'views/purchase_order_views.xml',
        'views/property_property_views.xml',
        'views/res_partner_views.xml',
        'views/res_partner_category_view.xml',
        # 'views/res_users_view.xml',
        'views/res_company_views.xml',
        'views/account_payment_views.xml',
        'views/product_template_views.xml',
        'views/sdd_mandate_views.xml',
        'views/project_project_views.xml',
        'views/fleet_vehicle_log_contract_views.xml',
        'views/fleet_vehicle_views.xml',
        'views/account_move_views.xml',
        'views/account_move_line_views.xml',
        'views/account_bank_statement_line.xml',
    ],
    "installable": True,
    "auto_install": False,
    "license": "LGPL-3",
}
