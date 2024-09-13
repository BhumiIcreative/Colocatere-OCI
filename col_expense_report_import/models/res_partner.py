# coding: utf-8
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    property_cleemy_number = fields.Integer("Cleemy number", company_dependent=True)

    @api.constrains("property_cleemy_number")
    def _check_property_cleemy_number(self):
        """
        Replace sql constrain with api constrain as property fields are not store
        in database.
        """
        for record in self:
            existing_property_cleemy_number = (
                record.search(
                    [
                        ("property_cleemy_number", "=", record.property_cleemy_number),
                        ("company_id", "=", record.company_id.id),
                    ]
                )
                - record
            )
            if existing_property_cleemy_number:
                raise ValidationError(
                    "The Cleemy number must be unique within the company. A contact with Cleemy number '%s' already exists."
                    % record.property_cleemy_number
                )
