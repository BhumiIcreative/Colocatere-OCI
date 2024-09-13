# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': "Invoice timeline - Purchase",
    'summary': "Create invoice with time interval - Purchase",
    'description': "Create invoice with time interval - Purchase",
    'author': "Aktiv software",
    'category': 'account',
     "version": "17.0.1.0.0",
    "license": "LGPL-3",
    # any module necessary for this one to work correctly
    'depends': [
        'invoice_timeline',
        'purchase',
    ],
    # always loaded
    'data': [
        'views/account_timeline_template_view.xml',
        'views/purchase_order_view.xml',
    ],
}
