# coding: utf-8

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import base64


class PaymentImport(models.TransientModel):
    _name = "payment.import"
    _description = "Payment Import"

    name = fields.Char(string="Name")
    file = fields.Binary(string="File", required=True)
    filename = fields.Char(string="File name")
    show_group = fields.Boolean(
        string="Show group", compute="load_payment_lines", store=True
    )

    account_move_journal_id = fields.Many2one(
        "account.journal", string="Journal", required=True
    )
    journal_id = fields.Many2one(
        "account.journal",
        string="Payment journal",
        required=True,
        domain="[('type', 'in', [('cash'), ('bank')]), ('company_id', '=', company_id)]",
    )
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company,
    )

    line_ids = fields.One2many(
        "payment.import.line", "payment_import_id", string="Payment import items"
    )

    def file_split(self):
        try:
            file_string = base64.b64decode(self.file).decode("cp1252").replace("\r", "")
        except Exception as e:
            raise UserError(
                _(" Try adding valid CSV file. Failed to upload with Error :  %s" % e)
            )
        file_string = file_string.split("\n")[1:]
        return file_string

    @api.onchange("file")
    def load_payment_lines(self):
        """
        Created payment lines from the imported file
        """
        self.line_ids = [(5, 0, 0)]
        current_group = "has_group"
        if self.file:
            file_values = self.file_split()
            for line in file_values:
                values = line.split(";")
                if len(values) >= 3 and values[0] and values[3]:
                    vals = self.env["payment.import.line"].create_line(
                        current_group, values, self.company_id
                    )
                    self.line_ids = [(0, 0, vals)]
                elif len(values) >= 5 and values[0] and values[5]:
                    current_group = values[5]

        n_group = 0
        line_by_group = self.env["script.tools"].groupby(self.line_ids, "group")
        for group, line_ids in line_by_group.items():
            if not line_ids:
                continue
            n_group += 1
        self.show_group = False
        if n_group > 1:
            self.show_group = True

    def _prepare_payment_values(self, line):
        domain_in = [("payment_type", "=", "inbound"), ("code", "=", "sdd")]
        domain_out = [("payment_type", "=", "outbound"), ("code", "=", "sepa_ct")]
        domain = domain_out if line.credit > 0 else domain_in
        payment_method = self.env["account.payment.method"].search(domain, limit=1).id

        partner_bank_account_id = line.partner_id.bank_ids or False
        if partner_bank_account_id:
            partner_bank_account_id = partner_bank_account_id[0].id
        vals = {
            "payment_type": "outbound" if line.credit > 0 else "inbound",
            "amount": line.credit if line.credit > 0 else line.debit,
            "payment_method_id": payment_method,
            "journal_id": self.journal_id.id,
            "date": line.date,
            "partner_type": "supplier" if line.credit > 0 else "customer",
            "partner_id": line.partner_id.id,
            "company_id": self.company_id.id,
            "name": line.libelle,
            "partner_bank_id": partner_bank_account_id,
            "use_employee_account": True,
            "ref": line.libelle,
        }
        return vals

    def open_imported_data_view(self, payments, moves):
        """
        Show account move as payment or moves based on button clicked
        """
        if self.env.context.get("payments"):
            return {
                "type": "ir.actions.act_window",
                "res_model": "account.payment",
                "view_mode": "form",
                "domain": [("id", "in", payments)],
                "views": [
                    (self.env.ref("account.view_account_payment_tree").id, "tree"),
                    (False, "form"),
                ],
            }
        if self.env.context.get("moves"):
            return {
                "type": "ir.actions.act_window",
                "res_model": "account.move",
                "view_mode": "form",
                "domain": [("id", "in", moves)],
                "views": [
                    (self.env.ref("account.view_move_tree").id, "tree"),
                    (False, "form"),
                ],
            }

    def run_and_open(self):
        """
        Create Payment or moves record from the imported records
        """
        AccountAccount = self.env["account.account"]
        Script = self.env["script.tools"]

        line_by_group = Script.groupby(self.line_ids, "group")
        payments = []
        moves = []
        for group, line_ids in line_by_group.items():
            if not line_ids:
                continue
            if group != "has_group":
                move_id = self.env["account.move"].create(
                    {
                        "ref": group,
                        "date": line_ids[0].date,
                        "journal_id": self.account_move_journal_id.id,
                    }
                )

                move_line_ids = []
                for line in line_ids:

                    account_id = AccountAccount.search(
                        [
                            ("code", "=", line.account_code),
                            ("company_id", "=", self.company_id.id),
                        ]
                    )
                    if not account_id:
                        account_id = AccountAccount.create(
                            {
                                "code": line.account_code,
                                "name": line.account_code,
                                "account_type": "liability_payable",
                                "reconcile": True,
                            }
                        )
                    move_line_ids.append(
                        (
                            0,
                            0,
                            {
                                "account_id": account_id and account_id.id or False,
                                "partner_id": line.partner_id.id,
                                "name": line.libelle,
                                "debit": line.debit,
                                "credit": line.credit,
                            },
                        )
                    )
                    if line.partner_id:
                        account_id = line.partner_id.with_context(
                            force_company=self.company_id.id
                        ).property_account_employee_id
                        if not account_id:
                            raise UserError(
                                _(
                                    "Please fill employee account for %s"
                                    % (line.partner_id.name)
                                )
                            )
                        vals = self._prepare_payment_values(line)
                        payment_line = self.env["account.payment"].create(vals)
                        payments += payment_line.ids
                move_id.line_ids = move_line_ids
                moves += move_id.ids
        return self.open_imported_data_view(payments, moves)
