# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import UserError
import uuid


class contactGroup(models.Model):
    _name = 'res.partner.group'

    name = fields.Char(string='Name', required=True)
    partner_ids = fields.One2many('res.partner', 'group_id', string='Contacts')
    rank = fields.Integer(string='Rank')

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

    @api.constrains('rank')
    def _check_rank(self):
        if self.rank < 1:
            raise UserError('Rank needs to be a positive number!')
