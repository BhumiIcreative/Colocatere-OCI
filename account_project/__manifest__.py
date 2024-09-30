# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    "name": "Account project",
    "version": "17.0.1.0.0",
    "author": "Aktiv software",
    "summary": "Account project",
    "description": """
        Account project
        """,
    "license": "LGPL-3",
    "data": [
        "views/account_move_view.xml",
        "views/project_project_view.xml",
    ],
    "depends": [
        "account",
        "project",
        "script_tools",
    ],
}
