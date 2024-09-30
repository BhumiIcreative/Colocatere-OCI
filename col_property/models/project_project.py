# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ProjectProject(models.Model):
    _name = "project.project"
    _inherit = ["project.project", "akawam.connector"]

    lease_count = fields.Integer(
        string=_("Lease count"), compute="_cpt_count", store=True
    )
    property_count = fields.Integer(
        string=_("Property count"), compute="_cpt_count", store=True
    )
    purchase_contract_count = fields.Integer(
        string=_("Purchase contract count"), compute="_cpt_count", store=True
    )
    sale_count = fields.Integer(
        string=_("Sale count"), compute="_cpt_count", store=True
    )
    purchase_count = fields.Integer(
        string=_("Purchase count"), compute="_cpt_count", store=True
    )
    in_deficit = fields.Boolean(
        string=_("Is in deficit"), compute="_cpt_in_deficit", store=True
    )
    transfer_locked = fields.Boolean(string=_("Transfer locked"))

    seller_id = fields.Many2one("res.partner", string=_("Seller"))
    cgp_id = fields.Many2one("res.partner", string=_("CGP"))
    sourcer_id = fields.Many2one("res.partner", string=_("Sourcer"))
    subcontractor_id = fields.Many2one("res.partner", string=_("Subcontractor"))
    decorator_id = fields.Many2one("res.partner", string=_("Decorator"))

    lease_ids = fields.Many2many(
        "property.lease",
        relation="rel_project_project__property_lease",
        string=_("Lease"),
    )
    property_ids = fields.Many2many(
        "property.property",
        relation="rel_project_project__property_property",
        string=_("Property"),
    )
    purchase_contract_ids = fields.Many2many(
        "property.purchase_contract",
        relation="rel_project_project__property_purchase_contract",
        string=_("Purchase contracts"),
    )
    sale_ids = fields.One2many("sale.order", "project_id", string=_("Sales"))
    purchase_ids = fields.One2many(
        "purchase.order", "project_id", string=_("Purchases")
    )

    agency_col_id = fields.Many2one("res.partner", string=_("Agence"))

    def _fix_project_id_to_project_ids(self):
        property_ids = self.env["property.property"].search(
            [
                ("project_id", "!=", False),
            ]
        )
        for property_id in property_ids:
            property_id.project_ids = [(4, property_id.project_id.id)]
        lease_ids = self.env["property.lease"].search(
            [
                ("project_id", "!=", False),
            ]
        )
        for lease_id in lease_ids:
            lease_id.project_ids = [(4, lease_id.project_id.id)]
        purchase_contract_ids = self.env["property.purchase_contract"].search(
            [
                ("project_id", "!=", False),
            ]
        )
        for purchase_contract_id in purchase_contract_ids:
            purchase_contract_id.project_ids = [(4, purchase_contract_id.project_id.id)]

    @api.depends(
        "purchase_ids",
        "purchase_contract_ids",
        "sale_ids",
        "property_ids",
        "property_ids.room_ids",
        "lease_ids",
    )
    def _cpt_count(self):
        """Compute and set counts for purchases, contracts, sales, properties, and leases."""
        for project_id in self:
            project_id.purchase_contract_count = len(project_id.purchase_contract_ids)
            project_id.sale_count = len(project_id.sale_ids)
            project_id.purchase_count = len(project_id.purchase_ids)
            project_id.property_count = len(project_id.property_ids)
            project_id.lease_count = len(project_id.lease_ids)

    @api.depends("property_ids", "property_ids.in_deficit")
    def _cpt_in_deficit(self):
        """Compute if any related properties are in deficit."""
        for project_id in self:
            project_id.in_deficit = any(project_id.property_ids.mapped("in_deficit"))

    def action_view_room(self):
        """Open the room records related to the current project."""
        script = self.env["script.tools"]
        return script.open_records(
            self.room_ids,
            name=_("Rooms"),
            context={
                "default_project_id": self.id,
            },
        )

    def action_view_property(self):
        """Open the property records related to the current project."""
        script = self.env["script.tools"]
        return script.open_records(
            self.property_ids,
            name=_("Property"),
            context={
                "default_project_id": self.id,
            },
        )

    def action_view_purchase_contracts(self):
        """Open the purchase contract records related to the current project."""
        script = self.env["script.tools"]
        return script.open_records(
            self.purchase_contract_ids,
            name=_("Purchase contracts"),
            context={
                "default_project_id": self.id,
                "default_project_ids": [(4, self.id)],
            },
        )

    def action_view_leases(self):
        """Open the lease records related to the current project."""
        Script = self.env["script.tools"]
        return Script.open_records(
            self.lease_ids,
            name=_("Leases"),
            context={
                "default_project_id": self.id,
            },
        )

    # def action_view_sales(self):
    #     """ Open the sales records related to the current project."""
    #     Script = self.env['script.tools']
    #     return Script.open_records(self.sale_ids, name=_('Sales'), context={
    #         'default_project_id': self.id,
    #     })

    def action_view_purchases(self):
        """Open the purchase records related to the current project."""
        Script = self.env["script.tools"]
        return Script.open_records(
            self.purchase_ids,
            name=_("Purchases"),
            context={
                "default_project_id": self.id,
            },
        )
