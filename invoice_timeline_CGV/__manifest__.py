# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    "name": "Invoice Timeline CGV",
    "version": "1.0",
    "summary": "Add cgv to invoice timeline",
    "description": "Add cgv to invoice timeline",
    "category": "account",
    "author": "Aktiv software",
    "website": "www.aktivsoftware.com",
    "depends": [
        "account",
        "sale",
        "invoice_timeline",
        "invoice_timeline_sale_col_property",
    ],
    "data": [
        "views/account_timeline_view.xml",
        "views/sale_invoice_view.xml",
    ],
    "installable": True,
    "auto_install": False,
    "license": "LGPL-3",
}
