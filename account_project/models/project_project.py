# coding: utf-8

from odoo import api, fields, models, _


class ProjectProject(models.Model):
    _inherit = "project.project"

    account_move_count = fields.Integer(
        string=_("Invoices count"), compute="_cpt_account_move_count", store=True
    )

    account_move_ids = fields.One2many(
        "account.move", "project_id", string=_("Invoices")
    )

    @api.depends("account_move_ids")
    def _cpt_account_move_count(self):
        """Computes the count of related invoices for each project"""
        for project in self:
            project.account_move_count = len(project.account_move_ids)

    def action_view_invoices(self):
        """Opens the related invoices in a new window. Calls the `open_records` method from 'script.tools'"""
        Script = self.env["script.tools"]
        context = {
            "default_project_id": self.id,
        }
        return Script.open_records(
            self.account_move_ids, name=_("Invoices"), context=context
        )
