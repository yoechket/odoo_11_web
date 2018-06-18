# -*- coding: utf-8 -*-

from openerp import models, api, fields, exceptions
import logging
from . import calculate
import math
_logger = logging.getLogger(__name__)


STATE_SEL = [('loading', 'Loading'), ('first', 'First'), ('second', 'Second'), ('saving', 'Saving')]

PLATER_SEL = [('1', '1'), ('2', '2'), ('3', '3')]
FERDIG2_SEL = [('f1', 'Stritchliner rill og perforering'),
               ('f2', 'Klipping')]

MEDIE_SEL = [('m1', 'Silk 90gr'), ('m2', 'Kopipapir 70gr'), ('m3', 'Skisseblokk')]
STORLEIK_SEL = [('a4', 'A4'), ('a5', 'A5')]

FARGER_SEL = [
    ('1_0', '1+0'),
    ('4_0', '4+0'),
    ('1_1', '1+1'),
    ('4_1', '4+1'),
    ('4_4', '4+4')
]

FARGER_KONV = {
    '1_0': 1,
    '4_0': 1,
    '1_1': 2,
    '4_1': 2,
    '4_4': 2,
}



class Design(models.TransientModel):
    _name = 'printing_wizard.design'

    name = fields.Char('Design')

class Trykk(models.TransientModel):
    _name = 'printing_wizard.trykk'

    name = fields.Char('Trykk')

class PrintFerdig1(models.TransientModel):
    _name = 'printing_wizard.ferdig1'

    name = fields.Char('Ferdiggjøring 1')
    ftrykk = fields.Many2one('printing_wizard.trykk', string='Trykk')


MASKINTYPER = [('trykk', 'Trykk'),
               ('ferdiggjoring', 'Ferdiggjøring'),
               ('digital_ark', 'Digitaltrykk Ark'),
               ('digital_rull', 'Digitaltrykk Rull'),
               ]


# Used to icnlude storleik_inn
field_names = ['maskin', 'storleik', 'medie', 'plater', 'sider', 'ant_sider',
               'antall', 'ferdiggjoring', 'klikk_ratio', 'direction', 'svinn', 'order']

class PrintingConfiguration(models.Model):
    _name = 'printing_wizard.printing_cfg'

    name = fields.Char('Configuration name', index=True)
    # A replica of the wizard but for saving
    maskin = fields.Many2one('printing_wizard.machine', domain="[('maskintype', '=', 'trykk')]", string='Maskin')
    storleik = fields.Many2one('printing_wizard.paper_format', domain="[('kind', '=', 'output')]", string='Format')
    #storleik_inn = fields.Many2one('printing_wizard.paper_format', domain="[('kind', '=', 'input'), ('machine', '=', maskin)]",
    #                               readonly=True, string='Input format')
    medie = fields.Many2one('product.product', domain="[('categ_id', '=', 'Media')]", string='Medie',
                            required=True)
    plater = fields.Selection(PLATER_SEL, 'Plater')
    sider = fields.Selection(FARGER_SEL, string='Farger')
    ant_sider = fields.Integer('Sider')
    antall = fields.Integer('Antall')

    #design = fields.Many2one('printing_wizard.design',  string='Design')
    #trykk = fields.Many2one('printing_wizard.trykk', string='Trykk')
    ferdiggjoring = fields.Many2many('printing_wizard.machine', domain="[('maskintype', '=', 'ferdiggjoring')]", string='Ferdiggjøring')

    # Calculated format_advice = fields.Char('Formatforslag', readonly=True)
    klikk_ratio = fields.Float('Antall trykk pr råformat', readonly=True)
    direction = fields.Selection([('landscape', 'Liggende'), ('portrait', 'Stående')],
                        string='Retning')
    svinn = fields.Float('Svinn')

    order = fields.Many2one('sale.order', 'Ordre')


class Machine(models.Model):
    _name = 'printing_wizard.machine'

    name = fields.Char('Maskinnavn')
    maskintype = fields.Selection(MASKINTYPER, string='Makintype')
    max_height = fields.Integer('Max høyde')
    max_width = fields.Integer('Max bredde', required=True)
    startup_product = fields.Many2one('product.product', string='Startup product')
    running_product = fields.Many2one('product.product', string='Running product')

class PaperFormat(models.Model):
    _name = 'printing_wizard.paper_format'

    name = fields.Char('Format', required=True)
    height = fields.Float('Høyde', required=True)
    width = fields.Float('Bredde', required=True)
    machine = fields.Many2one(comodel_name='printing_wizard.machine', string='Maskin')
    kind = fields.Selection([('input', 'Input'), ('output', 'Output')], string='Kind')

class PrintWIizard(models.TransientModel):
    _name = 'printing_wizard.printing_wizard'

    @api.onchange('medie')
    def _onchange_format(self):
        _logger.info('ONCHANGE RECALC')

        if not self.maskin:
            return # Must select machine first

        outh = self.storleik.height
        outw = self.storleik.width

        max_height = self.maskin.max_height
        max_width = self.maskin.max_width

        format = self.medie

        _logger.info('Onchange Checking for %s [%s %s]', format.name, format.height, format.width)
        inh = format.height
        inw = format.width
        ant, direction, svinn = calculate.calculate_format(inh, inw, outh, outw)

        advice = u"Du får %d eksemplarer og %.2f cm2 i svinn hvis du velger %s format." % (ant, svinn,
                {'landscape': u'Liggende',
                        'portrait': u'Stående'}[direction])
        advice += u" [%d %d %d %d]" % (inh, inw, outh, outw)
        _logger.info(u'Advice %s', advice)
        _logger.info(u'SVINN %s vs %s', svinn, format)

        self.format_advice = advice
        self.klikk_ratio = ant
        self.direction = direction
        self.svinn = svinn
        assert self.klikk_ratio

        new_context = dict(self.env.context).copy()
        new_context.update({'klikk_ratio': self.klikk_ratio})
        self.env.context = new_context

        idd = self.env.context.get('active_id')
        self.env.cr.execute('update printing_wizard_printing_wizard set klikk_ratio=%s where id=%s', (self.klikk_ratio, idd))
        assert self.klikk_ratio
        _logger.info('NEW CONTEXT %s', self.env.context)
        _logger.info(u'%s Onchange Format advice %s gives %s', self, advice, self.klikk_ratio)


    @api.onchange('maskin', 'storleik')
    def _recalc_format(self):
        _logger.info('RECALC %s %s', self.state, self.env.context)
        """
        inh = 60
        inw = 120
        """
        #inh = self.maskin.max_height
        #inw = self.maskin.max_width
        """"
        outh = 25
        outw = 10
        """

        if not self.maskin:
            return # Must select machine first

        outh = self.storleik.height
        outw = self.storleik.width

        possible = self.env['product.product'].search([('categ_id', '=', 'Media'),
                                                       ('width', '>', 0),
                                                       ('height', '>', 0)],
                                                      order='width asc, height asc')
        max_height = self.maskin.max_height
        max_width = self.maskin.max_width
        if self.state not in ('first', 'loading'):
            _logger.info('%s Recalc called but we are in state %s %s', self.id, self.state, self.klikk_ratio)
            assert self.klikk_ratio
            return

        _logger.info('Possible papers %s', possible)
        #practical = [x for x in possible if x.width <= max_width and x.height <= max_height]
        practical = possible

        #possible = self.env['printing_wizard.paper_format'].search([('kind', '=', 'input')])
        #_logger.info('All paper %s - machine %s', [x.name for x in possible], self.maskin.id)
        #practical = [x for x in possible if x.machine.id == self.maskin.id ]
        #_logger.info('Paper for machine %s', [(x.machine.id, x.name) for x in practical])
        _logger.info('Practical papers %s', practical)
        if not practical:
            _logger.info('No paper formats within spec %s %s %s', self.maskin, max_height, max_width)
            return # No paper formats for this machine

        best_format = [None, None]
        for format in practical:
            _logger.info('Checking for %s [%s %s]', format.name, format.height, format.width)
            inh = format.height
            inw = format.width
            ant, direction, svinn = calculate.calculate_format(inh, inw, outh, outw)

            advice = u"Du får %d eksemplarer og %.2f cm2 i svinn hvis du velger %s format." % (ant, svinn,
                {'landscape': u'Liggende',
                          'portrait': u'Stående'}[direction])
            advice += u" [%d %d %d %d]" % (inh, inw, outh, outw)
            _logger.info(u'Advice %s', advice)
            _logger.info(u'SVINN %s vs %s', svinn, best_format)
            if not best_format[1] or svinn < best_format[1]:
                best_format[0] = format
                best_format[1] = svinn

        self.format_advice = advice
        self.klikk_ratio = ant
        self.direction = direction
        self.svinn = svinn
        assert self.klikk_ratio
        new_context = dict(self.env.context).copy()
        new_context.update({'klikk_ratio': self.klikk_ratio})
        self.env.context = new_context
        idd = self.env.context.get('active_id')
        self.env.cr.execute('update printing_wizard_printing_wizard set klikk_ratio=%s where id=%s',
                             (self.klikk_ratio, idd))
        _logger.info('NEW CONTEXT %s', self.env.context)
        assert self.klikk_ratio
        self.write({'klikk_ratio': self.klikk_ratio})

        _logger.info(u'%s Format advice %s gives %s %s', self, advice, self.klikk_ratio, self.env.context)
        if best_format[0]:
            #self.storleik_inn = best_format[0]
            self.medie = best_format[0]

    @api.multi
    def _calc_format(self):
        inh = 60
        inw = 120

        outh = 25
        outw = 10

        ant, direction, svinn = calculate.calculate_format(inh, inw, outh, outw)

        advice = u"Du får %d eksemplarer og %.2f cm2 i svinn hvis du velger %s format." % (ant, svinn, direction)
        self.format_advice = advice

    state = fields.Selection(STATE_SEL, default='loading')
    maskin = fields.Many2one('printing_wizard.machine', domain="[('maskintype', '=', 'trykk')]", string='Maskin')
    storleik = fields.Many2one('printing_wizard.paper_format', domain="[('kind', '=', 'output')]", string='Format')
    #storleik_inn = fields.Many2one('printing_wizard.paper_format', domain="[('kind', '=', 'input'), ('machine', '=', maskin)]",
    #                               readonly=True, string='Input format')
    medie = fields.Many2one('product.product', domain="[('categ_id', '=', 'Media')]", string='Medie',
                            required=False,
                            states={'second': [('required', True)],
                                    'saving': [('required', True)]
                                    })
    plater = fields.Selection(PLATER_SEL, 'Plater')
    sider = fields.Selection(FARGER_SEL, string='Farger')
    ant_sider = fields.Integer('Sider')
    antall = fields.Integer('Antall')


    design = fields.Many2one('printing_wizard.design',  string='Design')

    trykk = fields.Many2one('printing_wizard.trykk', string='Trykk')
    ferdiggjoring = fields.Many2many('printing_wizard.machine', domain="[('maskintype', '=', 'ferdiggjoring')]", string='Ferdiggjøring')
    #ferdiggjoring1 = fields.Many2one('printing_wizard.machine', domain="[('maskintype', '=', 'ferdiggjoring')]", string='Ferdiggjøring 1')
    #ferdiggjoring2 = fields.Many2one('printing_wizard.machine', domain="[('id', '!=', ferdiggjoring1), ('maskintype', '=', 'ferdiggjoring')]",
    #                                 string='Ferdiggjøring 2')
    ##ferdiggjoring1 = fields.Many2one('printing_wizard.ferdig1', domain="[('ftrykk', '=', trykk)]", string='Ferdiggjøring 1')
    ##ferdiggjoring2 = fields.Selection(FERDIG2_SEL, string='Ferdiggjøring 2')

    #format_advice = fields.Char('Formatforslag', compute='_calc_format')
    format_advice = fields.Char('Formatforslag', readonly=True)
    klikk_ratio = fields.Float('Antall trykk pr råformat', readonly=True)
    direction = fields.Selection([('landscape', 'Liggende'), ('portrait', 'Stående')],
                        string='Retning')
    svinn = fields.Float('Svinn')

    order = fields.Many2one('sale.order', 'Ordre')

    configuration = fields.Many2one(comodel_name='printing_wizard.printing_cfg', string='Configuration', help='Leave open to create new')
    configuration_name = fields.Char('Configuration name')
    config_status = fields.Char('Status', readonly=True)

    def update_order(self):
        self.ensure_one()

        ordre = self.order
        self._recalc_format()
        if not self.klikk_ratio:
            raise exceptions.UserError('No klikk ratio is set.')

        assert self.klikk_ratio, 'Strange %s has this %s' % (self, self.klikk_ratio)
        konv = FARGER_KONV[self.sider]
        media_klikk = self.antall
        media_klikk /= self.klikk_ratio
        media_klikk *= (float(self.ant_sider)/2)
        klikk = media_klikk * konv
        media_klikk = math.ceil(media_klikk)
        klikk = math.ceil(klikk)
        _logger.info('Calculate klikk ratio %s konv %s gives media %s and klikk %s',
                     self.klikk_ratio, konv, media_klikk, klikk)

        processing_klikk = self.antall
        entities = [(self.maskin, klikk)]
        for ent in self.ferdiggjoring:
            _logger.info('Ferdiggjoring %s', ent)
            entities.append((ent, processing_klikk))

        for entity, qty in entities:
            if not entity.startup_product:
                _logger.warn('No startup product for %s', entity)
            else:
                linje = {'product_id': entity.startup_product.id,
                          'product_uom_qty': 1,
                          'product_uom': 1,
                          'order_id': ordre.id
                          }
                _logger.info('Creating SOL %s', linje)
                self.env['sale.order.line'].create(linje)

            linje = {'product_id': entity.running_product.id,
                     'product_uom_qty': qty,
                     'product_uom': 1,
                     'order_id': ordre.id
                     }
            _logger.info('Creating SOL %s', linje)
            self.env['sale.order.line'].create(linje)

        # Media
        linje = {'product_id': self.medie.id,
                 'product_uom_qty': media_klikk,
                 'product_uom': 1,
                 'order_id': ordre.id
                 }
        _logger.info('Creating SOL %s', linje)
        self.env['sale.order.line'].create(linje)

    @api.multi
    def next(self):
        _logger.info('NEXT %s %s', self.env.context, self.state)
        self.ensure_one()
        for wiz in self:
            if wiz.state == 'loading':
                if self.env.context['active_model'] == 'sale.order':
                    assert self.env.context['active_model'] == 'sale.order'
                    assert len(self.env.context['active_ids']) == 1
                    ordre = self.env['sale.order'].browse(self.env.context['active_ids'][0])
                    assert ordre
                    wiz.order = ordre

                assert wiz.order, 'Missing order'

                wiz.state = 'first'
                wiz.config_status = ''
                return {
                    'type': 'ir.actions.act_window',
                    'res_model': 'printing_wizard.printing_wizard',
                    'view_mode': 'form',
                    'view_type': 'form',
                     'res_id': wiz.id,
                    'views': [(False, 'form')],
                    'target': 'new',
                }

            elif wiz.state == 'first':
                if self.env.context['active_model'] == 'sale.order':
                    assert self.env.context['active_model'] == 'sale.order'
                    assert len(self.env.context['active_ids']) == 1
                    ordre = self.env['sale.order'].browse(self.env.context['active_ids'][0])
                    assert ordre
                    wiz.order = ordre

                assert wiz.order, 'Missing order'

                wiz.state = 'second'

                return {
                    'type': 'ir.actions.act_window',
                    'res_model': 'printing_wizard.printing_wizard',
                    'view_mode': 'form',
                    'view_type': 'form',
                     'res_id': wiz.id,
                    'views': [(False, 'form')],
                    'target': 'new',
                }
            elif wiz.state == 'second':
                assert wiz.order
                wiz.update_order()

                wiz.state = 'saving'

                return {
                    'type': 'ir.actions.act_window',
                    'res_model': 'printing_wizard.printing_wizard',
                    'view_mode': 'form',
                    'view_type': 'form',
                     'res_id': wiz.id,
                    'views': [(False, 'form')],
                    'target': 'new',
                }
            else:
                return {'type': 'ir.actions.act_window_close'}

    @api.multi
    def previous(self):
        _logger.info('PREVIOUS %s', self.env.context)
        self.ensure_one()

        for wiz in self:
            if wiz.state == 'second':
                wiz.state = 'first'

                wiz._recalc_format()


        return {
            'type': 'ir.actions.act_window',
            'res_model': 'printing_wizard.printing_wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': wiz.id,
            'views': [(False, 'form')],
            'target': 'new',
        }

    @api.multi
    def load_configuration(self):
        # Thi could maybe be replaced by a onchange
        _logger.info('LOAD %s %s', self.env.context, self.state)
        cfg = self.env['printing_wizard.printing_cfg']
        wiz = self
        if self.env.context['active_model'] == 'sale.order':
            assert self.env.context['active_model'] == 'sale.order'
            assert len(self.env.context['active_ids']) == 1
            ordre = self.env['sale.order'].browse(self.env.context['active_ids'][0])
            assert ordre
            wiz.order = ordre

        dbcfg = self.configuration
        if dbcfg:
            for field in field_names:
                field_value = getattr(dbcfg, field)
                setattr(self, field, field_value)
            self.config_status = 'Configuration loaded'
            self._recalc_format()

        self.config_status = 'No configuration given'
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'printing_wizard.printing_wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': wiz.id,
            'views': [(False, 'form')],
            'target': 'new',
        }


    @api.multi
    def save_configuration(self):
        cfg = self.env['printing_wizard.printing_cfg']
        self.ensure_one()
        wiz = self
        vals = {}
        vals['name'] = self.configuration_name
        for field in field_names:
            thevalue = getattr(self, field)

            if self._fields[field].type in ('one2many', 'many2many'):
                if thevalue and hasattr(thevalue, 'id'):
                    thevalue = [thevalue.id]
                elif thevalue:
                    thevalue = [x.id for x in thevalue]

                if thevalue:
                    assert type(thevalue) == list
                else:
                    thevalue = []
                vals[field] = [(6, 0, thevalue)]
            else:
                if hasattr(thevalue, 'id'):
                    thevalue = thevalue.id

                vals[field] = thevalue

        _logger.info('Ready to save configuration %s', vals)
        newcfg = cfg.create(vals)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'printing_wizard.printing_wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': wiz.id,
            'views': [(False, 'form')],
            'target': 'new',
        }
