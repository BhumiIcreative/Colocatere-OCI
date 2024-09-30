# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class PropertyProperty(models.Model):
    _name = "property.property"
    _inherit = "akawam.connector"
    _description = "Property"

    active = fields.Boolean(_("Active"), default=True)
    room_count = fields.Integer(_("room Count"), compute="_cpt_count", store=True)
    lease_count = fields.Integer(_("Lease Count"), compute="_cpt_count", store=True)
    purchase_contract_count = fields.Integer(
        _("Purchase Contracts Count"), compute="_cpt_count", store=True
    )
    name = fields.Char(_("Name"), required=True)
    area = fields.Float(_("Area"))
    renovated_area = fields.Float(_("Renovated area"))
    in_deficit = fields.Boolean(_("Is in deficit"))
    lease_manager_id = fields.Many2one(
        "res.partner", string=_("Lease manager"), required=True
    )
    partner_address_id = fields.Many2one(
        "res.partner", string=_("Partner Adresse"), required=True
    )
    project_id = fields.Many2one("project.project", string=_("Project"))
    room_ids = fields.One2many("property.room", "property_id", string=_("Rooms"))
    lease_ids = fields.One2many("property.lease", "property_id", string=_("Leases"))
    purchase_contract_ids = fields.One2many(
        "property.purchase_contract", "property_id", string=_("Purchases Contracts")
    )
    project_ids = fields.Many2many(
        "project.project",
        relation="rel_project_project__property_property",
        string=_("Projects"),
    )

    @api.depends("room_ids", "lease_ids", "purchase_contract_ids")
    def _cpt_count(self):
        """Compute and set counts for rooms, leases, and purchase contracts."""
        for property_id in self:
            property_id.room_count = len(property_id.room_ids)
            property_id.lease_count = len(property_id.lease_ids)
            property_id.purchase_contract_count = len(property_id.purchase_contract_ids)

    def action_view_room(self):
        """Open the room records related to the current property."""
        Script = self.env["script.tools"]
        return Script.open_records(
            self.room_ids,
            name=_("Rooms"),
            context={
                "default_property_id": self.id,
            },
        )

    def action_view_leases(self):
        """Open the lease records related to the current property."""
        Script = self.env["script.tools"]
        return Script.open_records(
            self.lease_ids,
            name=_("Leases"),
            context={
                "default_property_id": self.id,
            },
        )

    def action_view_purchase_contracts(self):
        """Open the purchase contract records related to the current property."""
        Script = self.env["script.tools"]
        return Script.open_records(
            self.purchase_contract_ids,
            name=_("Purchase Contracts"),
            context={
                "default_property_id": self.id,
            },
        )
