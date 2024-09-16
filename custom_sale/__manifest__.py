# coding: utf-8
{
    'name': "custom sale",

    'summary':
                   """
                   custom sale
                   """,

    'description': """
        custom sale
    """,

    'author': "Aktiv software",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category':    'sale',
    'version':     '1.0',

    # any module necessary for this one to work correctly
    'depends': [
        'col_property',
        'akawam_link',
    ],

    # always loaded
    'data': [
        'data/ir_cron.xml',
        "report/sale_invoice_summary.xml",
        'views/sale_order_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [],
    "license": "LGPL-3",
}
