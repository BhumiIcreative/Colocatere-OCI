# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, models, _, fields


class PurchaseContract(models.Model):
    _name = "property.purchase_contract"
    _inherit = "akawam.connector"
    _description = _("Purchase contract")

    @api.model
    def _get_default_currency(self):
        """Return the default currency for account moves"""
        journal = self.env["account.move"]._search_default_journal()
        return journal.currency_id or journal.company_id.currency_id

    amount = fields.Monetary(string=_("Property price (buying price)"))
    compromise_date = fields.Date(string=_("Compromise date"))
    is_real_compromise = fields.Boolean(
        string=_("Is the compromise date the real one ?")
    )
    is_real_signature = fields.Boolean(string=_("Is the signature date the real one ?"))
    name = fields.Char(_("Name"), related="property_id.name")
    owner_type = fields.Selection(
        [
            ("owner", _("Owner")),
            ("co-owners", _("Co-Owners")),
        ],
        string=_("Owner type"),
        compute="_cpt_owner_type",
        store=True,
        readonly=True,
    )
    signature_date = fields.Date(string=_("Signature date"))
    currency_id = fields.Many2one(
        "res.currency",
        store=True,
        readonly=True,
        string=_("Currency"),
        required=True,
        default=_get_default_currency,
    )
    project_id = fields.Many2one(
        "project.project",
        string=_("Project"),
        related="property_id.project_id",
        readonly=True,
    )
    property_id = fields.Many2one(
        "property.property", string=_("Property"), required=True
    )
    commission_ids = fields.One2many(
        "property.commission_line", "purchase_contract_id", string=_("Commissions")
    )
    owner_ids = fields.Many2many(
        "res.partner", "rel_purchase_owner", string=_("Owners")
    )
    project_ids = fields.Many2many(
        "project.project",
        relation="rel_project_project__property_purchase_contract",
        string=_("Projects"),
    )

    @api.depends("owner_ids")
    def _cpt_owner_type(self):
        """Compute and set the owner type based on the number of owners."""
        for purchase_contract_id in self:
            purchase_contract_id.owner_type = "owner"
            if len(purchase_contract_id.owner_ids) > 1:
                purchase_contract_id.owner_type = "co-owners"
