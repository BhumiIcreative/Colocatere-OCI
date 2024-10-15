# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, _, fields
from odoo.exceptions import UserError


class AccountTimelineTemplate(models.Model):
    _name = "account.timeline.template"
    _description = _("Account timeline template")
    _order = "sequence"

    @api.depends("invoice_ids", "invoice_ids.account_timeline_template_id")
    def _cpt_invoice_count(self):
        """
        Compute and update the count of invoices associated
        with each timeline template.
        """
        for template_id in self:
            template_id.invoice_count = len(template_id.invoice_ids)

    def _get_usage_values(self):
        """
        Retrieve a list of usage values associated
        with the record.
        """
        self.ensure_one()
        return []

    def _get_used_on(self):
        """
        Generate a comma-separated string of sorted usage values.
        """
        usage = self._get_usage_values()
        usage.sort()
        return ", ".join(usage)

    active = fields.Boolean(string="Active", default=True)
    invoice_count = fields.Integer(
        string="Invoice count", compute="_cpt_invoice_count", store=True
    )
    name = fields.Char(string="Name", required=True)
    sequence = fields.Integer(string="Sequence")
    used_on = fields.Char(string="Used on", readonly=True)

    invoice_ids = fields.One2many(
        "account.move", "account_timeline_template_id", string="Invoices"
    )
    line_ids = fields.One2many(
        "account.timeline.template.line", "template_id", string="Lines", copy=True
    )

    def action_view_invoices(self):
        """
        Open a view showing the invoices associated with the current record.
        Returns: dict
        """
        Script = self.env["script.tools"]
        return Script.open_records(self.invoice_ids, name=_("Invoices"))

    @api.constrains("line_ids", "line_ids.percent", "line_ids.product_categ_id")
    def check_line_sum(self):
        self._check_line_sum()

    def _check_line_sum(self):
        """
        Validate that the sum of percentages for
        each product category equals 100.

        Raises: UserError: If the sum of percentages for
        any product category is not 100.
        """
        self.ensure_one()
        Script = self.env["script.tools"]
        if not self.line_ids:
            raise UserError(_("You should probably fill lines."))
        line_by_category = Script.groupby(self.line_ids, "product_categ_id")
        for categ_id, line_ids in line_by_category.items():
            total_percent = sum(line_ids.mapped("percent"))
            if total_percent != 100:
                if categ_id:
                    raise UserError(
                        _("Line's sum for category %s is %s, it should be 100 !")
                        % (categ_id.name, total_percent)
                    )
                raise UserError(
                    _("Line's sum is %s, it should be 100 !") % (total_percent)
                )
        return True

    def _group_lines_by_categ_id(self, lines):
        """
        Group lines by their product category,
        excluding certain categories.

        Returns: dict
        """
        ProductCategory = self.env["product.category"]
        to_exclude_product_categ_ids = self.line_ids.mapped("product_categ_id")
        prices = dict()
        for line in lines:
            product_id = line["product_id"]
            categ_id = product_id.categ_id
            key = (
                categ_id
                if categ_id in to_exclude_product_categ_ids
                else ProductCategory
            )
            if key not in prices:
                prices[key] = []
            prices[key].append(line)
        return prices

    def _get_invoiceable_lines_by_date(self, prices, date_start):
        """
        Group invoiceable lines by date based on the given start date.
        Returns:  dict
        """
        invoiceable_lines_by_date = dict()
        date_start = fields.Date.from_string(date_start)
        dates = self.line_ids[0]._get_date(date_start)
        current_sequence = self.line_ids[0].sequence
        current_date = 0
        for line_id in self.line_ids.sorted("sequence"):
            if line_id.sequence != current_sequence:
                current_sequence = line_id.sequence
                current_date += 1
            line_date = dates[current_date]
            if line_date not in invoiceable_lines_by_date:
                invoiceable_lines_by_date[line_date] = []
            if line_id.product_categ_id in prices:
                lines = prices[line_id.product_categ_id]
                for line in lines:
                    quantity = line["quantity"] * line_id.percent / 100
                    if quantity:
                        invoiceable_lines_by_date[line_date].append(
                            {
                                "line_id": line["line_id"],
                                "product_id": line["product_id"],
                                "tax_ids": line["tax_ids"],
                                "quantity": quantity,
                                "price_unit": line["price_unit"],
                                "name": line["name"],
                            }
                        )
        return invoiceable_lines_by_date

    def create_invoices(
        self,
        partner_id,
        lines,
        date_start=False,
        invoice_type="out_invoice",
        **default_invoice_values
    ):
        """
        Create invoices with specified lines with date_start or todays
        Lines is a dict list:
        [
            {
                'line_id': related object having link_to_account_move_line(move_line_id) method which return values to put in invoice lines,
                'product_id': product.product(x),
                'tax_ids': account.tax(a, b, c, ...),
                'price_unit': float,
                'quantity': float,
                'name': str,
                'account_analytic_id': account.analytic.account(y)
            }
        ]
        """
        AccountMove = self.env["account.move"]
        self.ensure_one()
        date_start = date_start or fields.Date.today()
        template_copy_id = self.copy()
        prices = template_copy_id._group_lines_by_categ_id(lines)
        invoiceable_lines_by_date = template_copy_id._get_invoiceable_lines_by_date(
            prices, date_start
        )
        move_ids = AccountMove
        for date, lines in invoiceable_lines_by_date.items():
            move_id = AccountMove.create(
                dict(
                    {
                        "partner_id": partner_id.id,
                        "move_type": invoice_type,
                        "date": date,
                        "invoice_date": date,
                        "invoice_date_due": date,
                        "account_timeline_template_id": template_copy_id.id,
                    },
                    **default_invoice_values
                )
            )

            if invoice_type == "out_invoice":
                account_id = move_id.partner_id.property_account_receivable_id
            elif invoice_type == "in_invoice":
                account_id = move_id.partner_id.property_account_payable_id
            invoice_line_ids = []
            for line in lines:
                values = {
                    "product_id": line["product_id"].id,
                    "quantity": line["quantity"],
                    "price_unit": line["price_unit"],
                    "tax_ids": [(6, 0, line["tax_ids"].ids)],
                    "name": line["name"],
                    "analytic_distribution": False,
                }
                values = line["line_id"].link_to_account_move_line(values)
                invoice_line_ids.append((0, 0, values))

            move_id.invoice_line_ids = invoice_line_ids
            for line_id in move_id.invoice_line_ids:
                line_id.account_id = line_id.account_id.id
            move_ids |= move_id
        min_date = min(move_ids.mapped("invoice_date_due"))
        max_date = max(move_ids.mapped("invoice_date_due"))
        partner_id = move_ids[0].partner_id
        amount_total = sum(move_ids.mapped("amount_total_signed"))
        template_copy_id.name = "%s - %s: %s (%s to %s)" % (
            template_copy_id.name,
            partner_id.name,
            amount_total,
            min_date,
            max_date,
        )
        template_copy_id.active = False
        return move_ids


def write(self, vals):
    """
    Override: write method
    Returns: bool
    """
    res = super().write(vals)
    if "used_on" not in vals:
        used_val = {
            "used_on": self._get_used_on(),
        }
        return super().write(used_val)
    return res
