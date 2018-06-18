from openerp import fields, models, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'


    @api.multi
    def action_print_wizard(self):
        assert False


    @api.multi
    def print_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'printing_wizard.printing_wizard',
            'view_mode': 'form',
            'view_type': 'form',
            #'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new',
        }
