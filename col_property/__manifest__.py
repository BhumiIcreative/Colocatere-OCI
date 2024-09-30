# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    "name": "COL Property",
    "summary": "COL Property",
    "description": "COL Property",
    "author": "Aktiv software",
    "category": "property",
    "version": "17.0.1.0.0",
    "license": "LGPL-3",
    # any module necessary for this one to work correctly
    "depends": [
        "akawam_link",
        "account_project",
        "account_sepa_direct_debit",
        "invoice_timeline_custom_start_date",
        "purchase",
        "project",
        "sale_management",
    ],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "data/ir_cron.xml",
        "data/cron_exception_email_template.xml",
        "views/account_move_views.xml",
        "views/property_property_views.xml",
        "views/project_project_views.xml",
        "views/property_leases_views.xml",
        "views/property_pricing_views.xml",
        "views/property_purchase_contract_views.xml",
        "views/property_room_views.xml",
        "views/purchase_order_views.xml",
        "views/sale_order_views.xml",
        # 'report/invoice_list_report.xml', (commented because action of this report is not defined)
    ],
    "installable": True,
    "application": True,
}
