# coding: utf-8
import base64
from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ExpenseReportImport(models.TransientModel):
    _name = "expense_report_import"
    _description = "Import expense report"

    name = fields.Char(string=_("Name"))
    file = fields.Binary(string=_("File"), required=True)
    filename = fields.Char(string=_("File name"))
    account_move_journal_id = fields.Many2one(
        "account.journal", string=_("Journal"), required=True
    )
    company_id = fields.Many2one(
        "res.company",
        string=_("Company"),
        required=True,
        default=lambda self: self.env.company,
    )
    line_ids = fields.One2many(
        "expense_report_import_line",
        "expense_report_import_id",
        string="Expense report import lines",
    )

    @api.onchange("file")
    def _onchange_file(self):
        self.line_ids = [(5, 0, 0)]
        if self.file:
            # Décoder le fichier
            try:
                content = base64.b64decode(self.file).decode("cp1252").replace("\r", "")
            except Exception as e:
                raise UserError(
                    _(
                        " Try adding valid CSV file. Failed to upload with Error :  %s"
                        % e
                    )
                )
            # Séparer les lignes et retirer la première ligne contenant les noms de colonnes
            lines = content.split("\n")[1:]
            # Supprimer les lignes vides
            lines = list(filter(len, lines))
            # Séparer les colonnes
            lines = list(map(lambda line: line.split(";"), lines))
            for line in lines:
                self.line_ids = [
                    (
                        0,
                        0,
                        {
                            "date": datetime.strptime(line[0], "%d/%m/%Y").strftime(
                                "%Y-%m-%d"
                            ),
                            "account_code": line[1],
                            "move_ref": line[2],
                            "label": line[3],
                            "debit": line[4].replace(",", "."),
                            "credit": line[5].replace(",", "."),
                            "analytic_account_id": line[6],
                            "partner_id": (
                                self._get_partner_id(line[7]) if line[7] else None
                            ),
                        },
                    )
                ]

    def _get_partner_id(self, cleemy_number):
        """Search for partners with a property_cleemy_number that matches the provided cleemy_number"""
        partner_ids = self.env["res.partner"].search(
            [("property_cleemy_number", "=", int(cleemy_number))]
        )
        if len(partner_ids) == 0:
            raise UserError(_("No partner with number %s") % cleemy_number)
        if len(partner_ids) > 1:
            raise UserError(_("Multiple partners with number %s") % cleemy_number)
        return partner_ids.id

    def run(self):
        # Tour à vide pour vérifier que les comptes des employés sont renseignés
        # Grouper les lignes du fichier d'import par référence de facture
        #        for move_ref, lines in self.env['script.tools'].groupby(self.line_ids, 'move_ref').items():
        #            if not (lines[0].partner_id.with_context(force_company=self.company_id.id).property_account_employee_id):
        #                raise UserError(_("Please fill employee account for %s", lines[0].partner_id.name))

        # Grouper les lignes du fichier d'import par référence de facture
        moves = []
        for move_ref, lines in (
            self.env["script.tools"].groupby(self.line_ids, "move_ref").items()
        ):
            # Préparer les lignes de facture
            vals = []
            for line in lines:
                account = self.env["account.account"].search(
                    [
                        ("code", "=", line.account_code),
                        ("company_id", "=", self.company_id.id),
                    ]
                )
                if not account:
                    account = self.env["account.account"].create(
                        {
                            "code": line.account_code,
                            "name": line.account_code,
                            "account_type": "liability_payable",
                            "reconcile": True,
                        }
                    )
                vals.append(
                    (
                        0,
                        0,
                        {
                            "account_id": account and account.id or False,
                            "partner_id": lines[0].partner_id.id,
                            "name": line.label,
                            "debit": line.debit,
                            "credit": line.credit,
                            "analytic_line_ids": (
                                [(4, line.analytic_account_id)]
                                if line.analytic_account_id
                                else []
                            ),
                        },
                    )
                )
            """
            Créer la facture
            TODO ligne compte fournisseur sort dans ligne de facture et donne un montant = 0€
            il faudrait qu'il soit uniquement en ligne d'écriture comptable et que le TTC soit correcte
            attention lignes 76 et 91 c'est lines[0].partner_id.id qui est récupéré
            """
            move = self.env["account.move"].create(
                {
                    "date": lines[0].date,
                    "ref": _("Expense report %s") % move_ref,
                    "move_type": "in_invoice",
                    "journal_id": self.account_move_journal_id.id,
                    "partner_id": lines[0].partner_id.id,
                    "line_ids": vals,
                }
            )
            move._onchange_partner_id()
            moves += move.ids
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
