# -*- coding:utf-8 -*-
from odoo import fields, models, api
import uuid


class contactExtension(models.Model):
    _inherit = 'res.partner'

    def _get_default_access_token(self):
        uid = uuid.uuid4()
        print('----')
        print(uid)
        print(str(uid))
        print('----')
        return uid

    access_token = fields.Char(string='Security Token', default=_get_default_access_token, copy=False)

