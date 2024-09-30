# coding: utf-8
{
    "name": "Invoice timeline - Custom start date on 1st or 15",
    "summary": "Invoice timeline - Custom start date on 1st or 15",
    "description": "Invoice timeline - Custom start date on 1st or 15",
    "author": "Aktiv Software",
    "license": "LGPL-3",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "account",
    "version": "1.0",
    # any module necessary for this one to work correctly
    "depends": [
        "invoice_timeline",
    ],
    # always loaded
    "data": ["views/account_timeline_template_view.xml"],
}
