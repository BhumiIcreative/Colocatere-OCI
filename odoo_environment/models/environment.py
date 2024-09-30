# coding: utf-8

from odoo import api, fields, models, _


class Environment(models.Model):
    _name = "environment"
    _description = _("Environment")

    name = fields.Char(_("Name"), required=True)
    is_active = fields.Boolean(_("Is active"), compute="_cpt_is_active")
    is_production = fields.Boolean(_("Is production environment"), copy=False)

    parameter_ids = fields.One2many(
        "environment.parameter", "environment_id", string=_("Parameters")
    )
    cron_ids = fields.One2many("environment.cron", "environment_id", string=_("Crons"))

    def _cpt_is_active(self):
        for env_id in self:
            env_id.is_active = True and (env_id.parameter_ids or env_id.cron_ids)
            for parameter_id in env_id.parameter_ids:
                env_id.is_active = (
                    env_id.is_active
                    and parameter_id.value == parameter_id.current_value
                )
            for cron_id in env_id.cron_ids:
                env_id.is_active = (
                    env_id.is_active and cron_id.state == cron_id.current_state
                )

    def apply_env(self):
        self.ensure_one()
        self.parameter_ids.apply()
        self.cron_ids.apply()
        return True

    @api.model_create_multi
    def create(self, vals):
        env_id = super().create(vals)
        if not self.env.context.get("no_load_default_lines"):
            env_id.load_default_lines()
        return env_id

    def load_default_lines(self):
        self.ensure_one()
        IrCron = self.env["ir.cron"]
        ir_cron_ids = IrCron.with_context(lang="fr_FR").search(
            [
                "|",
                ("active", "=", True),
                ("active", "=", False),
            ]
        )
        existing_cron_ids = self.cron_ids.mapped("name")
        for ir_cron_id in ir_cron_ids:
            if ir_cron_id.name not in existing_cron_ids:
                self.cron_ids = [
                    (
                        0,
                        0,
                        {
                            "name": ir_cron_id.name,
                            "state": ir_cron_id.active and "active" or "inactive",
                        },
                    )
                ]

        IrConfigParameter = self.env["ir.config_parameter"]
        config_parameter_ids = IrConfigParameter.search([])
        existing_parameter_ids = self.parameter_ids.mapped("name")
        for config_parameter_id in config_parameter_ids:
            if config_parameter_id.key not in existing_parameter_ids:
                self.parameter_ids = [
                    (
                        0,
                        0,
                        {
                            "name": config_parameter_id.key,
                            "value": config_parameter_id.value,
                        },
                    )
                ]

        if not self.is_production:
            self.toggle_cron_inactive()
            self.toggle_parameter_value()
        return True

    def toggle_cron_inactive(self):
        for cron_id in self.cron_ids:
            cron_id.state = "inactive"

    def toggle_parameter_value(self):
        for parameter_id in self.parameter_ids:
            if parameter_id.can_be_change():
                parameter_id.value = "None"
