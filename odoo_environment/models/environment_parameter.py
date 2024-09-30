# coding: utf-8

from odoo import api, fields, models, _


class Environment(models.Model):
    _name = "environment.parameter"
    _description = _("Environment parameter")

    name = fields.Char(_("Name"), required=True)
    value = fields.Text(_("Value"), required=True)
    current_value = fields.Text(_("Current value"), compute="_cpt_current_value")

    environment_id = fields.Many2one("environment", string=_("Environment"))

    def _search_parameter_id(self):
        self.ensure_one()
        IrConfigParameter = self.env["ir.config_parameter"]
        return IrConfigParameter.search(
            [
                ("key", "=", self.name),
            ]
        )

    @api.depends("name")
    def _cpt_current_value(self):
        for parameter_id in self:
            config_parameter_id = parameter_id._search_parameter_id()
            parameter_id.current_value = config_parameter_id.value

    def apply(self):
        IrConfigParameter = self.env["ir.config_parameter"]
        for parameter_id in self:
            config_parameter_id = parameter_id._search_parameter_id()
            if not config_parameter_id:
                IrConfigParameter.create(
                    {
                        "key": parameter_id.name,
                        "value": parameter_id.value,
                    }
                )
            else:
                config_parameter_id.value = parameter_id.value
        return True

    def can_be_change(self):
        self.ensure_one()
        name = self.name.split(".")[0]
        module_ids = self.env["ir.module.module"].search(
            [
                ("author", "=", "Odoo S.A."),
                ("name", "=", self.name.split(".")[0]),
            ]
        )
        return not bool(module_ids) and name != "database"
