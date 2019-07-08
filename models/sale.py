# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from odoo.exceptions import ValidationError

class MiCustomer(models.Model):
    _name='mi.sale.customer'
    _description="Mi Sale Customer"
    
    name=fields.Char()
    customer_code=fields.Char(default='New')
    street=fields.Char()
    street2=fields.Char()
    city=fields.Char()
    zip=fields.Integer()
    country=fields.Char()
    mobile_no=fields.Char()
    cart_count=fields.Integer(compute="compute_cart_items")
    service_count=fields.Integer(compute="compute_service_count")
    
    #Relational Fields
    service_ids=fields.One2many('mi.service','customer_service_id',compute='compute_search_service_charge')
    order_ids=fields.One2many('mi.sale.order','customer_id')
    product_cart_ids=fields.Many2many('mi.product')
    
    @api.model
    def create(self,vals):
        if vals.get('customer_code','New')=='New':
            vals['customer_code']= self.env['ir.sequence'].next_by_code('mi.sale.customer') or '/'
            return super(MiCustomer,self).create(vals)
        
    @api.multi
    def name_get(self):
        context={}
        res=[]
        for record in self:
          if context.get('customer_special_name',False):
                res.append((record.id,record.name))
          else:
                res.append((record.id,'%s %s' %(record.name,record.city)))
        return res
    
    def compute_cart_items(self):
        action = {
                      'name': 'Mi product',
                      'type': 'ir.actions.act_window',
                      'res_model': 'mi.product',
                      'target': 'current',
                 }
        products=self.product_cart_ids
        self.cart_count=len(products)
        if self.cart_count>1:
            action['domain'] = [('id', 'in', products.ids)]
            action['view_mode'] = 'tree,form'
            return action
        else:
            action['views'] = [(self.env.ref('mi_app.product_form').id, 'form')]
            action['res_id'] = products.id
            return action
        
    def compute_service_count(self):
        action = {
                  'name':'Mi Service',
                  'type':'ir.actions.act_window',
                  'res_model': 'mi.service',
                  'target': 'current',
                  }
        services=self.service_ids
        self.service_count=services.search_count([('id','in',services.ids)])
        if self.service_count>1:
            action['domain'] = [('id', 'in', services.ids)]
            action['view_mode'] = 'tree,form'
            return action
        else:
            action['views'] = [(self.env.ref('mi_app.service_form').id, 'form')]
            action['res_id'] = services.id
            return action
            
        
    def compute_search_service_charge(self):
            self.service_ids=self.env['mi.service'].search([('service_charge','>',50)])
        

class MiSale(models.Model):
    _name = 'mi.sale'
    _inherits={'mi.sale.customer':'sale_customer_id'}
    _description="Mi Sales"
    _rec_name="sale_code"

    sale_code=fields.Char(default='New')
    sale_customer_id=fields.Many2one('mi.sale.customer',string="Customer Name",required=True,ondelete='cascade')
    sale_order_ids=fields.One2many('mi.sale.order','order_sale_id')
    
    def create(self,vals):
        if vals.get('sale_code','New')=='New':
            vals['sale_code']= self.env['ir.sequence'].next_by_code('mi.sale') or '/'
            return super(MiSale,self).create(vals)
    
class MiOrder(models.Model):
    _name='mi.sale.order'
    _description="Mi Sale Order"
    _rec_name="order_code"
    
    order_code=fields.Char(default='New')
    product_code=fields.Char(related='order_product_id.product_code')
    order_date=fields.Datetime()
    order_quantity=fields.Integer(string="Ordered Quantities")
    delivery_date=fields.Date()
    warranty_period=fields.Selection([('one_year','1 Year'),('two_year','2 Years'),('three_year','3 Years')])
    total_price=fields.Float()
    payment_type=fields.Selection([('COD','Cash On Delivery'),('Card','Card Payment')])
    
    #Relational Fields
    customer_id=fields.Many2one('mi.sale.customer')
    order_product_id=fields.Many2one('mi.product')
    order_sale_id=fields.Many2one('mi.sale')
    
    @api.onchange('order_quantity')
    def onchange_order_quantity(self):
            self.total_price=self.order_product_id.price * self.order_quantity
    
    def create(self,vals):
        if vals.get('order_code','New')=='New':
            vals['order_code'] = self.env['ir.sequence'].next_by_code('mi.sale.order') or '/'
            return super(MiOrder,self).create(vals)
    
    @api.multi
    def name_get(self):
        context={}
        res=[]
        for record in self:
            if context.get('order_special_name',False):
                res.append((record.id,record.customer_id.name))
            elif not record.exists():
                raise Exceptions("The record has been deleted")
            else:
                res.append((record.id,'%s,%s' %(record.customer_id.name,record.order_product_id.name)))
        return res
    
    @api.constrains('order_quantity')
    def check_order_quantity(self):
        if self.order_quantity==0:
            raise ValidationError('Order quantity should not be zero')
        
class MiDelivery(models.Model):
    _name='mi.sale.delivery'
    _inherit='mail.thread'
    _description="The Mi Delivery"
    _rec_name="delivery_customer_id"
    
    delivery_customer_id=fields.Many2one('mi.sale.customer',string="Delivery Customer")
    delivery_order_id=fields.Many2one('mi.sale.order',string="Delivery Order")
    delivery_datetime=fields.Datetime(string="Expected Delivery",track_visibility='onchange')
    state=fields.Selection([('shipped','Item Shipped'),
                             ('packed','Item Packed'),
                             ('out_delivery','Out for Delivery'),
                             ('delivered','Item Delivered')
                             ],default='shipped',track_visibility='onchange')
    payment_type=fields.Char()
    total_amount=fields.Float('Total Amount')
    
    @api.one
    def ship_progressbar(self):
        self.write({
                    'state':'shipped',
                    })
    
    @api.one
    def pack_progress(self):
        self.write({
                    'state':'packed',
                    })

    @api.one
    def out_progress(self):
        self.write({
                    'state':'out_delivery',
                    })

    @api.one
    def delivery_progress(self):
        self.write({
                    'state':'delivered',
                    })
    
    @api.onchange('delivery_order_id')
    def onchange_delivery_order_id(self):
        self.payment_type=self.delivery_order_id.payment_type
        self.total_amount=self.delivery_order_id.total_price
    
