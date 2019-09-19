# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MiService(models.Model):
    _name = 'mi.service'
    _description="Mi Service"
    _inherits={'mi.product':'product_service_id'}

    service_code=fields.Char(default='New')
    service_charge=fields.Float()
    code_customer=fields.Char()
    is_warranty_available=fields.Boolean()
    customer_service_id=fields.Many2one('mi.sale.customer',string="Name Customer")
    product_service_id=fields.Many2one('mi.product',string="Product Service",required=True,ondelete="restrict")
    
    @api.onchange('customer_service_id')
    def onchange_customer_id(self):
        if self.customer_service_id:
            self.code_customer=self.customer_service_id.customer_code
            
    @api.model
    def create(self,vals):
        if vals.get('service_code','New')=='New':
            vals['service_code']=self.env['ir.sequence'].next_by_code('mi.service') or '/'
            return super(MiService,self).create(vals)
    