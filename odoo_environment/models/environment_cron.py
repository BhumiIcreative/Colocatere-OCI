# coding: utf-8

from odoo import api, fields, models, _

STATES = [
    ("active", _("Active")),
    ("inactive", _("Inactive")),
]


class Environment(models.Model):
    _name = "environment.cron"
    _description = _("Environment cron")

    name = fields.Char(_("Cron name"), required=True)
    state = fields.Selection(STATES, _("State"), required=True, default="active")
    current_state = fields.Selection(
        STATES, _("Current state"), compute="_cpt_current_state"
    )

    environment_id = fields.Many2one("environment", string=_("Environment"))

    def _search_ir_cron_id(self):
        self.ensure_one()
        IrCron = self.env["ir.cron"]
        lang_ids = self.env["res.lang"].search(
            [
                ("active", "=", True),
            ]
        )
        for lang_id in lang_ids:
            cron_id = IrCron.with_context(lang=lang_id.code).search(
                [
                    ("name", "=", self.name),
                    "|",
                    ("active", "=", True),
                    ("active", "=", False),
                ]
            )
            if cron_id:
                return cron_id
        return IrCron

    @api.depends("name")
    def _cpt_current_state(self):
        for cron_id in self:
            ir_cron_id = cron_id._search_ir_cron_id()
            cron_id.current_state = "active" if ir_cron_id.active else "inactive"

    def apply(self):
        for cron_id in self:
            ir_cron_id = cron_id._search_ir_cron_id()
            if ir_cron_id:
                ir_cron_id.active = cron_id.state == "active"
        return True
