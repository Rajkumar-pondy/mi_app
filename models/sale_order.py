# -*- coding: utf-8 -*-

from odoo import models, fields

class SaleOrder(models.Model):
    _inherit='sale.order'
    
    currency_id=fields.Many2one('res.currency')