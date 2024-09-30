# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Account default analytic account from project",
    "version": "17.0.1.0.0",
    "author": "Aktiv software",
    "summary": "Account default analytic account from project",
    "description": """
        Account default analytic account from project
        """,
    "license": "LGPL-3",
    "data": [
        "views/account_move_view.xml",
    ],
    "depends": [
        "account_project",
    ],
}
