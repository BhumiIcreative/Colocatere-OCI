# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, _


class AkawamConnector(models.AbstractModel):
    _name = "akawam.connector"
    _description = _("Akawam connector abstract class")
    _sql_constraints = [
        ("akawam_id_unique", "CHECK (1=1)", _("Akawam ID must be unique !")),
    ]

    akawam_id = fields.Integer(
        string=_("Akawam id"), readonly=True, copy=False
    )
    akawam_last_hash = fields.Char(string=_("Akawam last hash"), readonly=True)

    # Commented this method this method is not called anywhere
    # def search_by_akawam_ids(self, akawam_ids):
    #     if type(akawam_ids) is not list:
    #         akawam_ids = [akawam_ids]
    #
    #     return self.search(
    #         [
    #             ("akawam_id", "in", akawam_ids),
    #         ]
    #     )
    #
    # search_by_akawam_id = search_by_akawam_ids
