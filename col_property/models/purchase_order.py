# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, _,api


class PurchaseOrder(models.Model):
    _name = "purchase.order"
    _inherit = ["purchase.order", "akawam.connector"]

    project_id = fields.Many2one("project.project", string=_("Project"))
    purchase_contract_id = fields.Many2one(
        "property.purchase_contract", string=_("Purchase contract")
    )

    @api.onchange('project_id')
    def project(self):
        if not self.project_id:
            self.purchase_contract_id = False
        elif self.project_id and self.purchase_contract_id:
            if self.project_id.id != self.purchase_contract_id.id:
                self.purchase_contract_id = False

    def _prepare_invoice(self):
        """Prepare invoice values including project
        and purchase contract information.
        """
        result = super()._prepare_invoice()
        result.update(
            {
                "project_id": self.project_id.id,
                "purchase_contract_id": self.purchase_contract_id.id,
            }
        )
        return result
