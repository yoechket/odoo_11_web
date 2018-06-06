# -*- coding:utf-8 -*-
from odoo.tests import common


class TestPartner(common.TransactionCase):

    def test_partner(self):
        lead_ids = self.env['crm.lead'].search([('partner_id', '!=', False)])
        print("######")
        print(lead_ids)
        print("######")
        for lead in lead_ids:
            print("#####")
            print(lead.name)
            print("#####")
            self.assertNotEqual(lead.partner_id.name, lead.name)
