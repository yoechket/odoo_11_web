# -*- coding: utf-8 -*-
from odoo import fields, models, api
import uuid


class contactGroup(models.Model):
    _name = 'res.partner.group'

    name = fields.Char(string='Name')
    partner_ids = fields.One2many('res.partner', 'group_id', string='Contacts')

    def _get_default_access_token(self):
        uid = str(uuid.uuid4())
        return uid

    access_token = fields.Char(string='Security Token', default=_get_default_access_token, copy=False)

    @api.multi
    def preview_group(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': '/group/%s/%s' % (self.id, self.access_token)
        }
