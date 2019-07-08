# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class MiProduct(models.Model):
    _name = 'mi.product'
    _description="Mi Products"
    _sql_constraints=[('name_unique','unique(name)','Name must be unique'),('check_price','check(price>0)','Price should not be zero')]
    _rec_name='name'

    name = fields.Char('Product Name')
    image=fields.Binary("Image")
    product_code=fields.Char(default='New',copy=False)
    manufacture_date = fields.Date('Manufacture Date')
    currencies=fields.Many2one('res.currency','Currencies',required=True)
    price = fields.Monetary('Price',currency_field='currencies',digits=(7,1),group_operator='avg')
    description=fields.Html('Description')
    product_availability = fields.Selection([('in_stock', 'In Stock'), ('out_stock', 'Out of Stock'), ('soon_available', 'Available Soon')],string="Product Availability")
    is_product_available = fields.Boolean(default=False)
    color=fields.Integer()
    
    #Relational Fields
    category_id=fields.Many2one('mi.product.category',string='Product Categories')
    
    @api.model
    def create(self,vals):
        if vals.get('product_code','New')=='New':
            vals['product_code']=self.env['ir.sequence'].next_by_code('mi.product') or '/'
            return super(MiProduct,self).create(vals)
    
    @api.constrains('name')
    def check_name_constrains(self):
        if len(self.name)<5:
            raise ValidationError("The product name should not be less than 5 characters")
        
   
class ProductCategory(models.Model):
    _name="mi.product.category"
    _description="Mi Product Category"
    _rec_name="category_name"

    category_code=fields.Char('Category Id')
    category_name=fields.Selection([('Phones','Mobile Phones'),('Tv','Mi Tv'),('Lights','Mi Lights'),('Bags','Mi Bags')])
    
    #Relational Fields
    product_ids=fields.One2many('mi.product','category_id',string="Products")
    