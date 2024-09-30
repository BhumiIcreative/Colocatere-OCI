# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    "name": "Col employee",
    "summary": "Col employee",
    "version": "17.0.1.0.0",
    "description": "Col employee",
    "author": "Aktiv software",
    "website": "",
    "license": "LGPL-3",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "account",
    # any module necessary for this one to work correctly
    "depends": ["col_property", "account_accountant"],
    # always loaded
    "data": [
        "views/res_partner_view.xml",
    ],
    # only loaded in demonstration mode
    "demo": [],
}
