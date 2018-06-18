# -*- coding: utf-8 -*-

from openerp import models, api, fields
import logging

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
	_inherit = 'product.template'

	width = fields.Integer('Width', help='Width of media in mm')
	height = fields.Integer('Height', help='Height of media in mm')

