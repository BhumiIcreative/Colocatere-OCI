# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    "name": "Akawam web service",
    "summary": "Akawam web service",
    "description": "Akawam web service",
    "author": "Aktiv software",
    "category": "project,sale",
    "version": "1.0",
    "depends": [
        "account",
        "col_property",
        "col_employee",
    ],
    "data": [
        "data/ir_config_parameter.xml",
        "security/ir.model.access.csv",
        "views/account_move_views.xml",
        "views/akawam_ws_call_views.xml",
        "views/account_payment_view.xml",
    ],
    "demo": [],
    "license": "LGPL-3",
}
