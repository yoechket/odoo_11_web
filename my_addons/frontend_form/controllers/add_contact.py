# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class Contact(http.Controller):
    @http.route("/add_contact", type="http", auth="user", website=True)
    def add_contact(self):
        contact_country_ids = request.env['res.country'].sudo().search([])
        return request.render('frontend_form.add_contact', {'contact_country_ids': contact_country_ids})

    @http.route("/add_contact/create_contact",
                type="http", auth="user",
                website=True, method="post")
    def create_contact(self, contact_name,
                       contact_street,
                       contact_city,
                       contact_country,
                       contact_phone,
                       contact_email,
                       lead_name,
                       **post):
        partner_ids = request.env['res.partner'].sudo().search([
            ('name', '=', contact_name)
        ])
        if not partner_ids:
            partner_id = request.env['res.partner'].sudo().create({'name': contact_name,
                                                                   'street': contact_street,
                                                                   'city': contact_city,
                                                                   'country_id': contact_country,
                                                                   'phone': contact_phone,
                                                                   'email': contact_email})
            lead_ids = request.env['crm.lead'].sudo().search([
                ('name', '=', lead_name)
            ])
            if lead_ids:
                lead_id = lead_ids[0]
                lead_id.sudo().write({'partner_id': partner_id.id})
            elif not lead_ids:
                lead_id = request.env['crm.lead'].sudo().create({'partner_id': partner_id.id,
                                                                 'name': lead_name})
                return request.render(
                    'frontend_form.contact_created',
                    {'partner_id': partner_id,
                     'lead_id': lead_id})
        elif partner_ids:
            partner_ids = request.env['res.partner'].sudo().search([
                ('name', '=', contact_name)
            ])
            partner_id = partner_ids[0]
            lead_ids = request.env['crm.lead'].sudo().search([
                ('name', '=', lead_name)
            ])
            if lead_ids:
                lead_id = lead_ids[0]
                return request.render(
                    'frontend_form.existing_contact',
                    {'partner_id': partner_id,
                     'lead_id': lead_id}
                )
            elif not lead_ids:
                lead_id = request.env['crm.lead'].sudo().create({'partner_id': partner_id.id,
                                                                 'name': lead_name})
