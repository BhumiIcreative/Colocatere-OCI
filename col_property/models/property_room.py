# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, _, fields


class Propertyroom(models.Model):
    _name = "property.room"
    _description = "Property Room"
    _inherit = "akawam.connector"

    lease_count = fields.Integer(
        string=_("Lease Count"), readonly=True, compute="_get_lease_count"
    )
    name = fields.Char(string=_("Name"), required=True)
    property_id = fields.Many2one(
        "property.property", string=_("Property"), required=True
    )
    lease_ids = fields.One2many("property.lease", "room_id", string=_("Leases"))

    def action_view_lease(self):
        """Open lease records for the current property and room."""
        Script = self.env["script.tools"]
        return Script.open_records(
            self.lease_ids,
            name=_("Leases"),
            context={
                "default_property_id": self.property_id.id,
                "default_room_id": self.id,
            },
        )

    @api.depends("lease_ids")
    def _get_lease_count(self):
        """Compute and set the count of associated lease records."""
        for record in self:
            record.lease_count = len(record.lease_ids)
