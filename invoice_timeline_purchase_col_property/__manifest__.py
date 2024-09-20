# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    "name": "Invoice timeline - Purchase / Col property",
    "summary": "Match col property with invoice timeline purchase",
    "version": "17.0.1.0.0",
    "description": "Match col property with invoice timeline purchase",
    "author": "Aktiv software",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "account",
    # any module necessary for this one to work correctly
    "depends": [
        "invoice_timeline_purchase",
        "col_property",
    ],
    # always loaded
    "data": [
        "views/purchase_order_view.xml",
    ],
}
