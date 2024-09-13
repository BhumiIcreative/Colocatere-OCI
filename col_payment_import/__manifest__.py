# coding: utf-8
{
    "name": "Col payment import",
    "summary": "Col payment import",
    "description": "Col payment import",
    "author": "Aktiv software",
    "website": "http://www.aktivsoftware.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "account",
    "version": "17.0.1.0.0",
    "license": "LGPL-3",
    # any module necessary for this one to work correctly
    "depends": [
        "account_accountant",
        "col_employee",
        "script_tools",
    ],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "wizard/payment_import.xml",
    ],
    # only loaded in demonstration mode
    "demo": [],
}
