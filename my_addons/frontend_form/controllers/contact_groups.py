# -*- coding:utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import get_records_pager


class contact_group(http.Controller):

    @http.route("/group/<int:group_id>/<token>", type='http', aut='public', website=True)
    def view(self, group_id, token=None, **post):
        if token:
            Group = request.env['res.partner.group'].sudo().search([('id', '=', group_id), ('access_token', '=', token)])
            group_sudo = Group.sudo()
            values = {'group': group_sudo,
                      'token': token}
            return request.render('frontend_form.contact_group', values)
