# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    "name": "Invoice timeline - Sale / Col property",
    "summary": "Match col property with invoice timeline sale",
    "description": "Match col property with invoice timeline sale",
    "author": "Aktiv software",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "account",
    "version": "1.0",
    # any module necessary for this one to work correctly
    "depends": [
        "invoice_timeline_sale",
        "col_property",
        "akawam_link",
    ],
    # always loaded
    "data": [
        "views/sale_order_view.xml",
    ],
}
