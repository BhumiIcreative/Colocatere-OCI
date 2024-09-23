# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    "name": "Colocatere Studio",
    "version": "1.0",
    "summary": "Add cgv to invoice timeline",
    "description": "Add cgv to invoice timeline",
    "category": "account",
    "author": "Aktiv software",
    "website": "www.aktivsoftware.com",
    "depends": [
        'account',
        'sale_management',
        'fleet',
        'col_property',
        'project',
    ],
    "data": [
        'views/sale_order_views.xml',
        'views/purchase_order_views.xml',
        # 'views/property_property_views.xml',
        'views/res_partner_views.xml',
        'views/res_partner_category_view.xml',
        # 'views/res_users_view.xml',
        'views/res_company_views.xml',
        'views/account_payment_views.xml',
        # 'views/account_bank_statement_line.xml',
        # 'views/product_product_views.xml',
        'views/product_template_views.xml',
    ],
    "installable": True,
    "auto_install": False,
    "license": "LGPL-3",
}
