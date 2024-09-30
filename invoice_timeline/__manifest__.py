# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Invoice timeline",
    "summary": "Create invoice with time interval",
    "description": "Create invoice with time interval",
    "author": "Aktiv Software",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "account",
    "version": "17.0.1.0.0",
    "license": "LGPL-3",
    # any module necessary for this one to work correctly
    "depends": ["account", "script_tools", "sale"],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "views/account_move_view.xml",
        "views/account_timeline_template_view.xml",
        "views/sale_order_views.xml",
        "wizard/account_move_date_update_view.xml",
    ],
}
