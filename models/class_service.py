# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MiService(models.Model):
    _name = 'mi.service'
    _inherit='mi.service'
    
    currency_field=fields.Many2one('res.currency')
    service_charge=fields.Monetary('service charge','currency_field')