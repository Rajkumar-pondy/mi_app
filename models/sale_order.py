# -*- coding: utf-8 -*-

from odoo import models, fields

class SaleOrder(models.Model):
    _inherit='sale.order'
    
    currency=fields.Many2one('res.currency')