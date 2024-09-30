# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, models, _, fields


class PropertyLease(models.Model):
    _name = "property.lease"
    _inherit = "akawam.connector"
    _description = _("Property lease")

    name = fields.Char(_("Name"), compute="_cpt_name", store=True)
    end_date = fields.Date(string=_("End Date"))
    start_date = fields.Date(string=_("Start Date"), required=True)

    pricing_id = fields.Many2one("property.pricing", string=_("Pricing"))
    project_id = fields.Many2one(
        "project.project", _("Project"), related="property_id.project_id", readonly=True
    )
    property_id = fields.Many2one(
        "property.property", string=_("Property"), required=True
    )
    room_id = fields.Many2one("property.room", string=_("Room"))

    lessor_partner_ids = fields.Many2many(
        "res.partner", string=_("Lessor"), relation="rel_partner_lessor"
    )
    project_ids = fields.Many2many(
        "project.project",
        relation="rel_project_project__property_lease",
        string=_("Projects"),
    )
    tenant_partner_ids = fields.Many2many(
        "res.partner", string=_("Tenant"), relation="rel_partner_tenant"
    )

    @api.depends("property_id", "property_id.name", "start_date", "end_date")
    def _cpt_name(self):
        """Compute and set the lease name based on the property and room names."""
        for lease_id in self:
            lease_id.name = lease_id.property_id.name
            if lease_id.room_id:
                lease_id.name += " - %s" % (lease_id.room_id.name)
