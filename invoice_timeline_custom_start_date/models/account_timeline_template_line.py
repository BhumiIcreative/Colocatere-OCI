# coding: utf-8

from odoo import models

# from v12.enterprise.pos_blackbox_be.models.pos_blackbox_be import product_template


class AccountTimelineTemplateLine(models.Model):
    _inherit = "account.timeline.template.line"

    def _get_date(self, date_start):
        """
        Computes a list of dates starting from `date_start` based on the
        intervals defined in the timeline template.
        """
        if self != self.template_id.line_ids[0]:

            return super()._get_date(date_start)

        Script = self.env["script.tools"]
        res = [date_start]

        month_delta = 1
        if date_start.day > 15:
            month_delta = 2

        date_start = Script.date_delta(
            date_start, month_delta, delta_type="months"
        ).replace(day=1)

        next_lines = self.template_id.line_ids[1:].sorted('sequence')
        if next_lines:
            res += next_lines[0]._get_date(date_start)

        return res
