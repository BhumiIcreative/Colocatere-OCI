# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Invoice timeline - Sale",
    'summary': "Create invoice with time interval - Sale",
    'description': "Create invoice with time interval - Sale",
    'author': "Aktiv software",
    'category': 'account',
    'version': '17.0.1.0.0',
    # any module necessary for this one to work correctly
    'depends': [
        'invoice_timeline',
        'sale_management',
    ],
    # always loaded
    'data': [
        'views/account_timeline_template_view.xml',
        'views/sale_order_view.xml',
        'wizard/sale_make_invoice_advance_view.xml',
    ]
}
