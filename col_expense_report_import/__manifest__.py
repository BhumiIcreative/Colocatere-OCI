# coding: utf-8
{
    "name": "Col expense report import",
    "summary": "Col expense report import",
    "description": "Col expense report import",
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
        "col_employee",
        "script_tools",
        "account_accountant",
    ],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "views/res_partner_views.xml",
        "wizard/expense_report_import.xml",
    ],
    # only loaded in demonstration mode
    "demo": [],
}
