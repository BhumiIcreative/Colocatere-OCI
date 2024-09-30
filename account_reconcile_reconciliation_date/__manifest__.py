# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# -*- coding: utf-8 -*-

{
    "name": "Account Reconciliation Date",
    "summary": "Compute Latest Reconciliation Date AML",
    "version": "1.0",
    "depends": ["account_accountant"],
    "author": "Aktiv Software",
    "category": "Finance",
    "license": "AGPL-3",
    "data": [
        "views/account_move_line.xml",
    ],
    "installable": True,
    "post_init_hook": "post_init_hook",
}
