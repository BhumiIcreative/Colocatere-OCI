# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, _
from odoo.exceptions import UserError

import hashlib
import base64
import json
import requests
import time

# Do not put this contraints everywhere
fields_args = {
    "required": True,
    "readonly": True,
}


def hash_dict(datas):
    keys = list(datas.keys())  # Get all keys from the dictionary
    keys.sort()
    res = []
    for k in keys:
        value = datas[k]
        if (
            type(value) is dict
        ):  # If the value is a dictionary, recursively hash it
            value = hash_dict(value)
        res.append((k, value))
    res = json.dumps(res)  # Convert the list of tuples to a JSON string
    res = base64.b64encode(res.encode())  # Encode the JSON string to base64
    return hashlib.sha512(res).hexdigest()


class AkawamWsCall(models.Model):
    _name = "akawam.ws.call"
    _description = _("Akawam Web Service call")
    _order = "date desc"

    akawam_id = fields.Integer(string=_("Akawam id"), readonly=True)
    datas = fields.Text(string=_("Datas"), **fields_args)
    date = fields.Datetime(string=_("Date"), **fields_args)
    method = fields.Selection(
        [
            ("POST", _("POST")),
            ("PATCH", _("PATCH")),
        ]
    )
    model_name = fields.Char(string=_("Model name"), **fields_args)
    name = fields.Char(string=_("Route"), **fields_args)
    odoo_id = fields.Integer(string=_("Odoo id"), **fields_args)
    response_code = fields.Char(string=_("Response code"), **fields_args)
    response = fields.Text(string=_("Response"), **fields_args)
    time = fields.Float(string=_("Call time"))

    def call(self, route, record_id, datas):
        self = self.sudo()
        script_obj = self.env["script.tools"]
        # Generate hash and compare with stored hash
        hash = hash_dict(
            {
                "route": route,
                "record_id": script_obj.record_to_reference(record_id),
                "datas": datas,
            }
        )
        # Put force_akawam_sync to True in context to force sync
        if hash == record_id.akawam_last_hash and not self._context.get(
            "force_akawam_sync", False
        ):
            # If it's the same hash then don't send it cause it won't change anything
            return False
        else:
            # Otherwise store new hash and continue send WS
            self = self.with_context(force_akawam_sync=False)
            record_id = record_id.with_context(force_akawam_sync=False)
            record_id.akawam_last_hash = hash
        # Prepare URL and headers
        get_param = self.env["ir.config_parameter"].get_param
        base_url = get_param("akawam.base_url")
        while base_url[-1] == "/":
            base_url = base_url[:-1]
        url = base_url + route
        token = get_param("akawam.token")
        headers = {
            "Accept": "application/json",
            "Authorization": "Bearer %s" % (token),
            "Content-Type": "application/json",
        }
        # Set method based on existence of akawam_id
        method = "POST"
        if record_id.akawam_id:
            url += "/%s" % (record_id.akawam_id)
            method = "PATCH"

        start = time.time()
        response = requests.request(
            method, url, headers=headers, json={"data": datas}
        )
        stop = time.time()
        # Log the call
        call_id = self.create(
            {
                "datas": datas,
                "date": fields.Datetime.now(),
                "method": method,
                "model_name": record_id._name,
                "name": url,
                "odoo_id": record_id.id,
                "response_code": "%s" % (response),
                "response": "%s" % (response.text),
                "time": stop - start,
            }
        )
        response = json.loads(response.text)
        # Error handling
        if "data" not in response and method == "POST":
            error = _(
                """Error from Akawam side, please contact an administrator:\n\tResponse: %s\n\t[Method] URL: [%s] %s\n\tDatas: %s"""
            ) % (response, method, url, datas)
            raise UserError(error)
        # Update record_id and call_id
        if not record_id.akawam_id:
            record_id.akawam_id = response["data"]
        # Update the Akawam ID in the call log
        call_id.akawam_id = response.get("data", 0)
        return True  # Indicate that the call was successful
