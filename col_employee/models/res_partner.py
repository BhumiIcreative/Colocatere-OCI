# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, _


class ResPartner(models.Model):
    _inherit = "res.partner"

    property_account_employee_id = fields.Many2one(
        "account.account",
        string=_("Employee account"),
        domain=[
            ("account_type", "=", "liability_payable"),
            ("deprecated", "=", False),
        ],
        company_dependent=True,
    )

    """ Update or create property for the employee account """

    def _update_property_account_employee_id(self, field_property_account_employee_id):
        IrProperty = self.env["ir.property"]
        # Fetch partners with a non-null employee account
        self._cr.execute(
            """
        SELECT
            id,
            property_account_employee_id
        FROM
            res_partner
        WHERE
            property_account_employee_id IS NOT NULL
        """
        )
        partner_account_employee_ids = self._cr.dictfetchall()
        for partner_account_employee_id in partner_account_employee_ids:
            # Get the account record
            property_account_employee_id = self.env["account.account"].browse(
                partner_account_employee_id["property_account_employee_id"]
            )
            res_id = "res.partner,%s" % (partner_account_employee_id["id"])
            company_id = property_account_employee_id.company_id
            # Search for the existing property
            property_id = IrProperty.search(
                [
                    ("res_id", "=", res_id),
                    ("fields_id", "=", field_property_account_employee_id.id),
                    ("company_id", "=", company_id.id),
                ]
            )
            if not property_id:
                # Create the property if it doesn't exist
                property_id = IrProperty.create(
                    {
                        "name": "property_account_employee_id",
                        "company_id": company_id.id,
                        "fields_id": field_property_account_employee_id.id,
                        "res_id": res_id,
                        "value_reference": "account.account,%s"
                        % (property_account_employee_id.id),
                        "type": "many2one",
                    }
                )

    def init(self):
        """Initialize and update employee account properties, Get the field definition for the employee account"""
        field_id = self.env["ir.model.fields"].search(
            [
                ("model_id.model", "=", self._name),
                ("name", "=", "property_account_employee_id"),
            ]
        )
        # Check if the field should be updated
        update_property_account_employee_id = field_id and field_id.store or False
        if update_property_account_employee_id:
            self._update_property_account_employee_id(
                field_id
            )  # Update employee account properties
        super().init()
