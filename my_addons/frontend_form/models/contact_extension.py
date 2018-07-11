# -*- coding:utf-8 -*-
from odoo import fields, models, api


class contactExtension(models.Model):
    _inherit = 'res.partner'

    group_id = fields.Many2one('res.partner.group', string='Contact Group')