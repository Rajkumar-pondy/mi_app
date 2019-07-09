# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MiNews(models.Model):
    _name = 'mi.newsfeed'
    _description="Mi News Feed"
    
    product_launch=fields.Char()
    product_img=fields.Binary()
    launching_date=fields.Date()
    about=fields.Text()
    categ_id=fields.Many2one('mi.product.category',string='Product Categories')
    
