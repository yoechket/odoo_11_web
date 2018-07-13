# -*- coding:utf-8 -*-
from odoo import http
from odoo.http import request
import werkzeug


class contact_group(http.Controller):

    @http.route("/group/<int:group_id>/<token>", type='http', auth='user', website=True)
    def view_group(self, group_id, token=None, pdf=None, **post):
        if token:
            if pdf:
                return request.render('frontend_form.dummy')
            self.contact_country_ids = request.env['res.country'].sudo().search([])
            Group = request.env['res.partner.group'].sudo().search([('id', '=', group_id), ('access_token', '=', token)])
            self.group_sudo = Group.sudo()
            contacts = request.env['res.partner'].sudo().search([('group_id', '=', False)])
            values = {'group': self.group_sudo,
                      'token': token,
                      'action': request.env.ref('frontend_form.action_view_partner_groups').id,
                      'contact_country_ids': self.contact_country_ids,
                      'contacts': contacts}
            return request.render('frontend_form.contact_group', values)

    @http.route("/contact_group/create_contact",
                type='http',
                auth='user',
                website=True,)
    def group_create_contact(self,
                             contact_name,
                             contact_street,
                             contact_city,
                             contact_country,
                             contact_phone,
                             contact_email,
                                **post):
        values = {'name': contact_name,
                  'street': contact_street,
                  'city': contact_city,
                  'country_id': contact_country,
                  'phone': contact_phone,
                  'email': contact_email,
                  'group_id': self.group_sudo.id}
        request.env['res.partner'].sudo().create(values)
        return werkzeug.utils.redirect("/group/%s/%s" % (self.group_sudo.id, self.group_sudo.access_token))

    @http.route("/group/add_contact/<int:partner_id>/<int:group_id>/<token>", type='http', auth='user', website=True)
    def group_add_contact(self, partner_id, group_id, token, **post):
        partner = request.env['res.partner'].sudo().search([('id', '=', partner_id)])
        partner.write({'group_id': group_id})
        return werkzeug.utils.redirect("/group/%s/%s" % (group_id, token))

    @http.route("/group/unlink_contact/<int:partner_id>/<int:group_id>/<token>", type='http', auth='user', website=True)
    def group_unlink_contact(self, partner_id, group_id, token, **post):
        partner = request.env['res.partner'].sudo().search([('id', '=', partner_id)])
        partner.write({'group_id': False})
        return werkzeug.utils.redirect("/group/%s/%s" % (group_id, token))
